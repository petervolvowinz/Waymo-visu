# Created by PWINZELL at 9/6/24
from matplotlib.animation import FuncAnimation

import waymo_data_getter
import waymo_data_getter as wdg
import matplotlib.pyplot as plt
import numpy as np

from simple_waymo_open_dataset_reader import motion_utils as mu

# either use allo objects or just the selected list of objects nearest to ego.
use_all_data_objects = True
def calculate_heading_angle(vx, vy):
    return np.arctan2(vy, vx) * 180 / np.pi
def deg2rad(deg):
    return deg * np.pi / 180
def getVehicle(index,ax,scen_dict,WDG)-> tuple[[],float,float]:
    veh = scen_dict['objects'][index]
    vehicle_rects,cX,cY = WDG.get_vehicle_rectangles_in_meters(veh,ax)

    return vehicle_rects,cX,cY

def getPedestrian(index,ax,scen_dict,WDG)->[]:
    pede = scen_dict['objects'][index]
    ped_circs = WDG.get_pedestrian_circles_in_meters(pede,ax)
    return ped_circs

def getCyclist(index,ax,scen_dict,WDG)->[]:
    cycle = scen_dict['objects'][index]
    cycle_rects = WDG.get_cycle_rectangles_in_meters(cycle, ax)

    return cycle_rects

class VehicleSceneData:
    def __init__(self,objectindex,ax,scene_dict,WDG, ego = False):
        self.rects,cX,cY = getVehicle(objectindex,ax,scene_dict,WDG)
        self.index = objectindex
        # self.vx =
        rect_data = self.rects[0]
        self.datapoints = len(self.rects)
        if ego == True:
            ax.set_xlim(cX - 60, cX + 60)
            ax.set_ylim(cY - 60, cY + 60)

            self.coneline_1, = ax.plot([],[],'g-',linewidth=1)
            self.coneline_2, = ax.plot([],[],'g-',linewidth=1)

            self.animation_rect = plt.Rectangle((rect_data.get_x(), rect_data.get_y()), rect_data.get_width(),
                                       rect_data.get_height(), angle=rect_data.get_angle(), edgecolor='blue',
                                       facecolor='lightblue', linewidth=1, alpha=1.0)
        else:
            self.animation_rect = plt.Rectangle((rect_data.get_x(), rect_data.get_y()), rect_data.get_width(),
                                       rect_data.get_height(), angle=rect_data.get_angle(), edgecolor='blue',
                                       facecolor='lightblue', linewidth=1, alpha=0.3)
        ax.add_patch(self.animation_rect)

class PedestrianSceneData:
    def __init__(self,objectindex,ax,scene_dict,WDG):
        self.circs = getPedestrian(objectindex,ax,scene_dict,WDG)
        self.index = objectindex
        circ_data = self.circs[0]
        self.datapoints = len(self.circs)
        x,y = circ_data.get_center()
        self.animation_circ = plt.Circle((x,y), circ_data.get_radius(),edgecolor='red',
                                       facecolor='red', linewidth=1, alpha=0.9)
        ax.add_patch(self.animation_circ)

class CyclistSceneData:
    def __init__(self, objectindex, ax, scene_dict, WDG):
        self.rects = getCyclist(objectindex, ax, scene_dict, WDG)
        self.index = objectindex
        rect_data = self.rects[0]
        self.datapoints = len(self.rects)
        self.animation_rect = self.animation_rect = plt.Rectangle((rect_data.get_x(), rect_data.get_y()), rect_data.get_width(),
                                       rect_data.get_height(), angle=rect_data.get_angle(), edgecolor='green',
                                       facecolor='green', linewidth=1, alpha=0.5)
        ax.add_patch(self.animation_rect)

class ScenarioAnimation:
    # Divide into vehicle and pedestrian scene
    vehicleSceneData = []
    pedestrianSceneData = []
    cyclistSceneData = []

    # The area of attention
    centerX = 0
    centerY = 0

    WDG = waymo_data_getter.WaymoDataGetter()
    def __init__(self,fig,ax):

        self.scen_dict = waymo_data_getter.get_waymo_data_as_dict(wdg.getScenario(wdg.FILEPATH))

        self.indexes = self.WDG.get_track_indeces(self.scen_dict,use_all_data_objects)
        self.ego_index = self.WDG.get_ego_vehicle(self.scen_dict)
        self.objects = self.WDG.get_objects(self.scen_dict)
        if use_all_data_objects == False:
            self.indexes = self.addPedestriansToIndexes(self.objects,self.indexes)
        self.roads = self.WDG.get_roads(self.scen_dict)
        self.fig = fig
        self.ax = ax

    def addPedestriansToIndexes(self, objects, indexes):
        for index,object in enumerate(objects):
            if (object['type'] == 'pedestrian') and (index not in indexes):
                indexes.append(index)
        return indexes

    def drawRoads(self):
        ft = mu.FeatureType
        for road in self.roads:
            roadtype = road['type']
            #oldx = road[0]['points']['x']
            #oldy = road[0]['points']['y']
            points = road['points']
            xvalues = [point['x'] for point in points]
            yvalues = [point['y'] for point in points]

            if roadtype == ft.ROAD_EDGE_BOUNDARY:
                self.ax.plot(xvalues, yvalues,color='black', linewidth=1, alpha=0.5)
            elif roadtype == ft.ROAD_EDGE_MEDIAN:
                self.ax.plot(xvalues,yvalues,color='black', linewidth=1, alpha=0.9)
            elif roadtype == ft.BIKE_LANE:
                self.ax.plot(xvalues, yvalues, color='blue', linewidth=1, alpha=0.5)
            elif roadtype == ft.CROSSWALK:
                self.ax.plot(xvalues, yvalues, color='gray', linewidth=2, alpha=0.2)
            elif roadtype == ft.DRIVEWAY:
                self.ax.plot(xvalues, yvalues, color='gray', linewidth=1, alpha=0.4)
            elif roadtype == ft.FREEWAY_LANE:
                self.ax.plot(xvalues, yvalues, color='gray', linewidth=1, alpha=0.3, linestyle='--')
            elif roadtype == ft.SURFACE_STREET_LANE:
                self.ax.plot(xvalues, yvalues, color='gray', linewidth=1, alpha=0.3, linestyle='--')
            elif roadtype == ft.BROKEN_DOUBLE_YELLOW_BOUNDARY:
                self.ax.plot(xvalues, yvalues, color='yellow', linewidth=2, alpha=0.8, linestyle='--')
            elif roadtype == ft.BROKEN_SINGLE_YELLOW_BOUNDARY:
                self.ax.plot(xvalues, yvalues, color='yellow', linewidth=1, alpha=0.8, linestyle='--')
            #elif roadtype == ft.

    def initCircle(self,objectindex,fig,ax):
        pedData = PedestrianSceneData(objectindex, ax, self.scen_dict, self.WDG)
        self.pedestrianSceneData.append(pedData)
    def initRect(self,objectindex,fig,ax,ego = False):
        vehSceneData = VehicleSceneData(objectindex,ax,self.scen_dict,self.WDG,ego)
        self.vehicleSceneData.append(vehSceneData)
    def initCrect(self,objectindex,fig,ax):
        cycleSceneData = CyclistSceneData(objectindex, ax, self.scen_dict, self.WDG)
        self.cyclistSceneData.append(cycleSceneData)

    def initAnimation(self):

        self.initRect(self.ego_index,self.fig,self.ax,True) # Add ego_vehicle
        for i,value in enumerate(self.indexes):
            if self.ego_index != value:
                object = self.objects[value]
                if object['type'] == 'vehicle':
                    self.initRect(value,self.fig,self.ax)
                elif object['type'] == 'pedestrian':
                    self.initCircle(value,self.fig,self.ax)
                elif object['type'] == 'cyclist':
                    self.initCrect(value,self.fig,self.ax)

    def getConeLines(self,angle,centerx,centery):
        heading_angle_rad = deg2rad(angle - 90)

        # Calculate the angles for ±45 degrees from the heading
        angle1 = heading_angle_rad + deg2rad(30)
        angle2 = heading_angle_rad - deg2rad(30)

        coneL = 20
        # Calculate the end points of the two lines
        x1, y1 = centerx + coneL * np.cos(angle1), centery + coneL * np.sin(angle1)
        x2, y2 = centerx + coneL * np.cos(angle2), centery + coneL * np.sin(angle2)

        return x1,y1,x2,y2

    def animate_vehicle_plot(self,index):
        rects = []
        lines = []
        for i, scene in enumerate(self.vehicleSceneData):
            rect = scene.animation_rect
            updatesrect = self.vehicleSceneData[i].rects[index]
            u_x = updatesrect.get_x()
            if u_x != -1:
                rect.set_xy((updatesrect.get_x(), updatesrect.get_y()))
                rect.set_angle(updatesrect.get_angle())
                rects.append(updatesrect)
                if scene.index == self.ego_index:
                    rel_x =  updatesrect.get_width() / 2
                    rel_y =  updatesrect.get_height() / 2
                    rad_heading = deg2rad(updatesrect.get_angle())

                    # rotation matrix
                    rx = rel_x * np.cos(rad_heading) - rel_y * np.sin(rad_heading)
                    ry = rel_x * np.sin(rad_heading) + rel_y * np.cos(rad_heading)

                    x1,y1,x2,y2 = self.getConeLines(updatesrect.get_angle(),updatesrect.get_x() + rx,updatesrect.get_y() + ry)

                    scene.coneline_1.set_data([updatesrect.get_x() + rx,x1],[updatesrect.get_y() + ry,y1])
                    scene.coneline_2.set_data([updatesrect.get_x() + rx,x2],[updatesrect.get_y() + ry,y2])

                    lines.append(scene.coneline_1)
                    lines.append(scene.coneline_2)
        circs = []
        for i, scene in enumerate(self.pedestrianSceneData):
            circ = scene.animation_circ
            updatescirc = self.pedestrianSceneData[i].circs[index]
            u_x,u_y = updatescirc.get_center()
            if u_x == -1:
                circ.set_facecolor('white')
                circ.set_edgecolor('white')
            else:
                circ.set_facecolor('red')
                circ.set_edgecolor('red')
            circ.set_center((u_x,u_y))
            circs.append(updatescirc)


        bikes = []
        for i, scene in enumerate(self.cyclistSceneData):
            rect = scene.animation_rect
            updatesrect = self.cyclistSceneData[i].rects[index]
            u_x = updatesrect.get_x()
            if u_x != -1:
                rect.set_xy((updatesrect.get_x(), updatesrect.get_y()))
                rect.set_angle(updatesrect.get_angle())
                bikes.append(updatesrect)

        return rects,circs,bikes,lines

    def animateScene(self):
        self.initAnimation()
        vehScene = self.vehicleSceneData[0]
        size = vehScene.datapoints
        self.drawRoads()
        return FuncAnimation(self.fig, self.animate_vehicle_plot, frames=size, interval=200,blit=False)
