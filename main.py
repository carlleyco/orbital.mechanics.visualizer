import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Constants
G = 6.674e-11   # Gravitational Constant
M = 5.972e24    # Earth Mass
R = 6.371e6     # Earth Radius

def start(vmultiplier, steps=10000, dt=10.0):
    r0 = R + 400e3
    vcircular = np.sqrt(G * M / r0) # circular velocity

    x,y = r0, 0.0
    vx, vy = 0.0, vcircular * vmultiplier

    xlist,ylist = [x], [y]

    maxdistance = 20 * R if vmultiplier >= np.sqrt(2) else 10 * R

    for _ in range(steps):
        r = np.sqrt(x**2 + y**2)

        if r > maxdistance:
            break
        if r < R:
            break

        ax = -G * M * x / r**3
        ay = -G * M * y / r**3

        vx += ax * dt
        vy += ay * dt

        x += vx * dt
        y += vy *dt

        xlist.append(x)
        ylist.append(y)

    return np.array(xlist), np.array(ylist)

fig,ax=plt.subplots(figsize=(8,8))
plt.subplots_adjust(bottom=0.18, top=0.95)

earth = plt.Circle((0,0), R, color='royalblue', alpha=0.8)
ax.add_patch(earth)

def updatelimits(xarray,yarray):
    if len(xarray) > 0:
        maxdist = max(np.max(np.abs(xarray)), np.max(np.abs(yarray)))
        limit = max(2.5 * R, min(maxdist * 1.2, 20 * R))
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)

xarray,yarray = start(1.0)
updatelimits(xarray,yarray)

orbit, = ax.plot([], [], color='orange', lw=0.8, alpha=0.5)
satellite, = ax.plot([], [], 'yo', markersize=9, label='Satellite')
trail, = ax.plot([], [], color='orange', lw=2)

orbit.set_data(xarray, yarray)

vcircularvalue = np.sqrt(G * M / (R + 400e3))
text = ax.text(
    0.02, 0.97, '', transform=ax.transAxes,
    verticalalignment='top', fontsize=9,
    bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8)
)

def update_text(vmultiplier):
    vescape = np.sqrt(2) * vcircularvalue
    vcurrent = vmultiplier * vcircularvalue

    if vmultiplier < 0.99:
        orbit_type = 'Sub-Orbital / Crash'
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

update_text(1.0)
ax.legend(loc='upper right')

frame_idx = [0]

def animate(i):
    if len(xarray) == 0:
        return trail, satellite
    
    idx = frame_idx[0] % len(xarray)
    startidx = max(0, idx-120)

    if idx > 0:
        trail.set_data(xarray[startidx:idx], yarray[startidx:idx])
    else:
        trail.set_data([], [])
    
    satellite.set_data([xarray[idx]], [yarray[idx]])
    frame_idx[0] += 2

    return trail, satellite

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True)

axslider = fig.add_axes([0.18, 0.06, 0.65, 0.03])

vmultiplierslider = Slider(axslider, 'Velocity Multiplier', 0.5, 1.6, valinit=1.0, valfmt='%0.2f')
axslider.axvline(1.0, color='tomato', lw=1.0, linestyle=':', alpha=0.5, label='Circular')
axslider.axvline(np.sqrt(2), color='tomato', lw=1.5, linestyle='--', label='Escape')

def on_slider(val):
    global xarray, yarray
    xarray, yarray = start(val)

    updatelimits(xarray,yarray)
    
    orbit.set_data(xarray,yarray)
    trail.set_data([], [])
    satellite.set_data([], [])
    
    frame_idx[0] = 0
    update_text(vmultiplierslider.val)
    fig.canvas.draw_idle()

vmultiplierslider.on_changed(on_slider)

ax.set_title('Orbital Mechanics Visualizer')
plt.show()
