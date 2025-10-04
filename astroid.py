import numpy as np

# Given parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_pl = 5.972e24  # Mass of Earth (kg)
R_pl = 6371000.0  # Radius of Earth (m)
R_p1a1 = R_pl + 7000000.0  # Distance from center of Earth to top of atmosphere (m)
rho_met = 3000  # Density of asteroid (kg/m^3)
C_D = 0.5
C_H = 0.1
xi = 8000000  # heat of ablation (J/kg)
D_met = 10
R_met = D_met / 2

# I Volume of asteroid (m^3)
volume = (4.0 / 3.0) * np.pi * (R_met ** 3)

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
    den = np.pi * (R_met ** 2)
    return num / den

# X r_crit
def r_crit_calc(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Calculate the critical radius of the asteroid.
    """
    return 100 * (surface_pressure(pos, vel) / 1e5) * (400 / rho_met) * (9.81 / g_of_h(atm_height)) * 1/(angle_of_inclination(pos, vel) * np.sqrt(2))

# XI 
def d_ad_t(t):
    rho_atm = rho_of_p_r(ast_pos)
    v = np.linalg.norm(ast_vel)

    num_1 = -3 * rho_atm * C_H * v ** 3
    den_1 = 4 * rho_met * xi
    first_term = num_1 / den_1

    num_2 = 42 * R_met * rho_atm * C_H * v ** 3 \
            * ((rho_met * xi)/(rho_atm * C_H * v ** 3 * t)) ** 3 \
            + 9 * ((rho_met * xi)/(rho_atm * C_H * v ** 3 * t ** 2)) \
            * rho_met * xi
    den_2 = 8 * rho_met * xi \
            * ((rho_met * xi)/(rho_atm * C_H * v ** 3 * t)) ** 3 \
            * np.sqrt(9 * R_met ** 2 + (21 * R_met * rho_atm * C_H * v**3 * t)/(rho_met * xi) + ((3 * rho_atm * C_H * v**3 * t)/(2 * rho_met * xi))**2)
    second_term = num_2 / den_2

    return first_term + second_term

# XII
def d_md_a(a):
    return (np.pi / 3) * rho_met * (-6 * a * R_met + 3 * a ** 2)

# XIII
def d_md_t(t, a):
    return d_ad_t(t) * d_md_a(a)

dt = 60.0
steps = 1000
in_atmosphere = False
a = R_met  # meteor burn-off coefficient
angle_of_incl = 0 # angle of inclination for when the meteor enters the atmosphere
point_of_entry = 0
time_entered_atmosphere = 0

for t in range(steps):
    # Update acceleration (pending)

    # Update velocity
    ast_vel += ast_acc * dt

    # Update position
    ast_pos += ast_vel * dt

    # Print current state
    print(f"Time: {t*dt:.1f} s, Position: {ast_pos}, Velocity: {ast_vel}, Acceleration: {ast_acc}")

    # Check if asteroid has entered the atmosphere
    if not in_atmosphere and np.linalg.norm(ast_pos) <= R_p1a1:
        print("Asteroid has entered the atmosphere.")
        in_atmosphere = True
        time_entered_atmosphere = t

        # Update entry values
        angle_of_incl = angle_of_inclination(ast_pos, ast_vel)
        point_of_entry = ast_pos
        R_crit = r_crit_calc(ast_pos, ast_vel)
        if R_met <= R_crit:
            print("YIPEE HURRAH")
            break
    
    # Update asteroid mass and radius now that it is in the atmosphere
    if in_atmosphere:
        a -= d_ad_t(dt * (t-time_entered_atmosphere+1))
        mass += d_md_t(dt * (t-time_entered_atmosphere+1), a)

        # Check if asteroid has reached the ground
        if np.linalg.norm(ast_pos) <= R_pl:
            curr_pos = ast_pos 
            prev_pos = ast_pos - ast_vel

            curr_vel = ast_vel
            prev_vel = ast_vel - ast_acc

            a_coeff = (curr_pos[0] - prev_pos[0]) ** 2 + (curr_pos[1] - prev_pos[1]) ** 2 +  (curr_pos[2] - prev_pos[2]) ** 2
            b_coeff = 2 * ((curr_pos[0] - prev_pos[0])*prev_pos[0] + (curr_pos[1] - prev_pos[1])*prev_pos[1] + (curr_pos[2] - prev_pos[2])*prev_pos[2])
            c_coeff = prev_pos[0] ** 2 + prev_pos[1] ** 2 + prev_pos[2] ** 2 - R_pl ** 2

            roots = np.roots([a_coeff, b_coeff, c_coeff])
            time = np.max(roots)

            impact_position = prev_pos + time * prev_vel 
            impact_velocity = prev_vel + time * ast_acc

            print(impact_position)
            print(impact_velocity)
            break
