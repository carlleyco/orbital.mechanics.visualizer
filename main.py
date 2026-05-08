import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.674e-11   # Gravitational Constant
M = 5.972e24    # Earth Mass
R = 6.371e6     # Earth Radius

def start(vmultiplier, steps=10000, dt=10.0):
    altitude = 400e3
    r0 = R + altitude
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

types = [
    (1.0,'Circular','orange'),
    (1.2,'Elliptical','purple'),
    (np.sqrt(2),'Escape','green'),
]

fig,ax = plt.subplots(figsize=(9,9))
earth = plt.Circle((0,0), R, color='royalblue', alpha = 0.8, label='Earth')
ax.add_patch(earth)

for vmultiplier, label, color in types:
    xarray, yarray = start(vmultiplier)
    ax.plot(xarray,yarray, color=color, lw=1.5, label=f'{label} (v x {vmultiplier:.3f})')
    ax.plot(xarray[0], yarray[0], 'o', color=color, markersize=6)

ax.set_aspect('equal')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title('Orbital Mechanics [Circular, Elliptical, Escape]')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()
