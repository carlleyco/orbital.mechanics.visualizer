import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Constants
G = 6.674e-11
M = 5.972e24
R = 6.371e6
MU = G * M
alt = 400e3
r0 = R + alt
vcircular = np.sqrt(MU / r0)
vescape = np.sqrt(2) * vcircular

xarray, yarray, vxarray, vyarray = None, None, None, None

def start(vmultiplier, steps=10000, dt=10.0):
    x, y = r0, 0.0
    vx, vy = 0.0, vcircular * vmultiplier
    
    xlist, ylist = [x], [y]
    vxlist, vylist = [vx], [vy]
    
    maxdistance = 20 * R if vmultiplier >= np.sqrt(2) else (10 * R if vmultiplier >= 0.99 else 5 * R)
    crashed = False
    
    for _ in range(steps):
        r = np.hypot(x, y)
        if r > maxdistance or r < R:
            if r < R:
                crashed = True
                xlist.append(x)
                ylist.append(y)
            break
        
        factor = -MU / r**3
        vx += factor * x * dt
        vy += factor * y * dt
        x += vx * dt
        y += vy * dt
        
        xlist.append(x)
        ylist.append(y)
        vxlist.append(vx)
        vylist.append(vy)
    
    return np.array(xlist), np.array(ylist), np.array(vxlist), np.array(vylist), crashed

fig,ax=plt.subplots(figsize=(8,8))
plt.subplots_adjust(bottom=0.18, top=0.95)

earth = plt.Circle((0,0), R, color='royalblue', alpha=0.8)
ax.add_patch(earth)

currentlimit = {'value': 2.5 * R}

def updatelimits(xarray, yarray):
    if len(xarray) > 0:
        maxdist = max(np.max(np.abs(xarray)), np.max(np.abs(yarray)))

        if np.isfinite(maxdist):
            targetlimit = max(2.5 * R, min(maxdist * 1.2, 20 * R))

            # Smooth interpolation
            currentlimit['value'] += (targetlimit - currentlimit['value']) * 0.15

            limit = currentlimit['value']

            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)

xarray, yarray, vxarray, vyarray, crashed = start(1.0)
updatelimits(xarray,yarray)

orbit, = ax.plot([], [], color='tomato', lw=0.8, alpha=0.6)
satellite, = ax.plot([], [], 'yo', markersize=9, label='Satellite')
trail, = ax.plot([], [], color='tomato', lw=2)

crashmarker, = ax.plot([], [], 'rx', markersize = 12, markeredgewidth=2, label='Crash Point')

orbit.set_data(xarray, yarray)

text = ax.text(
    0.02, 0.97, '', transform=ax.transAxes,
    verticalalignment='top', fontsize=9,
    bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8)
)

def update_text(vmultiplier, crashed=False, vx_array=None, vy_array=None):
    vescape = np.sqrt(2) * vcircular

    if vx_array is not None and len(vx_array) > 0:
        idx = len(vx_array) - 1
        vcurrent = np.sqrt(vx_array[idx]**2 + vy_array[idx]**2)
    else:
        vcurrent = vmultiplier * vcircular

    if vmultiplier < 0.99:
        orbit_type = 'Sub-Orbital (Crashed)' if crashed else 'Sub-Orbital'
    elif vmultiplier < 1.01:
        orbit_type = 'Circular'
    elif vmultiplier < np.sqrt(2) - 0.01:
        orbit_type = 'Elliptical'
    else:
        orbit_type = 'Escape Trajectory'

    text.set_text(
        f'Orbit type : Circular\n'
        f'Current Speed : {vcircular/1000:.2f} km/s\n'
        f'Circular Speed : {vcircular/1000:.2f} km/s\n'
        f'Escape Speed : {vescape/1000:.2f} km/s'
    )

ax.legend(loc='upper right')

framecounter = {'value': 0}
currentcrashed = {'value': False}
updating = {'value': False}
sliderupdating = {'value': False}

def animate(i):
    global xarray, yarray, vxarray, vyarray

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
        
        # Update speed display in real-time during animation
        current_speed = np.sqrt(vxarray[idx]**2 + vyarray[idx]**2)
        val = vmultiplierslider.val
        
        if currentcrashed['value']:
            orbit_type = 'Sub-Orbital (Crashed)'
        elif val < 0.99:
            orbit_type = 'Sub-Orbital'
        elif val < 1.01:
            orbit_type = 'Circular'
        elif val < np.sqrt(2) - 0.01:
            orbit_type = 'Elliptical'
        else:
            orbit_type = 'Escape Trajectory'
        
        text.set_text(
            f'Orbit type : {orbit_type}\n'
            f'Current Speed : {current_speed/1000:.2f} km/s\n'
            f'Circular Speed : {vcircular/1000:.2f} km/s\n'
            f'Escape Speed : {vescape/1000:.2f} km/s'
        )

    step = max(1, len(xarray) // 800)
    framecounter['value'] += step

    if framecounter['value'] >= len(xarray):
        framecounter['value'] = 0

    return orbit, trail, satellite, crashmarker

ani = animation.FuncAnimation(fig, animate, interval=20, blit=False, save_count=1000, cache_frame_data=False)

axslider = fig.add_axes([0.18, 0.06, 0.65, 0.03])

vmultiplierslider = Slider(axslider, 'Velocity Multiplier', 0.5, 1.6, valinit=1.0, valfmt='%0.2f')
axslider.axvline(1.0, color='tomato', lw=1.0, linestyle=':', alpha=0.5, label='Circular')
axslider.axvline(np.sqrt(2), color='tomato', lw=1.5, linestyle='--', label='Escape')

def on_slider(val):
    global xarray, yarray, vxarray, vyarray, currentcrashed

    if sliderupdating['value']:
        return

    sliderupdating['value'] = True

    xarray, yarray, vxarray, vyarray, crashed = start(val)

    currentcrashed['value'] = crashed

    framecounter['value'] = 0

    updatelimits(xarray, yarray)

    orbit.set_data(xarray, yarray)

    trail.set_data([], [])
    satellite.set_data([], [])

    if crashed:
        crashmarker.set_data([xarray[-1]], [yarray[-1]])
        crashmarker.set_visible(True)
    else:
        crashmarker.set_data([], [])
        crashmarker.set_visible(False)

    # Update text with final velocity of the new orbit
    if len(vxarray) > 0:
        final_speed = np.sqrt(vxarray[-1]**2 + vyarray[-1]**2)
    else:
        final_speed = val * vcircular
    
    if val < 0.99:
        orbit_type = 'Sub-Orbital (Crashed)' if crashed else 'Sub-Orbital'
    elif val < 1.01:
        orbit_type = 'Circular'
    elif val < np.sqrt(2) - 0.01:
        orbit_type = 'Elliptical'
    else:
        orbit_type = 'Escape Trajectory'
    
    text.set_text(
        f'Orbit type : {orbit_type}\n'
        f'Current Speed : {final_speed/1000:.2f} km/s\n'
        f'Circular Speed : {vcircular/1000:.2f} km/s\n'
        f'Escape Speed : {vescape/1000:.2f} km/s'
    )

    fig.canvas.draw_idle()

    sliderupdating['value'] = False

vmultiplierslider.on_changed(on_slider)

ax.set_title('Orbital Mechanics Visualizer')
plt.show()
