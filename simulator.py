import numpy as np
import time
import math
# Import your asteroid.py file as a library
import asteroid

# --- 1. CUSTOMIZABLE PARAMETERS ---
TARGET_SEPARATION = 50000
lat_clem = 34.6834
long_clem = -82.8374
DT = 10.0
SIM_DURATION = 3600 * 10
PHI_RANGE = np.arange(0, 2 * np.pi, 0.4)
THETA_RANGE = np.arange(-0.5, 0.5, 0.25)

# --- 2. HELPER FUNCTIONS ---
def latlon_to_cartesian_offset(lat, lon, radius):
    lat_rad, lon_rad = math.radians(lat), math.radians(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return np.array([x, y, z])

def launch_vector_to_global(v, phi, theta, lat, lon, planet_vel):
    lat_rad, lon_rad = math.radians(lat), math.radians(lon)
    vx_local, vy_local, vz_local = v*np.cos(theta)*np.cos(phi), v*np.cos(theta)*np.sin(phi), v*np.sin(theta)
    c_lat, s_lat, c_lon, s_lon = np.cos(lat_rad), np.sin(lat_rad), np.cos(lon_rad), np.sin(lon_rad)
    R = np.array([[-s_lon, -s_lat*c_lon, c_lat*c_lon], [c_lon, -s_lat*s_lon, c_lat*s_lon], [0, c_lat, s_lat]])
    return R.dot(np.array([vx_local, vy_local, vz_local])) + planet_vel

def update_body_state(position, velocity, mass, planets_dict, dt):
    """Iterative updater that uses the function from your asteroid.py."""
    g_acc = asteroid.calculate_gravitational_acceleration(position, planets_dict)
    new_velocity = velocity + g_acc * dt
    new_position = position + new_velocity * dt
    return new_position, new_velocity

# --- 3. SIMULATOR ---
def run_intercept_search():
    print("--- Asteroid Intercept Simulator (using asteroid.py) ---")
    
    # Use the planets dictionary directly from your imported file
    planets = asteroid.planets
    earth = planets['Earth']

    # Calculate missile mass using the nuke_power() function from your file
    m_launch = asteroid.nuke_power() + 32000

    # Setup target asteroid (using a simple orbit for this scenario)
    initial_asteroid_pos = np.array([1.55e11, 0., 0.])
    initial_asteroid_vel = np.array([0., 28000., 0.])
    
    print(f"IV Mass set to: {m_launch:.2f} kg")
    print(f"Launching from: Lat {lat_clem}, Lon {long_clem}")
    best_attempt = {"min_dist": float('inf'), "phi": None, "theta": None}

    # --- 4. START THE LIVE SEARCH ---
    for LAUNCH_VELOCITY in range(10000, 20000, 1000):
        for phi in PHI_RANGE:
            for theta in THETA_RANGE:
                asteroid_pos, asteroid_vel = initial_asteroid_pos.copy(), initial_asteroid_vel.copy()
                
                launch_offset = latlon_to_cartesian_offset(lat_clem, long_clem, earth['radius'])
                iv_pos = earth['position'] + launch_offset
                iv_vel = launch_vector_to_global(LAUNCH_VELOCITY, phi, theta, lat_clem, long_clem, earth['velocity'])
                
                min_dist_this_run = float('inf')

                for t in np.arange(0, SIM_DURATION, DT):
                    # Update positions using full physics
                    asteroid_pos, asteroid_vel = update_body_state(asteroid_pos, asteroid_vel, 5e9, planets, DT)
                    iv_pos, iv_vel = update_body_state(iv_pos, iv_vel, m_launch, planets, DT)
                    
                    current_dist = np.linalg.norm(iv_pos - asteroid_pos)
                    if current_dist < min_dist_this_run:
                        min_dist_this_run = current_dist

                    if current_dist <= TARGET_SEPARATION:
                        print("\n" + "="*20 + " HIT! " + "="*20)
                        print(f"SUCCESSFUL INTERCEPT with parameters:")
                        print(f"  - v: {LAUNCH_VELOCITY} m/s, phi: {phi:.2f} rad, theta: {theta:.2f} rad")
                        return

                if min_dist_this_run < best_attempt["min_dist"]:
                    best_attempt = {"min_dist": min_dist_this_run, "phi": phi, "theta": theta}
                
                print(f"Attempt (phi={phi:.2f}, theta={theta:.2f}): Closest approach = {min_dist_this_run/1000:,.0f} km")

    print("\n--- SEARCH COMPLETE ---")
    print(f"Best attempt: Closest approach of {best_attempt['min_dist']/1000:,.0f} km with phi={best_attempt['phi']:.2f}, theta={best_attempt['theta']:.2f}")

if __name__ == "__main__":
    run_intercept_search()
