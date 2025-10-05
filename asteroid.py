import numpy as np

# Given parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
rho_met = 8000  # Density of asteroid (kg/m^3)
xi = 8000000  # heat of ablation (J/kg)
D_met = 10 # diameter of asteroid (m)
R_met = D_met / 2 # radius of asteroid (m)
C_D = 0.5
C_H = 0.05 

# Earth rotation parameters
omega_earth = 2 * np.pi / 86400 
earth_rotation_axis = np.array([0.0, 0.0, 1.0])

# kg, m, m/s, m
planets = {
    'Mercury': {
        'mass': 3.285e23, 
        'position': np.array([-57.9e9, 0.0, 0.0]),  
        'velocity': np.array([0.0, 47360.0, 0.0]),  
        'radius': 2439700.0, 
    },
    'Venus': {
        'mass': 4.867e24, 
        'position': np.array([-108.2e9, 0.0, 0.0]), 
        'velocity': np.array([0.0, 35020.0, 0.0]), 
        'radius': 6051800.0, 
    },
    'Earth': {
        'mass': 5.972e24, 
        'position': np.array([0.0, 0.0, 0.0]),  
        'velocity': np.array([0.0, 0.0, 0.0]), 
        'radius': 6371000.0,
    },
    'Moon': {
        'mass': 7.342e22,
        'position': np.array([384400000.0, 0.0, 0.0]), 
        'velocity': np.array([0.0, 1022.0, 0.0]),
        'radius': 1737400.0, 
    },
    'Mars': {
        'mass': 6.39e23, 
        'position': np.array([227.9e9, 0.0, 0.0]), 
        'velocity': np.array([0.0, 24070.0, 0.0]), 
        'radius': 3389500.0, 
    },
    'Jupiter': {
        'mass': 1.898e27, 
        'position': np.array([778.5e9, 0.0, 0.0]), 
        'velocity': np.array([0.0, 13070.0, 0.0]),  
        'radius': 69911000.0, 
    },
    'Saturn': {
        'mass': 5.683e26,  
        'position': np.array([1434.0e9, 0.0, 0.0]),  
        'velocity': np.array([0.0, 9680.0, 0.0]),  
        'radius': 58232000.0,  
    },
    'Uranus': {
        'mass': 8.681e25, 
        'position': np.array([2871.0e9, 0.0, 0.0]),  
        'velocity': np.array([0.0, 6800.0, 0.0]),  
        'radius': 25362000.0,  
    },
    'Neptune': {
        'mass': 1.024e26, 
        'position': np.array([4495.0e9, 0.0, 0.0]), 
        'velocity': np.array([0.0, 5430.0, 0.0]),  
        'radius': 24622000.0,
    },
}

# Earth parameters for atmosphere and impact
earth_mass = planets['Earth']['mass']
earth_radius = planets['Earth']['radius']
earth_pos = planets['Earth']['position']
R_p1a1 = earth_radius + 100000.0  # Atmosphere boundary

# Volume and mass of asteroid
volume = (4.0 / 3.0) * np.pi * (R_met ** 3)
mass = rho_met * volume

# Starting asteroid parameters (in inertial frame, relative to Earth)
ast_pos = np.array([earth_radius + 15000000.0, 0.0, 0.0])
ast_vel = np.array([-50000.0, 0.0, 0.0])  
ast_acc = np.array([0.0, 0.0, 0.0]) 

def calculate_gravitational_acceleration(ast_position, planets_dict):
    """
    Calculate total gravitational acceleration on asteroid from all planets.
    
    Args:
        ast_position: Position of asteroid in inertial frame (m)
        planets_dict: Dictionary of planet data
    
    Returns:
        Total gravitational acceleration vector (m/s^2)
    """
    total_acc = np.array([0.0, 0.0, 0.0])
    
    for planet_name, planet_data in planets_dict.items():
        # Vector from planet to asteroid
        r_vec = ast_position - planet_data['position']
        r_mag = np.linalg.norm(r_vec)
        
        if r_mag > 0:
            # Gravitational acceleration: a = -GM/r^2 * r_hat
            g_magnitude = G * planet_data['mass'] / (r_mag ** 2)
            g_direction = -r_vec / r_mag 
            total_acc += g_magnitude * g_direction
    
    return total_acc

# III
def angle_of_inclination(pos: np.ndarray, vel: np.ndarray) -> float:
    """Compute the angle of inclination between position and velocity vectors."""
    pos_mag = np.linalg.norm(pos)
    vel_mag = np.linalg.norm(vel)
    
    if pos_mag == 0 or vel_mag == 0:
        return 0.0
    
    num = np.dot(pos, vel)
    den = pos_mag * vel_mag
    cos_angle = np.clip(num / den, -1.0, 1.0) 
    return (np.pi / 2) - np.arccos(cos_angle)

# V
def t_of_h(pos: np.ndarray) -> float:
    """Temperature as a function of altitude above Earth's surface."""
    h = np.linalg.norm(pos) - earth_radius
    
    if h > 25000:
        return -131.21 + 0.00299 * h
    elif 11000 < h <= 25000:
        return -56.46  
    else:
        return 15.04 - 0.00649 * h

# VI
def p_of_t_h(pos: np.ndarray) -> float:
    """Pressure as a function of temperature and altitude (returns kPa)."""
    h = np.linalg.norm(pos) - earth_radius
    T = t_of_h(pos)
    
    if h > 25000:
        return 2.488 * ((T + 273.1) / 216.6) ** -11.388
    elif 11000 < h <= 25000:
        return 22.65 * np.exp(1.73 - 0.000157 * h)
    else:
        return 101.29 * ((T + 273.1) / 288.08) ** 5.256

# VII
def rho_of_p_r(pos: np.ndarray) -> float:
    """Density as a function of pressure and temperature."""
    P = p_of_t_h(pos) * 1000 
    T = t_of_h(pos)
    R_specific = 287 
    return P / (R_specific * (T + 273.15))

# VIII
def g_of_h(pos: np.ndarray) -> float:
    """Gravitational acceleration from Earth."""
    r = np.linalg.norm(pos)
    return (G * earth_mass) / (r ** 2)

# IX
def surface_pressure(pos: np.ndarray, vel: np.ndarray, current_mass: float, 
                    current_radius: float) -> float:
    """Calculate the surface pressure on the asteroid."""
    rho_atm = rho_of_p_r(pos)
    v = np.linalg.norm(vel)
    g = g_of_h(pos)
    
    ram_pressure = 0.5 * rho_atm * (v ** 2)
    grav_stress = current_mass * g / (np.pi * (current_radius ** 2))
    
    return ram_pressure + grav_stress

# X
def r_crit_calc(pos: np.ndarray, vel: np.ndarray) -> float:
    """Calculate the critical radius of the asteroid."""
    surf_pressure = surface_pressure(pos, vel, mass, R_met)
    g = g_of_h(pos)
    theta = abs(angle_of_inclination(pos, vel))
    
    if theta < 0.01:
        theta = 0.01
    
    return 100 * (surf_pressure / 1e5) * (400 / rho_met) * (9.81 / g) * (np.sin(theta) * np.sqrt(2))

# XII
def d_ad_t(t, pos, vel, current_radius):
    """Calculate the rate of change of ablation depth (m/s)."""
    if t <= 0:
        return 0.0
    
    rho_atm = rho_of_p_r(pos)
    v = np.linalg.norm(vel)
    
    if rho_atm <= 0 or v <= 0:
        return 0.0
    
    ablation_rate = (rho_atm * C_H * (v ** 3)) / (2 * rho_met * xi)
    return ablation_rate

# XIII
def d_md_a(a, current_radius):
    """Calculate mass change with respect to ablation depth."""
    effective_radius = R_met - a
    if effective_radius <= 0:
        return 0.0
    return -4 * np.pi * rho_met * (effective_radius ** 2)

# XIV 
rws = (20752640 / 3768) * 100
A = .06*(50 + (1.92) + 33.75)

def nuke_power():
    return volume * (A/r_crit_calc(ast_pos, ast_vel)) ** 1.25 * (rws/115) ** .79

# Simulation parameters
dt = 0.1
steps = 200000
in_atmosphere = False
a = 0.0
angle_of_incl = 0
point_of_entry = np.zeros(3)
time_entered_atmosphere = 0

print(f"Active Planets:")
for name, data in planets.items():
    print(f"  {name}: mass={data['mass']:.2e} kg, pos={data['position']}")
print(f"\nTarget: Earth (always)")
print(f"Initial asteroid mass: {mass:.2e} kg")
print(f"Initial asteroid radius: {R_met:.2f} m")
print(f"Initial position: {ast_pos}")
print(f"Entry velocity: {np.linalg.norm(ast_vel):.2f} m/s\n")

current_radius = R_met
current_mass = mass

for step in range(steps):
    total_time = step * dt
    
    # Update planet positions (if they have velocities)
    for planet_name, planet_data in planets.items():
        if np.linalg.norm(planet_data['velocity']) > 0:
            planet_data['position'] += planet_data['velocity'] * dt
    
    # Calculate gravitational acceleration from planets
    g_acc = calculate_gravitational_acceleration(ast_pos, planets)
    
    # Distance from Earth
    r_mag = np.linalg.norm(ast_pos)
    
    # Calculate atmospheric velocity due to Earth's rotation
    omega_vec = omega_earth * earth_rotation_axis
    v_atmosphere = np.cross(omega_vec, ast_pos)
    
    # Calculate drag if in atmosphere
    if in_atmosphere and r_mag > earth_radius:
        rho_atm = rho_of_p_r(ast_pos)
        v_relative = ast_vel - v_atmosphere
        v_mag = np.linalg.norm(v_relative)
        
        if v_mag > 0:
            A = np.pi * (current_radius ** 2)
            drag_force = -0.5 * C_D * rho_atm * A * v_mag * v_relative
            drag_acc = drag_force / current_mass if current_mass > 0 else np.array([0.0, 0.0, 0.0])
        else:
            drag_acc = np.array([0.0, 0.0, 0.0])
    else:
        drag_acc = np.array([0.0, 0.0, 0.0])
        v_relative = ast_vel 
    
    ast_acc = g_acc + drag_acc
    
    # Update velocity and position
    ast_vel += ast_acc * dt
    ast_pos += ast_vel * dt
    
    # Check atmosphere entry
    if not in_atmosphere and r_mag <= R_p1a1:
        print(f"Asteroid entered Earth's atmosphere at t={step*dt:.1f} s")
        print(f"Position: {ast_pos}")
        print(f"Velocity magnitude: {np.linalg.norm(ast_vel):.2f} m/s\n")
        
        in_atmosphere = True
        time_entered_atmosphere = step
        angle_of_incl = angle_of_inclination(ast_pos, ast_vel)
        point_of_entry = ast_pos.copy()
        
        R_crit = r_crit_calc(ast_pos, ast_vel)
        print(f"Critical radius: {R_crit:.2f} m")
        print(f"Current radius: {current_radius:.2f} m")
        print(f"Angle of inclination: {np.degrees(angle_of_incl):.2f} degrees\n")

        print(f"Nuke Power Needed to Explode it: {nuke_power()}")
        
        if current_radius <= R_crit and current_radius < 20:
            print("Small asteroid will break up before impact!")
            break
    
    # Update ablation
    if in_atmosphere and r_mag > earth_radius:
        time_in_atm = (step - time_entered_atmosphere + 1) * dt
        
        da_dt = d_ad_t(time_in_atm, ast_pos, v_relative, current_radius)
        da = da_dt * dt  
        a += da  
        
        new_radius = max(R_met - a, 0.01) 
        dm_da = d_md_a(a, current_radius)
        dm = dm_da * da 
        new_mass = max(current_mass + dm, 1.0)
        
        current_radius = new_radius
        current_mass = new_mass
        
        if step % 1000 == 0:
            altitude = r_mag - earth_radius
            percent_mass_remaining = (current_mass / mass) * 100
            mass_lost = mass - current_mass
            print(f"t={step*dt:.1f}s, r={current_radius:.2f}m, m={percent_mass_remaining:.1f}%, lost={mass_lost:.2e}kg, alt={altitude:.0f}m, v={np.linalg.norm(ast_vel):.0f}m/s")
        
        if current_radius <= 0.1 or current_mass <= 1:
            print(f"\nAsteroid completely ablated at t={step*dt:.1f} s")
            print(f"Final altitude: {r_mag - earth_radius:.2f} m")
            break
    
    # Check for impact with Earth
    if r_mag <= earth_radius:
        print(f"\nAsteroid impacted Earth at t={step*dt:.1f} s ({step*dt/60:.2f} minutes)")
        print(f"Impact position (Cartesian): {ast_pos}")
        print(f"Impact velocity magnitude: {np.linalg.norm(ast_vel):.2f} m/s")
        print(f"Final mass: {current_mass:.2e} kg")
        print(f"Final radius: {current_radius:.2f} m")
        
        # Geographic coordinates
        x, y, z = ast_pos
        latitude = np.degrees(np.arcsin(z / earth_radius))
        longitude_inertial = np.degrees(np.arctan2(y, x))
        earth_rotation_degrees = np.degrees(omega_earth * total_time)
        longitude_earth_frame = longitude_inertial - earth_rotation_degrees
        
        while longitude_earth_frame > 180:
            longitude_earth_frame -= 360
        while longitude_earth_frame < -180:
            longitude_earth_frame += 360
        
        print(f"\nImpact Location (Earth-fixed coordinates):")
        print(f"Latitude: {latitude:.4f}°")
        print(f"Longitude: {longitude_earth_frame:.4f}°")
        
        lat_dir = "N" if latitude >= 0 else "S"
        lon_dir = "E" if longitude_earth_frame >= 0 else "W"
        print(f"Geographic: {abs(latitude):.4f}° {lat_dir}, {abs(longitude_earth_frame):.4f}° {lon_dir}")
        
        print(f"\nInertial frame longitude: {longitude_inertial:.4f}°")
        print(f"Earth rotated: {earth_rotation_degrees:.4f}°")
        print(f"Earth-fixed longitude: {longitude_earth_frame:.4f}°")
        
        if in_atmosphere:
            time_in_atmosphere = total_time - (time_entered_atmosphere * dt)
            rotation_angle = omega_earth * time_in_atmosphere
            rotation_distance = earth_radius * np.cos(np.radians(latitude)) * rotation_angle
            print(f"\nTime in atmosphere: {time_in_atmosphere:.1f} s")
            print(f"Earth rotated {np.degrees(rotation_angle):.4f}° during atmospheric transit")
            print(f"Ground track shift: {rotation_distance/1000:.2f} km at this latitude")
        
        # Impact energy
        impact_energy_joules = 0.5 * current_mass * (np.linalg.norm(ast_vel) ** 2)
        impact_energy_megatons = impact_energy_joules / 4.184e15
        print(f"\nImpact Energy: {impact_energy_megatons:.2f} megatons TNT")
        
        break
    
    if step % 10000 == 0:
        print(f"Step {step}: r_earth={r_mag:.2e} m, v={np.linalg.norm(ast_vel):.2f} m/s")