import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.674e-11   # Gravitational Constant
M = 5.972e24    # Earth Mass
R = 6.371e6     # Earth Radius

altitude = 400e3
r0 = R + altitude
vcircular = np.sqrt(G * M / r0) # circular velocity

x,y = r0, 0.0
vx, vy = 0.0, vcircular

dt = 10.0
t_max = 2 * np.pi * r0 / vcircular
steps = int(t_max / dt)

xlist,ylist = [x], [y]

for _ in range(steps):
    r = np.sqrt(x**2 + y**2)
    ax = -G * M * x / r**3
    ay = -G * M * y / r**3

    vx += ax * dt
    vy += ay * dt

    x += vx * dt
    y += vy *dt

    xlist.append(x)
    ylist.append(y)

xarray = np.array(xlist)
yarray = np.array(ylist)

fig,ax = plt.subplots(figsize=(8,8))
earth = plt.Circle((0,0), R, color='royalblue', alpha = 0.8, label='Earth')
ax.add_patch(earth)

ax.plot(xarray, yarray, color='tomato', lw=1.5, label='Orbit')
ax.plot(xarray[0], yarray[0], 'go', markersize=8, label='Start')

ax.set_aspect('equal')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title('Orbital Mechanics [Circular Orbit]')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()