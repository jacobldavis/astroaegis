import numpy as np

# Given parameters
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
rho_met = 8000  # Density of asteroid (kg/m^3)
xi = 8000000  # heat of ablation (J/kg)
D_met = 100 # diameter of asteroid (m)
R_met = D_met / 2 # radius of asteroid (m)
C_D = 0.5
C_H = 0.05 

# Earth rotation parameters
omega_earth = 2 * np.pi / 86400 
earth_rotation_axis = np.array([0.0, 0.0, 1.0])
earth_radius = 6371000
earth_mass = 5.972e24

R_p1a1 = earth_radius + 100000.0  # Atmosphere boundary

# Volume and mass of asteroid
volume = (4.0 / 3.0) * np.pi * (R_met ** 3)
mass = rho_met * volume

# Starting asteroid parameters (in inertial frame, relative to Earth)
ast_pos = np.array([earth_radius + 15000000.0, 0.0, 0.0])
ast_vel = np.array([-50000.0, 0.0, 0.0])  
ast_acc = np.array([0.0, 0.0, 0.0]) 

diam_met = 358 * 2
volume_met = 4/3 * np.pi * ((diam_met/2)** 3)

rws = (20752640 / 3768) * 100

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

x_av = 765 * (10 ** -6)
E = 496000000
A = .06*(50 + (1.92) + 33.75)

def nuke_power():
    num = x_av * (E ** 0.633)
    den = A * (volume_met ** 0.8) * (115 ** 0.633)
    print((num/den)**(-1/0.633))

def nuke_power2():
    num = (x_av ** 6) * (volume_met ** -4.8)
    den = A ** 6 * (115/rws) ** (19/20)
    print((num / den) ** (-1/3.8))

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


def nuke_power3():
    return volume_met * (A/r_crit_calc(ast_pos, ast_vel)) ** 1.25 * (rws/115) ** .79

# kg of explosive
nuke_power()
nuke_power2()
print(nuke_power3())