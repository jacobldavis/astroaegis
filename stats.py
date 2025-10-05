import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Create a Sample DataFrame ---
data = pd.read_csv('data.csv')

# --- Display Descriptive Statistics ---
print("--- Descriptive Statistics ---")
print("\n[Relative Velocity (KPH)]")
print(data['relative_velocity_kph'].describe())

print("\n[Estimated Minimum Diameter (meters)]")
print(data['estimated_diameter_min_m'].describe())

print("\n[Estimated Maximum Diameter (meters)]")
print(data['estimated_diameter_max_m'].describe())
print("\n" + "="*30 + "\n")


# --- Plotting and Saving Distributions ---
print("--- Generating and Saving Plots ---")

# Plot 1: Relative Velocity
plt.figure(figsize=(10, 6))
plt.hist(data['relative_velocity_kph'], bins=40, color='dodgerblue', edgecolor='black')
plt.title('Distribution of Relative Velocity', fontsize=16)
plt.xlabel('Relative Velocity (kilometers per hour)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
velocity_plot_filename = 'velocity_distribution.png'
plt.savefig(velocity_plot_filename)
plt.close()
print(f"✅ Saved velocity distribution plot to '{velocity_plot_filename}'")

# Plot 2: Estimated Minimum Diameter
plt.figure(figsize=(10, 6))
plt.hist(data['estimated_diameter_min_m'], bins=40, color='limegreen', edgecolor='black')
plt.title('Distribution of Estimated Minimum Diameter', fontsize=16)
plt.xlabel('Estimated Minimum Diameter (meters)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
min_diameter_plot_filename = 'min_diameter_distribution.png'
plt.savefig(min_diameter_plot_filename)
plt.close()
print(f"✅ Saved minimum diameter distribution plot to '{min_diameter_plot_filename}'")

# Plot 3: Estimated Maximum Diameter
plt.figure(figsize=(10, 6))
plt.hist(data['estimated_diameter_max_m'], bins=40, color='tomato', edgecolor='black')
plt.title('Distribution of Estimated Maximum Diameter', fontsize=16)
plt.xlabel('Estimated Maximum Diameter (meters)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
max_diameter_plot_filename = 'max_diameter_distribution.png'
plt.savefig(max_diameter_plot_filename)
plt.close()
print(f"✅ Saved maximum diameter distribution plot to '{max_diameter_plot_filename}'")