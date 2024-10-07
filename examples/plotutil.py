

import numpy as np
import plotly.graph_objects as go

def vehicle_plot(points,ax):
    ax.scatter(points[:, 0], points[:, 1], size=1, color='blue')


def pedestrian_plot(points,ax):
    ax.scatter(points[:, 0], points[:, 1], size=2, color='red')


def bicycle_plot(points,ax):
    ax.scatter(points[:, 0], points[:, 1], size=1, color='green')



def plot_object_points(objects,ax):
    for object in objects:
        points = np.array([(p["x"], p["y"]) for p in object["position"]])
        otype = object["type"]
        if otype=='vehicle':
            print("vehicle")
            #vehicle_plot(points,ax)
        elif otype=='pedestrian':
            pedestrian_plot(points,ax)
        elif otype=='bicycle':
            bicycle_plot(points,ax)

def getVehicleGraphics():
    return dict(size=2,color='green',line = dict(width=1,color='darkblue'))

def getPedestrianGraphics():
    return dict(size=1, color='red', line=dict(width=1, color='red'))

def get_data_points_forPlotly(objects,fig):
    for object in objects:
        ru_type = object["type"]
        x_vals = [point['x'] for point in object["position"] if point['x'] != -1]
        y_vals = [point['y'] for point in object["position"] if point['y'] != -1]
        x_array = np.array(x_vals)
        y_array = np.array(y_vals)
        if ru_type == 'vehicle':
            print("...")
           # fig.add_trace(go.Scatter(x=x_array, y=y_array,
                                   # mode='markers',marker=getVehicleGraphics()))
        elif ru_type == 'pedestrian':
            fig.add_trace(go.Scatter(x=x_array, y=y_array,
                                    mode='markers',marker=getPedestrianGraphics()))
        elif ru_type == 'bicycle':
            fig.add_trace(go.Scatter(x=x_array, y=y_array,
                                    mode='markers'))
    return fig

def get_data_points_plotwaymo_vehicle(objects,fig,waymo_index):
    waymo= objects[waymo_index]
    x_vals = [point['x'] for point in waymo["position"]]
    y_vals = [point['y'] for point in waymo["position"]]
    x_array = np.array(x_vals)
    y_array = np.array(y_vals)
    fig.add_trace(go.Scatter(x=x_array, y=y_array,
                             mode='markers', marker=getVehicleGraphics()))
    return fig