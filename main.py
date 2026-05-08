import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Constants
G = 6.674e-11   # Gravitational Constant
M = 5.972e24    # Earth Mass
R = 6.371e6     # Earth Radius
MU = G * M

def start(vmultiplier, steps=10000, dt=10.0):
    r0 = R + 400e3
    vcircular = np.sqrt(MU / r0) # circular velocity

    x,y = r0, 0.0
    vx, vy = 0.0, vcircular * vmultiplier

    xlist,ylist = [x], [y]

    if vmultiplier >= np.sqrt(2):
        maxdistance = 20 * R # Escape
    elif vmultiplier >= 0.99:
        maxdistance = 10 * R # Orbital
    else:
        maxdistance = 5 * R # Sub Orbital

    crashed = False

    for _ in range(steps):
        r = np.hypot(x,y)

        if r > maxdistance:
            break
        if r < R:
            crashed = True
            xlist.append(x)
            ylist.append(y)
            break

        ax_val = -MU * x / r**3
        ay = -MU * y / r**3

        vx += ax_val * dt
        vy += ay * dt

        x += vx * dt
        y += vy *dt

        xlist.append(x)
        ylist.append(y)

    return np.array(xlist), np.array(ylist), crashed

fig,ax=plt.subplots(figsize=(8,8))
plt.subplots_adjust(bottom=0.18, top=0.95)

earth = plt.Circle((0,0), R, color='royalblue', alpha=0.8)
ax.add_patch(earth)

def updatelimits(xarray,yarray):
    if len(xarray) > 0:
        maxdist = max(np.max(np.abs(xarray)), np.max(np.abs(yarray)))
        if np.isfinite(maxdist):
            limit = max(2.5 * R, min(maxdist * 1.2, 20 * R))
            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)

xarray,yarray, crashed = start(1.0)
updatelimits(xarray,yarray)

orbit, = ax.plot([], [], color='tomato', lw=0.8, alpha=0.6)
satellite, = ax.plot([], [], 'yo', markersize=9, label='Satellite')
trail, = ax.plot([], [], color='tomato', lw=2)

crashmarker, = ax.plot([], [], 'rx', markersize = 12, markeredgewidth=2, label='Crash Point')

orbit.set_data(xarray, yarray)

vcircularvalue = np.sqrt(MU / (R + 400e3))
text = ax.text(
    0.02, 0.97, '', transform=ax.transAxes,
    verticalalignment='top', fontsize=9,
    bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8)
)

def update_text(vmultiplier, crashed=False):
    vescape = np.sqrt(2) * vcircularvalue
    vcurrent = vmultiplier * vcircularvalue

    if vmultiplier < 0.99:
        if crashed:
            orbit_type = 'Sub-Orbital (Crashed)'
        else:
            orbit_type = 'Sub-Orbital'
    elif vmultiplier < 1.01:
        orbit_type = 'Circular'
    elif vmultiplier < np.sqrt(2) - 0.01:
        orbit_type = 'Elliptical'
    else:
        orbit_type = 'Escape Trajectory'
    text.set_text(
        f'Orbit type : {orbit_type}\n'
        f'Current Speed : {vcurrent/1000:.2f} km/s\n'
        f'Circular Speed : {vcircularvalue/1000:.2f} km/s\n'
        f'Escape Speed : {vescape/1000:.2f} km/s'
    )

update_text(1.0, False)
ax.legend(loc='upper right')

framecounter = {'value': 0}
currentcrashed = {'value': False}

def animate(i):
    global xarray, yarray

    if len(xarray) == 0:
        return orbit, trail, satellite, crashmarker

    if framecounter['value'] >= len(xarray):
        framecounter['value'] = 0

    idx = framecounter['value']
    startidx = max(0, idx - 120)

    if idx > 0:
        trail.set_data(xarray[startidx:idx], yarray[startidx:idx])
    else:
        trail.set_data([], [])

    if currentcrashed['value'] and idx >= len(xarray) - 1:
        satellite.set_data([], [])
    else:
        satellite.set_data([xarray[idx]], [yarray[idx]])

    step = max(1, len(xarray) // 800)
    framecounter['value'] += step

    if framecounter['value'] >= len(xarray):
        framecounter['value'] = 0

    return orbit, trail, satellite, crashmarker

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=1000, cache_frame_data=False)

axslider = fig.add_axes([0.18, 0.06, 0.65, 0.03])

vmultiplierslider = Slider(axslider, 'Velocity Multiplier', 0.5, 1.6, valinit=1.0, valfmt='%0.2f')
axslider.axvline(1.0, color='tomato', lw=1.0, linestyle=':', alpha=0.5, label='Circular')
axslider.axvline(np.sqrt(2), color='tomato', lw=1.5, linestyle='--', label='Escape')

def on_slider(val):
    global xarray, yarray, currentcrashed

    xarray, yarray, crashed = start(val)

    currentcrashed['value'] = crashed

    if len(xarray) > 0:
        updatelimits(xarray,yarray)

        orbit.set_data(xarray, yarray)

        trail.set_data([], [])
        satellite.set_data([], [])

        if crashed and len(xarray) > 0:
            crashmarker.set_data([xarray[-1]], [yarray[-1]])
            crashmarker.set_visible(True)
        else:
            crashmarker.set_data([], [])
            crashmarker.set_visible(False)

        framecounter['value'] = 0
        update_text(val, crashed)

        fig.canvas.draw_idle()

vmultiplierslider.on_changed(on_slider)

ax.set_title('Orbital Mechanics Visualizer')
plt.show()
