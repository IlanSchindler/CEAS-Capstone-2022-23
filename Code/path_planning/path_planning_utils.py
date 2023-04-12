import math
import random
import numpy as np
from flymaster2.core.utils.CoordinateUtils import gps_distance_meters
from flymaster2.core.services import Logging


def calc_3d_dist(w1, w2):
    if "altitude_agl" in w1 and "altitude_agl" in w2:
        return math.sqrt(
            gps_distance_meters(
                w1["latitude"], w1["longitude"], w2["latitude"], w2["longitude"]
            )
            ** 2
            + (w2["altitude_agl"] - w1["altitude_agl"]) ** 2
        )
    else:
        return gps_distance_meters(
            w1["latitude"], w1["longitude"], w2["latitude"], w2["longitude"]
        )


def gen_rand_waypoints(n):
    waypoints = []
    lat = 39.152
    lon = -84.789
    altLow = 38
    altHigh = 53
    for i in range(n):
        w = {}
        w["latitude"] = random.uniform(lat, lat + 0.001)
        w["longitude"] = random.uniform(lon, lon + 0.001)
        w["altitude_agl"] = random.randrange(altLow, altHigh)
        w["name"] = "Waypoint " + str(i)
        waypoints.append(w)
    return waypoints


def avoid_obstacles(waypoints, obstacles):
    return waypoints


def handle_wpt_obst_intersection(waypoints, obstacles, obst_buff):
    removables = []
    for idx, waypoint in enumerate(waypoints):
        for obstacle in obstacles:
            if np.linalg.norm(obstacle.vector_to(
                np.asarray([waypoint["latitude"], waypoint["longitude"]])
            )) < obst_buff:
                Logging.info(
                    f"Removed waypoint at {[waypoint['latitude'], waypoint['longitude']]} because it was inside an obstacle"
                )
                removables.append(idx)
                break
    for index in sorted(removables, reverse=True):
        del waypoints[index]
    return waypoints
