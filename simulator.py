import numpy as np
import math

# --- 1. PARAMETERS (MATCHED TO YOUR ASTEROID.PY) ---

# ASTEROID PROPERTIES
ASTEROID_DIAMETER = 100.0 # meters
ASTEROID_DENSITY = 8000   # kg/m^3
HEAT_OF_ABLATION = 8000000 # J/kg

# ENTRY CONDITIONS
ENTRY_ALTITUDE = 15000000.0 # 15,000 km
ENTRY_VELOCITY = 50000.0    # 50 km/s
ENTRY_ANGLE = 90.0          # degrees (straight down)

# SIMULATION SETTINGS
DT = 0.1  # Time step in seconds

# --- 2. PHYSICAL CONSTANTS & PLANET DATA (from your asteroid.py) ---
G = 6.67430e-11
C_D = 0.5
C_H = 0.05

EARTH = {
    'mass': 5.972e24, 
    'radius': 6371000.0,
}

# --- 3. ATMOSPHERIC PHYSICS FUNCTIONS (from your asteroid.py) ---

def get_temperature(altitude):
    """Temperature (Celsius) as a function of altitude (meters)."""
    h = altitude
    if h > 25000:
        return -131.21 + 0.00299 * h
    elif 11000 < h <= 25000:
        return -56.46  
    else:
        return 15.04 - 0.00649 * h

def get_pressure_kpa(altitude):
    """Pressure (kPa) as a function of temperature and altitude."""
    h = altitude
    T = get_temperature(h)
    if h > 25000:
        return 2.488 * ((T + 273.1) / 216.6) ** -11.388
    elif 11000 < h <= 25000:
        return 22.65 * np.exp(1.73 - 0.000157 * h)
    else:
        return 101.29 * ((T + 273.1) / 288.08) ** 5.256

def get_density(altitude):
    """Atmospheric density (kg/m^3) as a function of altitude."""
    if altitude > 100000: return 0.0 # Above 100km, density is negligible
    P_kpa = get_pressure_kpa(altitude)
    T_celsius = get_temperature(altitude)
    return (P_kpa * 1000) / (287 * (T_celsius + 273.15))

# --- 4. MAIN SIMULATION ---
def run_atmospheric_entry():
    print("--- Atmospheric Entry Simulator (Corrected Parameters) ---")

    # Initial calculations
    radius = ASTEROID_DIAMETER / 2.0
    initial_volume = (4.0 / 3.0) * np.pi * (radius ** 3)
    mass = ASTEROID_DENSITY * initial_volume
    initial_mass = mass
    
    # Set initial position and velocity vectors based on entry angle
    angle_rad = math.radians(ENTRY_ANGLE - 90) # Adjust angle for vector math
    start_pos_mag = EARTH['radius'] + ENTRY_ALTITUDE
    pos = np.array([start_pos_mag * np.cos(angle_rad), start_pos_mag * np.sin(angle_rad), 0.])
    
    # Velocity vector points towards the origin (Earth's center)
    vel = -ENTRY_VELOCITY * (pos / np.linalg.norm(pos))

    print(f"Initial State: Altitude={ENTRY_ALTITUDE/1000:.0f} km, Velocity={ENTRY_VELOCITY/1000:.1f} km/s, Angle={ENTRY_ANGLE}°")
    print(f"Asteroid Mass: {mass:.2e} kg, Radius: {radius:.2f} m")
    print("\n--- SIMULATION START ---")
    
    t = 0
    in_atmosphere = False
    
    while True:
        pos_mag = np.linalg.norm(pos)
        altitude = pos_mag - EARTH['radius']
        
        if altitude < 0: altitude = 0 # Don't go below ground

        # --- Physics Calculations ---
        g_force_mag = (G * EARTH['mass'] * mass) / (pos_mag**2)
        g_force_vec = -g_force_mag * (pos / pos_mag)
        
        drag_force_vec = np.array([0., 0., 0.])
        mass_loss_rate = 0.0
        
        # Check if inside atmosphere
        if altitude < 100000.0:
            if not in_atmosphere:
                print(f"Time: {t:4.1f}s - Atmosphere Entry at {altitude/1000:.1f} km")
                in_atmosphere = True

            atm_density = get_density(altitude)
            velocity_mag = np.linalg.norm(vel)
            
            if velocity_mag > 0:
                area = np.pi * radius**2
                # Drag Force
                drag_force_mag = 0.5 * C_D * atm_density * area * velocity_mag**2
                drag_force_vec = -drag_force_mag * (vel / velocity_mag)
                # Ablation (Mass Loss)
                mass_loss_rate = (0.5 * C_H * atm_density * area * velocity_mag**3) / HEAT_OF_ABLATION

        # Update mass and radius
        mass -= mass_loss_rate * DT
        if mass <= 0:
            print(f"\nTime {t:.1f}s: Asteroid completely ablated at {altitude/1000:.1f} km altitude.")
            break
        radius = ((3.0 * mass) / (4.0 * np.pi * ASTEROID_DENSITY))**(1/3)
        
        # Update motion
        total_force = g_force_vec + drag_force_vec
        acceleration = total_force / mass
        vel += acceleration * DT
        pos += vel * DT

        # Reporting
        if int(t/DT) % 200 == 0: # Print status every 10 seconds
            print(f"Time: {t:5.1f}s | Alt: {altitude/1000:7.1f} km | Vel: {np.linalg.norm(vel)/1000:5.1f} km/s | Mass Left: {(mass / initial_mass * 100):.1f}%")

        # Break condition for impact
        if altitude <= 0:
            print(f"\n--- IMPACT ---")
            impact_energy_J = 0.5 * mass * (np.linalg.norm(vel)**2)
            impact_energy_MT = impact_energy_J / 4.184e15
            print(f"Impact Velocity: {np.linalg.norm(vel)/1000:.2f} km/s")
            print(f"Final Mass: {mass:.2e} kg ({mass/initial_mass*100:.1f}% remaining)")
            print(f"Impact Energy: {impact_energy_MT:.2f} Megatons of TNT")
            break
            
        t += DT

if __name__ == "__main__":
    run_atmospheric_entry()