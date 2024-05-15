import argparse
import os
from constants import *
from utils.expiriments_runner import *
from utils.task_generator import TaskGenerator
from utils.expiriments_runner import TaskCSVReader

def is_a_file(path):
    if os.path.exists(path) and os.path.isfile(path):
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--experimentId', type=int, required=True, help='Id of the experiment to perform.')
    parser.add_argument('--dataPath', type=str, help='Path to the csv file with task data.')

    args = parser.parse_args()

    experiment_id = args.experimentId
    data_path = args.dataPath

    if data_path == 'default':
        data_path = CSV_FILE_PATH
    elif data_path and not is_a_file(data_path):
        print(f"The path '{data_path}' does not exist or it is not a file.")
        return

    tasks = []
    if not data_path:
        taskGenerator = TaskGenerator(n=DEFAULT_WORKERS_NUM, m=DEFAULT_TASKS_NUM)
        tasks = taskGenerator.generate_tasks()
    else:
        tasks = TaskCSVReader.read_tasks(data_path)

    if experiment_id > 3 or experiment_id < 1:
        print('Entered expiriment id does not exist.')
        return
    elif experiment_id == 1:
        print('Starting experiment... \n')
        average_results = run_iteration_experiment_1(tasks)
        print("Average fitness values for each k:")
        for k, avg_fitness in average_results.items():
            print(f"k = {k}: Average Fitness = {avg_fitness}")
    elif experiment_id == 2:
        print('Starting experiment... \n')
        average_fitness_results, average_time_results = run_population_experiment_2(tasks)
        print("Average fitness values for each population size:")
        for g, avg_fitness in average_fitness_results.items():
            print(f"Population size = {g}: Average Fitness = {avg_fitness}, ")
            
        print("\nAverage execution times for each population size:")
        for g, avg_time in average_time_results.items():
            print(f"Population size = {g}: Average Time = {avg_time} seconds")
    elif experiment_id == 3:
        print('Starting experiment... \n')
        average_time_results, average_fitness_results = run_dimension_experiment_3(N_EXPIRIMENT_VALUES, DEFAULT_WORKERS_NUM, DEFAULT_ITERATION_NUM)

        print("Average execution times for each algorithm and task size (rounded to nearest second):")
        for n, times in average_time_results.items():
            print(f"Task size = {n}:")
            for alg, avg_time in times.items():
                print(f"  {alg}: Average Time = {avg_time} seconds")

        print("\nAverage fitness values for each algorithm and task size:")
        for n, fitness in average_fitness_results.items():
            print(f"Task size = {n}:")
            for alg, avg_fitness in fitness.items():
                print(f"  {alg}: Average Fitness = {avg_fitness}")

if __name__ == '__main__':
    main()