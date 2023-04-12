
import os
import sys
print(sys.path)

import flymaster2.core.path_planning.optimization_algs as opt_algs
import flymaster2.core.path_planning.path_planning_utils as ut
import flymaster2.core.path_planning.fitness_funcs as fit

#waypoints = ut.gen_rand_waypoints(10)
waypoints= [
        {
          "latitude": 39.15516900,
          "longitude": -84.78777050,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15485280,
          "longitude": -84.78771150,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15452840,
          "longitude": -84.78814070,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15465320,
          "longitude": -84.78740570,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15437030,
          "longitude": -84.78754520,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15385450,
          "longitude": -84.78784020,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15395020,
          "longitude": -84.78866100,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15425800,
          "longitude": -84.78805480,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15406660,
          "longitude": -84.78721800,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15351750,
          "longitude": -84.78780810,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15339270,
          "longitude": -84.78873610,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15374220,
          "longitude": -84.78905800,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15372550,
          "longitude": -84.78862880,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15331370,
          "longitude": -84.78814600,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15354660,
          "longitude": -84.78714820,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15420390,
          "longitude": -84.78693370,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15427880,
          "longitude": -84.78740570,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15343020,
          "longitude": -84.78926180,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15424970,
          "longitude": -84.78853760,
          "altitude_agl": 30.0
        },
        {
          "latitude": 39.15367560,
          "longitude": -84.78820500,
          "altitude_agl": 30.0
        }
      ]

waypoints = ut.gen_rand_waypoints(8)
# x=genalg.ga(waypoints,[])
# x.init_ga()
# x.run_ga()
def printSolution(sol):
    print(sol)
    print(fit.order_solution(sol))
    print(fit.basic_distance(waypoints)(sol,0))
    print()

""" ga = opt_algs.GeneticAlgorithm(waypoints,[],fit.basic_distance(waypoints))
ga.init_ga()
ga_sol = ga.run_ga()
print(ga_sol)
printSolution(ga_sol[0]) """

if __name__ == '__main__':
  func = fit.fitness_functions(waypoints,[]).basic_distance
  fit_funcs = fit.fitness_functions(waypoints, [])
  bfa = opt_algs.BruteForceAlgorithm(waypoints,[],fit_funcs.basic_distance)
  bfa_sol = bfa.run_multi_bfa()
  print(bfa_sol)
  printSolution(bfa_sol)
