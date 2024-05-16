import argparse
import os
from constants import *
from utils.expiriments_runner import *
from utils.task_generator import TaskGenerator
from utils.expiriments_runner import TaskCSVReader

def is_valid_csv(path):
    if not os.path.isfile(path):
        return False
    
    if not path.endswith('.csv'):
        return False
    
    required_columns = ['id', 'income', 'duration', 'deadline']
    
    try:
        with open(path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            
            if not all(column in reader.fieldnames for column in required_columns):
                return False
            
            for row in reader:
                try:
                    id = int(row['id'])
                    income = int(row['income'])
                    duration = int(row['duration'])
                    deadline = int(row['deadline'])
                except ValueError:
                    return False
                
            return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def display_schedules_and_income(generated_schedule, total_income):
    print('\nРезультуючий розклад:')
    for i, machine in enumerate(generated_schedule):
        print(f"Завдання для машини {i + 1}: {machine}")
    print(f"\nЗагальний дохід: {total_income}")


def display_all_tasks(tasks):
    for task in tasks:
        print(task)


def main():
    print('1 - Згенерувати розклад за допомогою жадібного алгоритму(А1) для досягнення максимального доходу')
    print('2 - Згенерувати розклад за допомогою генетичного алгоритму без локального покращення(А2) для досягнення максимального доходу')
    print('3 - Згенерувати розклад за допомогою генетичного алгоритму з локальним покращенням(А3) для досягнення максимального доходу')
    print('4 - Провести екперимент для визначення оптимальної кількості послідовних ітерацій, протягом яких не змінюється рекордне значення ЦФ з використанням алгоритму А2')
    print('5 - Провести екперимент для дослідження впливу розміру популяції на ефективність та точність алгоритму А3')
    print('6 - Провести екперимент для дослідження, як розмірність задачі впливає на час роботи і значення ЦФ для трьох реалізованих алгоритмів')
   
    choice = input('Оберіть одну з запропонованих опцій в меню:\t')

    if not choice.isnumeric() or int(choice) <= 0 or int(choice) > 6:
        print('Введено некоректну опцію!')
        return
    
    print('\n1 - Зчитати дані з файлу')
    print('2 - Згенерувати дані автоматично')
    print('***У випадку обрання пункту 6 в меню, задачі генеруються автоматично за замовчуванням.')
    tasks_generation_type = input('Оберіть одну з запропонованих опцій:\t')
    
    tasks = []
    if not tasks_generation_type.isnumeric() or (int(tasks_generation_type) != 1 and int(tasks_generation_type) != 2):
        print('Введено некоректну опцію!')
        return  
    elif int(tasks_generation_type) == 1:
        file_path = input('Введіть шлях до .csv файлу(enter для використання файлу за замовченням):\t')
        if file_path == '':
            file_path = CSV_FILE_PATH
        elif not is_valid_csv(file_path):
            print('Введено некоректний шлях!')
            return  
        tasks = TaskCSVReader.read_tasks(file_path)
    elif int(tasks_generation_type) == 2:
        n = input('Введіть кількість задач(min - 10, max - 100): \t')
        if not n.isnumeric() or int(n) < 5 or int(n) < 10 or int(n) > 100:
            return
        tasks = TaskGenerator.generate_tasks(n=int(n))

    print('\nБули зчитані/згенеровані наступні задачі:')
    display_all_tasks(tasks)

    if int(choice) == 1:
        greedy_algorithm = GreedyAlgorithm(len(tasks), DEFAULT_WORKERS_NUM, tasks)
        generated_schedule, total_income = greedy_algorithm.maximize_income()
        display_schedules_and_income(generated_schedule, total_income)
    elif int(choice) == 2:
        genetic_algorithm_without_local_improvement = GeneticAlgorithmWithoutLocalImprovement(tasks, len(tasks), DEFAULT_WORKERS_NUM)
        generated_schedule, total_income =  genetic_algorithm_without_local_improvement.run()
        display_schedules_and_income(generated_schedule, total_income)
    elif int(choice) == 3:
        genetic_algorithm_with_local_improvement = GeneticAlgorithmWithLocalImprovement(tasks, len(tasks), DEFAULT_WORKERS_NUM)
        generated_schedule, total_income =  genetic_algorithm_with_local_improvement.run()
        display_schedules_and_income(generated_schedule, total_income)
    elif int(choice) == 4:
        print('Початок експерименту... \n')
        average_results = run_iteration_experiment_1(tasks)
        print("Середні значення прибутку для кожного k:")
        for k, avg_fitness in average_results.items():
            print(f"k = {k}: Середній прибуток = {avg_fitness}")
    elif int(choice) == 5:
        print('Початок експерименту... \n')
        average_fitness_results, average_time_results = run_population_experiment_2(tasks)
        print("Середні значення прибутку для кожного розміру популяції:")
        for g, avg_fitness in average_fitness_results.items():
            print(f"Розмір популяції = {g}: Середній прибуток = {avg_fitness}, ")

        print("\nCередні часи виконання для кожного розміру популяції:")
        for g, avg_time in average_time_results.items():
           print(f"Розмір популяції = {g}: Середній час = {round(avg_time)} секунд")
    elif int(choice) == 6:
        print('Початок експерименту... \n')
        average_time_results, average_fitness_results = run_dimension_experiment_3(N_EXPIRIMENT_VALUES, DEFAULT_WORKERS_NUM, DEFAULT_ITERATION_NUM)

        print("Середні часи виконання для кожного алгоритму та розміру завдання (округлені до найближчої секунди):")
        for n, times in average_time_results.items():
            print(f"Розмір завдання = {n}:")
            for alg, avg_time in times.items():
                print(f"  {alg}: Середній час = {avg_time} секунд")

        print("\nСередні значення функції придатності для кожного алгоритму та розміру завдання:")
        for n, fitness in average_fitness_results.items():
            print(f"Розмір завдання = {n}:")
            for alg, avg_fitness in fitness.items():
                print(f"  {alg}: Середня придатність = {avg_fitness}")

if __name__ == '__main__':
    main()