import numpy as np

# Given parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_pl = 5.972e24  # Mass of Earth (kg)
R_pl = 6371000.0  # Radius of Earth (m)
R_p1a1 = R_pl + 100000.0  # Distance from center of Earth to top of atmosphere (100 km)
rho_met = 8000  # Density of asteroid (kg/m^3)
xi = 8000000  # heat of ablation (J/kg)
D_met = 100 # diameter of asteroid (m)
R_met = D_met / 2 # radius of asteroid (m)
C_D = 0.5
C_H = 0.05 

# Earth rotation parameters
omega_earth = 2 * np.pi / 86400  # Earth's angular velocity (rad/s) - one rotation per day
earth_rotation_axis = np.array([0.0, 0.0, 1.0])  # Earth rotates around z-axis

# I Volume of asteroid (m^3)
volume = (4.0 / 3.0) * np.pi * (R_met ** 3)

# II Mass of asteroid (kg)
mass = rho_met * volume

# Starting asteroid parameters (relative to earth center) (in m)
ast_pos = np.array([R_pl + 150000.0, 0.0, 0.0])
ast_vel = np.array([-50000.0, 0.0, 0.0])  
ast_acc = np.array([0.0, 0.0, 0.0]) 

# III angle of inclination entering atmosphere
def angle_of_inclination(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Compute the angle of inclination between position and velocity vectors.
    """
    # Handle edge cases
    pos_mag = np.linalg.norm(pos)
    vel_mag = np.linalg.norm(vel)
    
    if pos_mag == 0 or vel_mag == 0:
        return 0.0
    
    num = np.dot(pos, vel)
    den = pos_mag * vel_mag
    cos_angle = np.clip(num / den, -1.0, 1.0) 
    return (np.pi / 2) - np.arccos(cos_angle)

# IV & V temperature at h (altitude above surface)
def t_of_h(pos: np.ndarray) -> float:
    """
    Temperature as a function of altitude above Earth's surface (in meters).
    """
    h = np.linalg.norm(pos) - R_pl  
    
    if h > 25000:
        return -131.21 + 0.00299 * h
    elif 11000 < h <= 25000:
        return -56.46  
    else:
        return 15.04 - 0.00649 * h

# IV & VI atmospheric pressure at h (in kPa)
def p_of_t_h(pos: np.ndarray) -> float:
    """
    Pressure as a function of temperature and altitude (returns kPa).
    """
    h = np.linalg.norm(pos) - R_pl 
    T = t_of_h(pos)
    
    if h > 25000:
        return 2.488 * ((T + 273.1) / 216.6) ** -11.388
    elif 11000 < h <= 25000:
        return 22.65 * np.exp(1.73 - 0.000157 * h)
    else:
        return 101.29 * ((T + 273.1) / 288.08) ** 5.256

# IV & VII atmospheric density at h (in kg/m^3)
def rho_of_p_r(pos: np.ndarray) -> float:
    """
    Density as a function of pressure and temperature.
    """
    P = p_of_t_h(pos) * 1000 
    T = t_of_h(pos)
    R_specific = 287 
    return P / (R_specific * (T + 273.15))

# IV & VIII force of gravity at h
def g_of_h(pos: np.ndarray) -> float:
    '''Gravitational acceleration as a function of distance from Earth's center.'''
    r = np.linalg.norm(pos)
    return (G * M_pl) / (r ** 2)

#IX surface pressure
def surface_pressure(pos: np.ndarray, vel: np.ndarray, current_mass: float, current_radius: float) -> float:
    """
    Calculate the surface pressure on the asteroid (ram pressure + weight).
    """
    rho_atm = rho_of_p_r(pos)
    v = np.linalg.norm(vel)
    g = g_of_h(pos)
    
    # Ram pressure + gravitational stress
    ram_pressure = 0.5 * rho_atm * (v ** 2)
    grav_stress = current_mass * g / (np.pi * (current_radius ** 2))
    
    return ram_pressure + grav_stress

# X r_crit
def r_crit_calc(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Calculate the critical radius of the asteroid.
    """
    surf_pressure = surface_pressure(pos, vel, mass, R_met)
    g = g_of_h(pos)  
    theta = abs(angle_of_inclination(pos, vel))
    
    if theta < 0.01:  # Avoid division by very small numbers
        theta = 0.01
    
    return 100 * (surf_pressure / 1e5) * (400 / rho_met) * (9.81 / g) * (np.sin(theta) * np.sqrt(2))

# XI ablation rate
def d_ad_t(t, pos, vel, current_radius):
    """Calculate the rate of change of ablation depth (m/s)."""
    if t <= 0:
        return 0.0
    
    rho_atm = rho_of_p_r(pos)
    v = np.linalg.norm(vel)
    
    if rho_atm <= 0 or v <= 0:
        return 0.0
    
    # Ablation rate formula: da/dt; simplified from our derived version
    ablation_rate = (rho_atm * C_H * (v ** 3)) / (2 * rho_met * xi)
    
    return ablation_rate

# XII mass change due to ablation
def d_md_a(a, current_radius):
    """Calculate mass change with respect to ablation depth.
    """
    effective_radius = R_met - a
    if effective_radius <= 0:
        return 0.0
    return -4 * np.pi * rho_met * (effective_radius ** 2)

# Simulation parameters
dt = 0.1  # Small time step for accuracy
steps = 200000
in_atmosphere = False
a = 0.0  # Cumulative ablation depth
angle_of_incl = 0
point_of_entry = np.zeros(3)
time_entered_atmosphere = 0

print(f"Initial mass: {mass:.2e} kg")
print(f"Initial radius: {R_met:.2f} m")
print(f"Initial position magnitude: {np.linalg.norm(ast_pos):.2e} m")
print(f"Initial position (x,y,z): {ast_pos}")
print(f"Atmosphere boundary: {R_p1a1:.2e} m")
print(f"Entry velocity: {np.linalg.norm(ast_vel):.2f} m/s")

# Calculate initial entry latitude/longitude
initial_lat = np.degrees(np.arcsin(ast_pos[2] / np.linalg.norm(ast_pos)))
initial_lon = np.degrees(np.arctan2(ast_pos[1], ast_pos[0]))
print(f"Entry point: {initial_lat:.2f}° N, {initial_lon:.2f}° E\n")

current_radius = R_met
current_mass = mass

for step in range(steps):
    total_time = step * dt
    
    # Calculate gravitational acceleration
    r_vec = ast_pos
    r_mag = np.linalg.norm(r_vec)
    
    if r_mag > 0:
        g_acc = -g_of_h(ast_pos) * (r_vec / r_mag)
    else:
        g_acc = np.array([0.0, 0.0, 0.0])
    
    # Calculate atmospheric velocity due to Earth's rotation
    omega_vec = omega_earth * earth_rotation_axis
    v_atmosphere = np.cross(omega_vec, ast_pos)
    
    # Calculate drag if in atmosphere (relative to rotating atmosphere)
    if in_atmosphere and r_mag > R_pl:
        rho_atm = rho_of_p_r(ast_pos)
        
        # Velocity relative to the rotating atmosphere
        v_relative = ast_vel - v_atmosphere
        v_mag = np.linalg.norm(v_relative)
        
        if v_mag > 0:
            A = np.pi * (current_radius ** 2)
            # Drag force opposes relative velocity
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
    
    # Check if asteroid has entered the atmosphere
    if not in_atmosphere and np.linalg.norm(ast_pos) <= R_p1a1:
        print(f"Asteroid entered atmosphere at t={step*dt:.1f} s")
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
        
        # Check if asteroid breaks up
        if current_radius <= R_crit and current_radius < 20:
            print("Small asteroid will break up before impact!")
            break
    
    # Update asteroid mass and radius in atmosphere
    if in_atmosphere and np.linalg.norm(ast_pos) > R_pl:
        time_in_atm = (step - time_entered_atmosphere + 1) * dt
        
        # Calculate ablation rate (m/s) using relative velocity
        da_dt = d_ad_t(time_in_atm, ast_pos, v_relative, current_radius)
        da = da_dt * dt  
        a += da  
        
        # Update radius
        new_radius = max(R_met - a, 0.01) 
        
        # Calculate mass change
        dm_da = d_md_a(a, current_radius)
        dm = dm_da * da 
        new_mass = max(current_mass + dm, 1.0)
        
        current_radius = new_radius
        current_mass = new_mass
        
        if step % 1000 == 0:
            altitude = np.linalg.norm(ast_pos) - R_pl
            percent_mass_remaining = (current_mass / mass) * 100
            mass_lost = mass - current_mass
            v_atm_mag = np.linalg.norm(v_atmosphere)
            print(f"t={step*dt:.1f}s, r={current_radius:.2f}m, m={percent_mass_remaining:.1f}%, lost={mass_lost:.2e}kg, alt={altitude:.0f}m, v={np.linalg.norm(ast_vel):.0f}m/s, v_atm={v_atm_mag:.0f}m/s")
        
        # Check if completely ablated
        if current_radius <= 0.1 or current_mass <= 1:
            print(f"\nAsteroid completely ablated at t={step*dt:.1f} s")
            print(f"Final altitude: {np.linalg.norm(ast_pos)-R_pl:.2f} m")
            break
    
    # Check if asteroid has reached the ground
    if np.linalg.norm(ast_pos) <= R_pl:
        print(f"\nAsteroid impacted Earth at t={step*dt:.1f} s ({step*dt/60:.2f} minutes)")
        print(f"Impact position (Cartesian): {ast_pos}")
        print(f"Impact velocity magnitude: {np.linalg.norm(ast_vel):.2f} m/s")
        print(f"Final mass: {current_mass:.2e} kg")
        print(f"Final radius: {current_radius:.2f} m")
        
        # Calculate impact location in geographic coordinates
        x, y, z = ast_pos
        
        # Latitude doesn't change with Earth's rotation
        latitude = np.degrees(np.arcsin(z / R_pl))
        
        # Grab longitude intertial
        longitude_inertial = np.degrees(np.arctan2(y, x))
        
        # Earth has rotated during the simulation
        earth_rotation_degrees = np.degrees(omega_earth * total_time)
        
        # Subtract Earth's rotation to get longitude in Earth's rotating frame
        longitude_earth_frame = longitude_inertial - earth_rotation_degrees
        
        # Normalize longitude to [-180, 180]
        while longitude_earth_frame > 180:
            longitude_earth_frame -= 360
        while longitude_earth_frame < -180:
            longitude_earth_frame += 360
        
        print(f"\nImpact Location (Earth-fixed coordinates):")
        print(f"Latitude: {latitude:.4f}°")
        print(f"Longitude: {longitude_earth_frame:.4f}°")
        
        # Determine hemisphere and direction
        lat_dir = "N" if latitude >= 0 else "S"
        lon_dir = "E" if longitude_earth_frame >= 0 else "W"
        print(f"Geographic: {abs(latitude):.4f}° {lat_dir}, {abs(longitude_earth_frame):.4f}° {lon_dir}")
        
        # Show the effect of Earth's rotation
        print(f"\nInertial frame longitude: {longitude_inertial:.4f}°")
        print(f"Earth rotated: {earth_rotation_degrees:.4f}°")
        print(f"Earth-fixed longitude: {longitude_earth_frame:.4f}°")
        
        # Calculate how far the impact point moved due to Earth's rotation
        if in_atmosphere:
            time_in_atmosphere = total_time - (time_entered_atmosphere * dt)
            rotation_angle = omega_earth * time_in_atmosphere
            # Distance depends on latitude
            rotation_distance = R_pl * np.cos(np.radians(latitude)) * rotation_angle
            print(f"\nTime in atmosphere: {time_in_atmosphere:.1f} s")
            print(f"Earth rotated {np.degrees(rotation_angle):.4f}° during atmospheric transit")
            print(f"Ground track shift: {rotation_distance/1000:.2f} km at this latitude")
        
        # Calculate impact energy (in megatons TNT)
        impact_energy_joules = 0.5 * current_mass * (np.linalg.norm(ast_vel) ** 2)
        impact_energy_megatons = impact_energy_joules / 4.184e15  # 1 megaton = 4.184e15 J
        print(f"\nImpact Energy: {impact_energy_megatons:.2f} megatons TNT")
        
        break
    
    # Safety check
    if step % 10000 == 0:
        print(f"Step {step}: r={np.linalg.norm(ast_pos):.2e} m, v={np.linalg.norm(ast_vel):.2f} m/s")