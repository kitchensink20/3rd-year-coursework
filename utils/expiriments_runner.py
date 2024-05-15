import random
import time
from algorithms.genetic_algorithm_without_local_improvement import GeneticAlgorithmWithoutLocalImprovement  
from algorithms.genetic_algorithm_with_local_improvement import GeneticAlgorithmWithLocalImprovement 
from algorithms.greedy_algorithm import GreedyAlgorithm
from constants import *
from utils.task_csv_reader import TaskCSVReader
from utils.task_generator import TaskGenerator

## Мета експерименту: встановити кількість послідовних ітерацій 
# (впродовж яких не змінюється рекордне значення ЦФ), після якої 
# слід зупиняти генетичний алгоритм без локального покращення.
def run_iteration_experiment_1(tasks, k_values=K_EXPIREMENT_VALUES, iterations=DEFAULT_EXPERIMENT_ITERATION_NUM, m=DEFAULT_WORKERS_NUM):
    n = len(tasks)
    results = {k: 0 for k in k_values}

    for i in range(1, iterations + 1):
        for k in k_values:
            ga = GeneticAlgorithmWithoutLocalImprovement(tasks, n, m, k=k) 
            best_schedule, best_fitness = ga.run()
            
            results[k] += best_fitness

    average_results = {k: results[k] / iterations for k in k_values}
    
    return average_results

# Мета експерименту: дослідити вплив розміру популяції на ефективність 
# та точність генетичного алгоритму з локальним покращенням.
def run_population_experiment_2(tasks, g_values=G_EXPIRIMENT_VALUES, iterations=DEFAULT_EXPERIMENT_ITERATION_NUM):
    n = len(tasks)
    fitness_results = {g: 0 for g in g_values}
    time_results = {g: 0 for g in g_values}

    for i in range(1, iterations + 1):
        for g in g_values:
            start_time = time.time()
            ga = GeneticAlgorithmWithLocalImprovement(tasks, n, m=DEFAULT_WORKERS_NUM, L=g) 
            best_schedule, best_fitness = ga.run()
            end_time = time.time()
            
            fitness_results[g] += best_fitness
            time_results[g] += (end_time - start_time)

    average_fitness_results = {g: fitness_results[g] / iterations for g in g_values}
    average_time_results = {g: time_results[g] / iterations for g in g_values}
    
    return average_fitness_results, average_time_results

# Метою проведення експериментів є визначення того, як розмірність 
# задачі впливає на час роботи і значення ЦФ розроблених алгоритмів.
def run_dimension_experiment_3(n_values=N_EXPIRIMENT_VALUES, m=DEFAULT_WORKERS_NUM, iterations=DEFAULT_ITERATION_NUM):
    time_results = {n: {'A1': 0, 'A2': 0, 'A3': 0} for n in n_values}
    fitness_results = {n: {'A1': 0, 'A2': 0, 'A3': 0} for n in n_values}

    for n in n_values:
        for i in range(1, iterations + 1):
            taskGenerator = TaskGenerator(n, m)
            generatedTasks = taskGenerator.generate_tasks()

            # A1 
            start_time = time.time()
            a1 = GreedyAlgorithm(n, m, generatedTasks)  
            _, a1_fitness = a1.maximize_income()
            end_time = time.time()
            time_results[n]['A1'] += (end_time - start_time)
            fitness_results[n]['A1'] += a1_fitness
            
            # A2 
            start_time = time.time()
            a2 = GeneticAlgorithmWithoutLocalImprovement(generatedTasks, n, m)  
            _, a2_fitness = a2.run()
            end_time = time.time()
            time_results[n]['A2'] += (end_time - start_time)
            fitness_results[n]['A2'] += a2_fitness
            
            # A3 
            start_time = time.time()
            a3 = GeneticAlgorithmWithLocalImprovement(generatedTasks, n, m)  
            _, a3_fitness = a3.run()
            end_time = time.time()
            time_results[n]['A3'] += (end_time - start_time)
            fitness_results[n]['A3'] += a3_fitness

    # Вирахуємо середній час виконання
    average_time_results = {n: {alg: round(time_results[n][alg]) / iterations for alg in time_results[n]} for n in n_values}
    average_fitness_results = {n: {alg: fitness_results[n][alg] / iterations for alg in fitness_results[n]} for n in n_values}
    
    return average_time_results, average_fitness_results