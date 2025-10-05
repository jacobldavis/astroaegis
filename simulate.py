import rebound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. SIMULATION PARAMETERS ---
delta_v_from_impact = 0.0026  # 2.6 mm/s, converted to m/s
integration_time = 5  # Simulate for 5 years
n_frames = 200        # Number of frames in the animation

# --- NEW: DEFINE PHYSICAL CONSTANTS MANUALLY ---
METERS_PER_AU = 1.495978707e11  # Meters in one Astronomical Unit
SECONDS_PER_YEAR = 365.25 * 24 * 3600 # Seconds in one year

# --- 2. SETUP THE SIMULATIONS ---
sim = rebound.Simulation()
sim.units = ('yr', 'AU', 'Msun')
sim.add("Sun")

asteroid_orbit_params = {
    "primary": sim.particles[0], 
    "a": 1.64, "e": 0.38, "inc": 0.05, "m": 2.5e-15
}

# Control simulation (no impact)
sim_no_impact = sim.copy()
sim_no_impact.add(**asteroid_orbit_params)
p_no_impact = sim_no_impact.particles[1]

# Impact simulation
sim_with_impact = sim.copy()
sim_with_impact.add(**asteroid_orbit_params)
p_with_impact = sim_with_impact.particles[1]

# --- APPLY THE DELTA-V FROM THE IMPACT ---
# --- THIS IS THE CORRECTED SECTION ---
# Manually convert our delta-v from m/s to the simulation's units (AU/yr)
delta_v_au_per_yr = (delta_v_from_impact / METERS_PER_AU) * SECONDS_PER_YEAR
p_with_impact.vx -= delta_v_au_per_yr

# --- 3. RECORD THE ORBITS OVER TIME ---
times = np.linspace(0., integration_time, n_frames)
x_no_impact, y_no_impact = np.zeros(n_frames), np.zeros(n_frames)
x_with_impact, y_with_impact = np.zeros(n_frames), np.zeros(n_frames)

for i, t in enumerate(times):
    sim_no_impact.integrate(t)
    x_no_impact[i] = p_no_impact.x
    y_no_impact[i] = p_no_impact.y
    
    sim_with_impact.integrate(t)
    x_with_impact[i] = p_with_impact.x
    y_with_impact[i] = p_with_impact.y

# --- 4. CREATE THE ANIMATION ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel("Distance (AU)")
ax.set_ylabel("Distance (AU)")
ax.set_title("Asteroid Deflection Simulation")
ax.plot(0, 0, 'o', color='orange', markersize=10, label='Star')

trail1, = ax.plot([], [], ':', color='blue', label='Original Path')
asteroid1, = ax.plot([], [], 'o', color='blue')
trail2, = ax.plot([], [], '-', color='red', label='Deflected Path')
asteroid2, = ax.plot([], [], 'o', color='red')
time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, verticalalignment='top')
ax.legend(loc='upper right')

def animate(i):
    trail1.set_data(x_no_impact[:i+1], y_no_impact[:i+1])
    trail2.set_data(x_with_impact[:i+1], y_with_impact[:i+1])
    asteroid1.set_data([x_no_impact[i]], [y_no_impact[i]])
    asteroid2.set_data([x_with_impact[i]], [y_with_impact[i]])
    time_text.set_text(f'Time: {times[i]:.2f} years')
    return trail1, asteroid1, trail2, asteroid2, time_text

print("\nCreating animation... This may take a minute.")
ani = FuncAnimation(fig, animate, frames=n_frames, interval=50, blit=True)

try:
    ani.save('asteroid_deflection.gif', writer='imagemagick')
    print("\n✅ Success! Animation saved to 'asteroid_deflection.gif'")
except Exception as e:
    print(f"\nError saving animation: {e}")
    print("Please ensure ImageMagick is installed and accessible in your system's PATH.")