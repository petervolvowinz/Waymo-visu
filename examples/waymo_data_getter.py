# Created by PWINZELL at 9/5/24
import os
import sys
from simple_waymo_open_dataset_reader import scenario_pb2
from simple_waymo_open_dataset_reader import motion_utils
import tensorflow as tf
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle


DIRPATH = "../data/"
FILEPATH = "../data/training.tfrecord-00014-of-01000"

class WaymoDataGetter:
    center_x = 0.0
    center_y = 0.0
    def __init__(self):
        pass
    def get_track_indeces(self,motion_scenario_dict,useAll = False):
        if useAll == False:
            return motion_scenario_dict['tracks_to_predict']
        else:
            return list(range(len(motion_scenario_dict['objects'])))


    def get_objects(self,motion_scenario_dict):
        return motion_scenario_dict['objects']
    def get_ego_vehicle(self,motion_scenario_dict):
        return motion_scenario_dict['sdc_track_index']
    def get_roads(self,motion_scenario_dict):
        return motion_scenario_dict['roads']
    def get_object_data(self,objects,index,attribute):
        return objects[index][attribute]

    min_x = sys.float_info.max
    min_y = sys.float_info.max
    max_x = -sys.float_info.max
    max_y = -sys.float_info.max

    def setCenterXY(self):
        self.center_x = self.min_x + ((self.max_x-self.min_x) / 2)
        self.center_y = self.min_y + ((self.max_y-self.min_y) / 2)

    def get_vehicle_rectangles_in_meters(self,vehicle,ax):
        rectangles = []
        vehicle_width = vehicle['width']
        vehicle_length = vehicle['length']
        index = 0
        for p in vehicle['position']:
            x = p["x"]
            y = p["y"]
            heading = vehicle["heading"][index]
            if x < self.min_x:
                self.min_x = x
            if x > self.max_x:
                self.max_x = x
            if y < self.min_y:
                self.min_y = y
            if y > self.max_y:
                self.max_y = y
            angle = 90 + heading # vehicle is already 90 degrees rotated from xaxis.
            newrect = Rectangle((x,y),vehicle_width,vehicle_length,angle=angle,
                                transform=ax.transData,edgecolor='blue',facecolor='lightblue',linewidth=1,alpha=0.1)
            rectangles.append(newrect)
            index = index + 1
        self.setCenterXY()
        return rectangles,self.center_x,self.center_y

    def get_pedestrian_circles_in_meters(self,pede,ax):
        circles = []
        pede_width = pede['width']
        pede_height = pede['length']
        index = 0
        for p in pede['position']:
            x = p["x"]
            y = p["y"]
            newcirc = Circle((x, y),pede_width,
                                transform=ax.transData, edgecolor='red', facecolor='red', linewidth=1, alpha=0.6)
            circles.append(newcirc)
        return circles

    def get_cycle_rectangles_in_meters(self,bicycle,ax):
        rectangles = []
        vehicle_width = bicycle['width']
        vehicle_length = bicycle['length']
        index = 0
        for p in bicycle['position']:
            x = p["x"]
            y = p["y"]
            heading = bicycle["heading"][index]
            angle = 90 + heading # vehicle is already 90 degrees rotated from xaxis.
            newrect = Rectangle((x,y),vehicle_width,vehicle_length,angle=angle,
                                transform=ax.transData,edgecolor='green',facecolor='green',linewidth=1,alpha=0.5)
            rectangles.append(newrect)
            index = index + 1
        return rectangles


def getScenario(filename):
    dataset = tf.data.TFRecordDataset(filename, compression_type="")
    tensordata = next(iter(dataset))
    # parse scenario protobuf
    scenario = scenario_pb2.Scenario()
    scenario.ParseFromString(bytes(tensordata.numpy()))
    return scenario
def get_waymo_data_as_dict(scenario):
    return motion_utils.waymo_to_scenario(scenario)