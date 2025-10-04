def get_asteroid(asteroid_id=3542519):
    import requests
    import json

    # NASA NeoWs API example
    url = f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}"
    params = {"api_key": "teMY7qAIMzQDC6rtdAR8d50ia6kb2O8ePfNDo7q2"}

    response = requests.get(url, params=params)
    if not response.ok:
        print("Error:", response.status_code)
        exit()

    data = response.json()

    # -------------------------------
    # 🌑 Basic Asteroid Information
    # -------------------------------
    name = data["name"]
    hazardous = data["is_potentially_hazardous_asteroid"]
    diameter = data["estimated_diameter"]["meters"]["estimated_diameter_max"]

    print(f"Asteroid: {name}")
    print(f"ID: {asteroid_id}")
    print(f"Estimated Diameter: {diameter:.2f} meters")
    print(f"Potentially Hazardous: {'Yes' if hazardous else 'No'}")

    # -------------------------------
    # Close Approach Information
    # -------------------------------
    if data["close_approach_data"]:
        approach = data["close_approach_data"][0]
        approach_date = approach["close_approach_date"]
        velocity = float(approach["relative_velocity"]["kilometers_per_hour"])
        distance = float(approach["miss_distance"]["kilometers"])
        orbiting_body = approach["orbiting_body"]

        print("\nClosest Approach:")
        print(f"Date: {approach_date}")
        print(f"Velocity: {velocity:,.0f} km/h")
        print(f"Miss Distance: {distance:,.0f} km")
        print(f"Orbiting Body: {orbiting_body}")
    else:
        print("\n(No close approach data available)")

    # -------------------------------
    # Orbital Data
    # -------------------------------
    orbital_data = data["orbital_data"]

    print("\nOrbital Parameters:")
    print(f"• Eccentricity: {orbital_data['eccentricity']}")
    print(f"• Semi-Major Axis: {orbital_data['semi_major_axis']} AU")
    print(f"• Inclination: {orbital_data['inclination']}°")
    print(f"• Ascending Node Longitude: {orbital_data['ascending_node_longitude']}°")
    print(f"• Perihelion Distance: {orbital_data['perihelion_distance']} AU")
    print(f"• Aphelion Distance: {orbital_data['aphelion_distance']} AU")
    print(f"• Orbital Period: {orbital_data['orbital_period']} days")
    print(f"• MOID (Earth): {orbital_data['minimum_orbit_intersection']} AU")

    # Orbit classification (nested dict)
    orbit_class = orbital_data["orbit_class"]
    print("\nOrbit Classification:")
    print(f"Type: {orbit_class['orbit_class_type']}")
    print(f"Description: {orbit_class['orbit_class_description']}")
    print(f"Range: {orbit_class['orbit_class_range']}")

import numpy as np

# get_asteroid()

# x, y, z in m
# x', y', z', in m/s
# radius m

import numpy as np

# Given parameters
diameter = 10
radius = diameter / 2
volume = (4.0 / 3.0) * np.pi * (radius ** 3)

# Starting asteroid parameters
ast_pos = np.array([0.0, 0.0, 0.0])  # [x, y, z]
ast_vel = np.array([0.0, 0.0, 0.0])  # [vx, vy, vz]
ast_acc = np.array([0.0, 0.0, 0.0])  # [ax, ay, az]

def angle_of_inclination(pos: np.ndarray, vel: np.ndarray) -> float:
    """
    Compute the angle of inclination between position and velocity vectors.
    """
    num = np.dot(pos, vel)
    den = np.linalg.norm(pos) * np.linalg.norm(vel)
    return (np.pi / 2) - np.arccos(num / den)


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


def p_of_t_phi(pos: np.ndarray) -> float:
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


def rho_of_p_r(pos: np.ndarray) -> float:
    """
    Density as a function of pressure and temperature.
    """
    P = p_of_t_phi(pos)
    T = t_of_h(pos)
    den = 0.2869 * (T + 273.1)
    return P / den





