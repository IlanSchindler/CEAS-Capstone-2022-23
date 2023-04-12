import flymaster2.core.path_planning.path_planning_utils as path_planning_utils
import numpy


def order_solution(inSol): 
    order = [[0, 0]] + [[inSol[i], i + 1] for i in range(len(inSol))]
    order.sort(key=lambda x: x[0])
    return [o[1] for o in order]

class fitness_functions:
    def __init__(self, waypoints, obstacles):
        print(waypoints)
        print(len(waypoints))
        self.waypoints = waypoints
        self.obstacles = obstacles
        num_waypoints = len(self.waypoints)
        self.obstacle_interference = [
            [False for x in range(num_waypoints)]
            for y in range(num_waypoints)
        ]
        for i in range(num_waypoints):
            for j in range(i+1, num_waypoints):
                for k in range(len(obstacles)):
                    w1 = self.waypoints[i]
                    w1a = numpy.array([w1["latitude"],w1["longitude"]])
                    w2 = self.waypoints[j]
                    w2a = numpy.array([w2["latitude"],w2["longitude"]])
                    o = obstacles[k]
                    result = o.segment_intersects(w1a,w2a)
                    self.obstacle_interference[i][j] = result
                    self.obstacle_interference[j][i] = result
        print(self.obstacle_interference)

    def basic_distance(self, inSol, solId):
        totalDist = 0
        pointOrder = order_solution(inSol)
        for i in range(len(pointOrder)):
            totalDist += path_planning_utils.calc_3d_dist(
                self.waypoints[pointOrder[i - 1]], self.waypoints[pointOrder[i]]
            )
        return totalDist * -1
    
    def avoid_obstacles(self, inSol, solId):
        totalDist = 0
        pointOrder = order_solution(inSol)
        for i in range(len(pointOrder)):
            if(self.obstacle_interference[i-1][i]):
                totalDist += 1000
            else:
                totalDist += path_planning_utils.calc_3d_dist(
                    self.waypoints[pointOrder[i-1]],
                    self.waypoints[pointOrder[i]]
                )
        return totalDist * -1