# Created by PWINZELL at 9/5/24
import matplotlib
matplotlib.use('MacOSX') # choose according to our current work nev.
import matplotlib.pyplot as plt
import waymo_data_getter as wdg
import scenario_animation as SA
from pathlib import Path
waymo_data_getter = wdg.WaymoDataGetter()


# Set up the figure and axis
fig, ax = plt.subplots()
# Enable interactive mode
plt.ion()

# dont plot axis
ax.axis('off')

plt.ion
plt.gca().set_aspect('equal', adjustable='box')
plt.ioff()
plt.tight_layout()

sc_anim = SA.ScenarioAnimation(fig,ax)
animation = sc_anim.animateScene()

path_name = wdg.FILEPATH
if SA.use_all_data_objects == True:
    filename = Path(path_name).name + "_all.mp4"
else:
    filename = Path(path_name).name + ".mp4"

animation.save('../data/'+filename, fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()
print("Press any key to")



