import pygad
import flymaster2.core.path_planning.fitness_funcs as fitness_funcs
import itertools
import sys
import random

last_fitness = 0


class GeneticAlgorithm:
    waypoint_list = []
    obstacle_interference = [[]]
    num_waypoints = 0
    fitness_func = None

    ga_inst = None


    def __init__(self, waypoints, obstacles, fitness):  # ,fitness):
        self.waypoint_list = waypoints
        self.num_waypoints = len(self.waypoint_list)
        self.fitness_func = fitness

    def init_ga(self, crossover_probability=0.5, mutation_probability=0.1, num_generations=500, num_parents_mating=10, sol_per_pop = 100):
        self.ga_inst = pygad.GA(
            gene_type=int,
            gene_space=[i for i in range(1, self.num_waypoints)],
            num_genes=self.num_waypoints - 1,
            allow_duplicate_genes=False,
            parent_selection_type="rank",
            crossover_type=self.crossover_func,
            mutation_type=self.mutation_func,
            fitness_func=self.fitness_func,
            on_generation=self.on_generation,
            on_crossover=self.on_crossover,
            crossover_probability=crossover_probability,
            mutation_probability=mutation_probability,
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            sol_per_pop=sol_per_pop
        )

    def run_ga(self):
        self.ga_inst.run()
        return self.ga_inst.best_solution()
    
    def crossover_func(self,parents, offspring_size, ga):
        offspring = ga.uniform_crossover(parents, offspring_size)
        for i in range(offspring.shape[0]):
            offspring[i], _, _ = ga.solve_duplicate_genes_by_space(
                solution=offspring[i], gene_type=ga.gene_type, num_trials=1
            )
        return offspring
    
    def mutation_func(self,offspring, ga):
        for i in range(offspring.shape[0]):
            kid = offspring[i]
            while random.random() < ga.mutation_probability:
                genes = random.sample(range(len(kid)), 2)
                temp = kid[genes[0]]
                kid[genes[0]] = kid[genes[1]]
                kid[genes[1]] = temp
            offspring[i] = kid
        return offspring
    
    def on_generation(self,ga_instance):
        pass

    def on_crossover(self, ga_instance, crossover):
        for i in range(len(ga_instance.last_generation_offspring_crossover)):
            (
                ga_instance.last_generation_offspring_crossover[i],
                _,
                _,
            ) = ga_instance.solve_duplicate_genes_by_space(
                solution=ga_instance.last_generation_offspring_crossover[i],
                gene_type=ga_instance.gene_type,
                num_trials=1,
            )


class BruteForceAlgorithm:
    waypoint_list = []
    num_waypoints = 0
    obstacle_interference = [[]]
    fitness_func = None

    def __init__(self, waypoints, obstacles, fitness):
        self.waypoint_list = waypoints
        self.num_waypoints = len(self.waypoint_list)
        self.fitness_func = fitness

    def run_bfa(self):
        best_sol = []
        best_sol_fitness = -sys.maxsize - 1
        perm_points = list(range(1, self.num_waypoints))
        for sol in itertools.permutations(perm_points):
            fitness = self.fitness_func(sol, 0)
            # print(solId, fitness, sol)
            if fitness > best_sol_fitness:
                best_sol = sol
                best_sol_fitness = fitness
        return best_sol


    def publisher_process(self, q, it):
        print("Hello! I'm a publisher")
        for i in it:
            q.put(i,True)
        q.put(self.sentinal,True)

    def calculator_process(self, in_q, out_q):
        print("Wassup! I'm a calculator")
        local_best = []
        local_best_fit = -sys.maxsize-1
        for i in range(100):
            sol = in_q.get(True)
            if(sol == self.sentinal):
                in_q.put(self.sentinal,True)
                break
            fitness = self.fitness_func(sol,i)
            if fitness > local_best_fit:
                local_best = sol
                local_best_fit = fitness
        out_q.put([local_best,local_best_fit],True)
        print("Goodbye! I'm a dead calculator")
        
    def consolidator_process(self,q):
        print("Greetings! I'm a consolidator")
        best_sol = []
        best_fit = -sys.maxsize - 1
        while(True):
            sol = q.get(True)
            if(sol==self.sentinal):
                break
            if(sol[1] > best_fit):
                best_sol = sol[0]
                best_fit = sol[1]
        q.put([best_sol, best_fit])

    def run_multi_bfa(self):
        import multiprocessing
        self.sentinal = object()

        print("Creating Itterator")
        perm_points = list(range(1, self.num_waypoints))
        
        print("Creating Itterater Queue")
        itter_que = multiprocessing.Queue(50)
        print("Creating Result Queue")
        result_que = multiprocessing.Queue(100)
        print("Creating Pool")
        # pool = multiprocessing.Pool(10)

        print("Creating Publisher Process")
        publisher = multiprocessing.Process(target=self.publisher_process, args=(itter_que,itertools.permutations(perm_points),))
        print("Starting Publisher Process")
        publisher.start()

        print("Creating Consolidator")
        consolidator = multiprocessing.Process(target=self.consolidator_process,args=(result_que,))
        print("Starting Consolidator")
        consolidator.start()

        print("Starting Calculators in Pool")

        calc_pool = []
        calc_pool_limit = 5
        while(publisher.exitcode == None or len(calc_pool)>0):
            if(len(calc_pool) <calc_pool_limit and publisher.exitcode == None):
                print("Creating Calculator Process")
                p = multiprocessing.Process(target=self.calculator_process, args=(itter_que,result_que,))
                print("Starting Calculator Process")
                p.start()
                calc_pool.append(p)
            i=0
            while i < len(calc_pool):
                if(calc_pool[i].exitcode != None):
                    calc_pool[i].close()
                    calc_pool.remove(calc_pool[i])
                    i-=1 
                i+=1
        
        print("Itterator is empty. Waiting for calculations to end")

        result_que.put(self.sentinal,True)

        solution = result_que.get(True)

        print("Closing Processess")
        publisher.close()
        consolidator.close()

        return solution






