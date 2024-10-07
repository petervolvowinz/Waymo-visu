# Created by PWINZELL at 9/6/24
import os
import sys
import json

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from simple_waymo_open_dataset_reader import scenario_pb2
from simple_waymo_open_dataset_reader import motion_utils


DIRPATH =  '../data/'
FILENAME = '../data/training.tfrecord-00014-of-01000'
FILENAME2 = 'gs://waymo_open_dataset_motion_v_1_2_1/uncompressed/scenario/training/training.tfrecord-00001-of-01000'

stats = []
statjsonfile =  "pedstats.json"


def check_file_exists(filename):
    return os.path.isfile(filename)



if check_file_exists(FILENAME):
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

# convert protobuf to json
ped_counter = 0

def plot_road_points(roads, ax):
    for road in roads:
        points = np.array([(p["x"], p["y"]) for p in road["points"]])
        ax.scatter(points[:, 0], points[:, 1], s=1)

def vehicle_plot(points,ax):
    ax.scatter(points[:, 0], points[:, 1], s=1, c='blue')


def pedestrian_plot(points,ax):
    ax.scatter(points[:, 0], points[:, 1], s=2, c='red')


def bicycle_plot(points,ax):
    ax.scatter(points[:, 0], points[:, 1], s=1, c='green')


def getDFfromScenario(objects):
    for object in objects:
        lastpos = object[""]
        points = np.array([(p["x"], p["y"]) for p in object["position"]])
        ru_type = object["type"]

def plot_object_points(objects,ax):
    for object in objects:
        points = np.array([(p["x"], p["y"]) for p in object["position"]])
        otype = object["type"]
        if otype=='vehicle':
            vehicle_plot(points,ax)
        elif otype=='pedestrian':
            pedestrian_plot(points,ax)
        elif otype=='bicycle':
            bicycle_plot(points,ax)

def traverse_directory(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.startswith('training'):
                scenario = getScenario(os.path.join(dirpath, filename))
                scenario_dict = motion_utils.waymo_to_scenario(scenario)

                data = scenario_dict['objects']
                fig, ax = plt.subplots(1, 1, figsize=(12, 12))
                plot_object_points(data, ax)



                ped_counter = 0
                for i in range(len(data)):
                    if data[i]['type'] == 'pedestrian':
                        ped_counter = ped_counter + 1
                stats.append({"filename":filename,"number of pedestrians":ped_counter})
        plt.show(config={'scrollZoom': True})

traverse_directory(DIRPATH)
with open(DIRPATH + statjsonfile, 'w') as json_file:
    json.dump(stats, json_file, indent=4)

print(f"Data has been written to {statjsonfile}")