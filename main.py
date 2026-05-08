import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

    for _ in range(steps):
        r = np.sqrt(x**2 + y**2)

        if r > 10 * R or r < R:
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

xarray, yarray = start(1.0)

fig,ax=plt.subplots(figsize=(8,8))

earth = plt.Circle((0,0), R, color='royalblue', alpha=0.8)
ax.add_patch(earth)

orbit = ax.plot([], [], color='orange', lw=1.2, alpha=0.5)[0]
satellite = ax.plot([], [], 'yo', markersize=8, label='Satellite')[0]
trail = ax.plot([], [], color='orange', lw=1.5)[0]

limit = 1.5 * (R + 400e3)
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_aspect('equal')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title('Orbital Mechanics [Satellite]')
ax.legend()
ax.grid(True, alpha=0.3)

ax.plot(xarray,yarray, color='orange', lw=0.8, alpha=0.3)

def init():
    orbit.set_data([], [])
    satellite.set_data([], [])
    return orbit, satellite

def update(frame):
    start = max(0, frame - 100)
    trail.set_data(xarray[start:frame], yarray[start:frame])
    satellite.set_data([xarray[frame]], [yarray[frame]])
    return trail, satellite

step = 3
frames = range(0, len(xarray), step)

ani = animation.FuncAnimation(
    fig,update, frames=frames,
    init_func=init, interval=20, blit=True
)

plt.tight_layout()
plt.show()
