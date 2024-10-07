import os
import sys
import tensorflow as tf

from examples import plotutil
from simple_waymo_open_dataset_reader import scenario_pb2
from simple_waymo_open_dataset_reader import motion_utils
import plotly.graph_objects as go


DIRPATH =  '../data/'
FILENAME = '../data/training.tfrecord-00014-of-01000'

def check_file_exists(filename):
    return os.path.isfile(filename)



if check_file_exists(DIRPATH+FILENAME):
    print("file path ok")
else:
    sys.exit("file does not exist " + FILENAME)


def getScenario(filename):
    dataset = tf.data.TFRecordDataset(filename, compression_type="")
    tensordata = next(iter(dataset))
    # parse scenario protobuf
    scenario = scenario_pb2.Scenario()
    scenario.ParseFromString(bytes(tensordata.numpy()))
    return scenario

scenario = getScenario(os.path.join(DIRPATH, FILENAME))
scenario_dict = motion_utils.waymo_to_scenario(scenario)
data = scenario_dict['objects']
sdc_track_index = scenario_dict['sdc_track_index']
fig = go.Figure()
fig = plotutil.get_data_points_forPlotly(data,fig)
fig = plotutil.get_data_points_plotwaymo_vehicle(data,fig,sdc_track_index)
fig.update_layout(
    title='Scatter Plot of Vehicles and pedestrians',  # Title of the figure
    title_font=dict(size=20, family='Arial', color='DarkBlue'),  # An optional title font customization
    xaxis_title='X is East',  # X-axis label
    yaxis_title='Y is North',  # Y-axis label
    width=800,  # Width of the figure
    height=600,  # Height of the figure
    paper_bgcolor='LightGray',  # Background color of the paper (outside the plotting area)
    plot_bgcolor='White',  # Background color of the plotting area
    margin=dict(l=40, r=40, t=40, b=40),  # Margins around the plot
)
fig.show(config={'scrollZoom': True})
