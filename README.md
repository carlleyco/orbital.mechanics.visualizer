# 🌍 Orbital Mechanics Visualizer

An orbital simulation built in Python using NumPy and Matplotlib.
This Project graphs how a satellite behaves in Earth's gravitational field based on different intial velocities.

## 🚀 Features
- **Real-Time orbital simulation** using Newtonian Gravity
- **Interactive Velocity Control** using a Slider
- Automatic **Orbit Classification**:
  - Sub-Orbital (Crash Trajectory)
  - Circular Orbit
  - Elliptical Orbit
  - Escape Trajectory
- **Live Velocity Tracking** of the Satellite
- **Crash Detection** with Crash Marker
- **Trail rendering** to Visualize Trajectory

## ⚙️ How it Works

### 🧠 Gravitational Model
The Simulation is based on Newton's Law of Gravitation:
**Gravitational Force**:
```
F = GMm / r²
```
**Acceleration**:
```
a = -GM / r³ * r⃗
```

### 🚀 Orbital Velocity
**Initial Velocity**:
```
v = √(GM / r)
```
Velocity Multiplier determines the Orbit Type:
- v < 1.0 → `sub-orbital (crash)`
- v ≈ 1.0 → `circular orbit`
- 1.0 < v < √2 → `elliptical orbit`
- v ≥ √2 → `escape trajectory`

**Escape Velocity**:
```
v = √(2GM / r)
```

### 🔢 Numerical Method
The simulation updates motion using **Euler's method**:
```
vx += ax * dt
vy += ay * dt
x  += vx * dt
y  += vy * dt
```

## 🧱 Code Structure

| Section / Function | Purpose |
|--------------------|--------|
| `constants (G, M, R, MU)` | Defines parameters of the Earth System|
| `start(vmultiplier)` | Runs the orbital simulation and returns data |
| `ax, ay computation` | Computes the gravitational acceleration vector |
| `Euler integration loop` | Updates velocity and position over time |
| `updatelimits()` | Adjusts zoom level of plot |
| `update_text()` | Updates live information box (orbit type + speed) |
| `animate()` | Handles satellite animation |
| `Slider (vmultiplierslider)` | Control of initial velocity |
| `on_slider()` | Recomputes orbit when user changes velocity |

---

## 🧠 What I Learned
- How Orbital Motion comes from Inverse Square Gravity
- Why Velocity determines the Orbit Type
- How to implement 2D physics with the help of vector components
- How animation and sliders can create better physics simulations
- How to structure simulation code into components

---

## 🔧 How It Can Be Improved
- **Runge-Kutta (RK4)** instead of Euler Integration for higher accuracy
- **Atmospheric Drag** for low Earth Orbit simulations
- **Multi-Body Gravity** (n-body simulation) implementation
- **Moon** or **Satellite** Network Systems
- **Compute Orbital Parameters**
  - eccentricity
  - semi-major axis
  - orbital period
- **Improve UI** with labels for apoapsis and periapsis

---

## ▶️ How to Run

**Requirements:** Python 3.8 or newer

**Install dependencies:**
```bash
pip install numpy matplotlib
```

**Run the simulator:**
```bash
python main.py
```

Use the velocity multiplier slider to adjust the orbit.

---

## 📌 Project Status
This is the **Final Stage** of the program fully functional with real time visualization and interactive control.
It can serve as a base for future simulation projects involving deeper orbital dynamics and multi-body systems.
Future improvements will be added listed above if there are any.

## 🎬 Demo

Video will be added here shortly.
