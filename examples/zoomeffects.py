# Created by PWINZELL at 9/5/24
import matplotlib
matplotlib.use('macosx')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.widgets import Button


# Set up the figure and axis
fig, ax = plt.subplots()

# Enable interactive mode
plt.ion()

# Define the coordinates and sizes of the circles
x = np.random.rand(10) * 100
y = np.random.rand(10) * 100
radii = np.random.rand(10) * 5  # Radii in data units (e.g., meters)

# Plot each circle
circles = []
for (xi, yi, ri) in zip(x, y, radii):
    circle = Circle((xi, yi), ri, transform=ax.transData, edgecolor='blue', facecolor='lightblue', alpha=0.5)
    ax.add_patch(circle)
    circles.append(circle)



def plot_ego_vehicle(ego_vehicle):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()


# Function to adjust object size based on zoom level
def on_zoom(event):
    for circle in circles:
        # Get the original radius in data units
        original_radius = circle.get_radius()

        # Get the current axis limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Calculate the scale factor based on the axis limits
        scale_factor = np.mean([xlim[1] - xlim[0], ylim[1] - ylim[0]]) / 100

        # Adjust the radius to reflect constant real-world size
        scaled_radius = original_radius / scale_factor
        if scaled_radius > 1:
            circle.set_radius(original_radius / scale_factor)
        else:
            scaled_radius = 1

    fig.canvas.draw_idle()



# Connect the zoom event to the function
ax.callbacks.connect('xlim_changed', on_zoom)
ax.callbacks.connect('ylim_changed', on_zoom)


# Add a reset zoom button for convenience
def reset_zoom(event):
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    fig.canvas.draw_idle()
def on_zoom(event):
    for circle in circles:
        # Get the original radius in data units
        original_radius = circle.get_radius()

        # Get the current axis limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Calculate the scale factor based on the axis limits
        scale_factor = np.mean([xlim[1] - xlim[0], ylim[1] - ylim[0]]) / 100

        # Adjust the radius to reflect constant real-world size
        scaled_radius = original_radius / scale_factor
        if scaled_radius > 1:
            circle.set_radius(original_radius / scale_factor)
        else:
            scaled_radius = 1

    fig.canvas.draw_idle()


reset_ax = plt.axes([0.8, 0.05, 0.1, 0.075])
reset_button = Button(reset_ax, 'Reset Zoom')
reset_button.on_clicked(reset_zoom)

# Set initial axis limits
ax.set_xlim(0, 1000)
ax.set_ylim(0, 1000)

plt.ion
plt.gca().set_aspect('equal', adjustable='box')
plt.ioff()
plt.show()
print("Press any key to")
# Keep the plot open in interactive mode
#plt.ioff()
