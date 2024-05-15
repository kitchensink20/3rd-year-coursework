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
        tasks = TaskGenerator.generate_tasks()
    else:
        tasksCsvReader = TaskCSVReader()
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
        
    
if __name__ == '__main__':
    main()