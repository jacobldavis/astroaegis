import numpy as np

# Given parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_pl = 5.972e24  # Mass of Earth (kg)
R_pl = 6371000.0  # Radius of Earth (m)
R_p1a1 = R_pl + 7000000.0  # Distance from center of Earth to top of atmosphere (m)
C_D = 0.5
C_H = 0.1
xi = 8000000  # heat of ablation (J/kg)
rho_met = 3000  # Density of asteroid (kg/m^3)
diameter = 10
radius = diameter / 2
a = 0  # meteor burn-off coefficient

# I Volume of asteroid (m^3)
volume = (4.0 / 3.0) * np.pi * (radius ** 3)

# II Mass of asteroid (kg)
mass = rho_met * volume

# Starting asteroid parameters (relative to earth) (in m)
ast_pos = np.array([-6550000.0, 0.0, 0.0])  # [x, y, z]
ast_vel = np.array([10.0, 0.0, 0.0])  # [vx, vy, vz]
ast_acc = np.array([5.0, 0.0, 0.0])  # [ax, ay, az]

atm_height = np.array([0, 0, 10000 * 1e3])  # [x, y, z]

# III angle of inclination entering atmosphere
def angle_of_inclination(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Compute the angle of inclination between position and velocity vectors.
    """
    num = np.dot(pos, vel)
    den = np.linalg.norm(pos) * np.linalg.norm(vel)
    return (np.pi / 2) - np.arccos(num / den)

# IV & V temperature at h
def t_of_h(pos: np.ndarray) -> float:
    """
    Temperature (or related function) as a function of altitude (magnitude of position vector).
    """
    h = np.linalg.norm(pos)
    if h > 25000:
        return -131.21 + 0.00299 * h
    elif 11000 < h <= 25000:
        return -56.4 * h
    else:
        return 15.04 - 0.00649 * h

# IV & VI atmospheric pressure at h
def p_of_t_h(pos: np.ndarray) -> float:
    """
    Pressure as a function of temperature and altitude.
    """
    h = np.linalg.norm(pos)
    T = t_of_h(pos)
    if h > 25000:
        return 2.448 * ((T + 273.1) / 216.6) ** -11.388
    elif 11000 < h <= 25000:
        return 22.65 * np.e ** (1.73 - 0.000157 * h)
    else:
        return 101.29 * ((T + 273.1) / 288.08) ** 5.256

# IV & VII atmospheric density at h
def rho_of_p_r(pos: np.ndarray) -> float:
    """
    Density as a function of pressure and temperature.
    """
    P = p_of_t_h(pos)
    T = t_of_h(pos)
    den = 0.2869 * (T + 273.1)
    return P / den

# IV & VIII force of gravity at h
def g_of_h(pos: np.ndarray) -> float:
    '''Gravitational acceleration as a function of altitude.'''
    return (G * M_pl) / ((np.linalg.norm(pos) + R_pl) ** 2)

#IX surface pressure
def surface_pressure(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Calculate the surface pressure on the asteroid.
    """
    num = -0.5 * C_D * rho_of_p_r(pos) * (np.linalg.norm(vel) ** 2) - g_of_h(pos) * mass / (np.linalg.norm(pos) + R_pl)
    den = np.pi * (radius ** 2)
    return num / den

# X r_crit
def r_crit(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Calculate the critical radius of the asteroid.
    """
    return 100 * (surface_pressure(pos, vel) / 1e5) * (400 / rho_met) * (9.81 / g_of_h(atm_height)) * 1/(angle_of_inclination(pos, vel) * np.sqrt(2))

dt = 60.0
steps = 1000
in_atmosphere = False

angle_of_incl = 0

for t in range(steps):
    # Update position
    ast_pos += ast_vel * dt

    # Update velocity
    ast_vel += ast_acc * dt

    # Calculate atmospheric density
    rho_atm = rho_of_p_r(ast_pos)

    # Calculate drag force
    F_drag = 0.5 * C_D * rho_atm * np.linalg.norm(ast_vel)**2 * np.pi * radius**2

    # Calculate acceleration due to drag
    a_drag = F_drag / mass

    # Update acceleration (assuming drag acts opposite to velocity)
    ast_acc = -a_drag * (ast_vel / np.linalg.norm(ast_vel)) + np.array([0, 0, -g_of_h(ast_pos)])

    # Print current state
    print(f"Time: {t*dt:.1f} s, Position: {ast_pos}, Velocity: {ast_vel}, Acceleration: {ast_acc}")

    # Check if asteroid has entered atmosphere
    if not in_atmosphere and np.linalg.norm(ast_pos) <= R_p1a1:
        print("Asteroid has entered the atmosphere.")
        in_atmosphere = True
        angle_of_incl = angle_of_inclination(ast_pos, ast_vel)
    elif in_atmosphere:
        # Calculate mass loss due to ablation
        mass_loss = (C_H * rho_atm * np.linalg.norm(ast_vel)**3) / (2 * xi) * dt
        mass -= mass_loss
        if mass <= 0:
            print("Asteroid has completely ablated.")
            break
        # Update radius based on new mass
        volume = mass / rho_met
        radius = ((3 * volume) / (4 * np.pi)) ** (1/3)

    # Check if asteroid has reached the ground
    if np.linalg.norm(ast_pos) <= R_pl:
        print("Asteroid has reached the ground.")
        break
