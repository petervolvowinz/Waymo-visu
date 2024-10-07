# Created by PWINZELL at 9/6/24
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('macosx')
from matplotlib.animation import FuncAnimation

# Create figure and axis
fig, ax = plt.subplots()

# Set the limits for the plot
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create a circle patch
circle = plt.Circle((0, 0), radius=0.5, color='blue')

# Add the circle to the axis
ax.add_patch(circle)

# Define the update function to animate the circle
def update(frame):
    # Update the center of the circle for each frame
    circle.set_center((frame, np.sin(frame) + 5))  # Moves along a sine wave
    return circle,

# Create the animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 100), interval=1000)
ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
# Show the animation
plt.show()
