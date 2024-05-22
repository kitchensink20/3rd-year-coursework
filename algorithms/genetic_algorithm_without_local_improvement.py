import random
from copy import deepcopy
from constants import *

class GeneticAlgorithmWithoutLocalImprovement:
    def __init__(self, tasks, n, m, k=DEFAULT_ITERATION_NUM, L=DEFAULT_POPULATION_AMOUNT, q=DEFAULT_MUTATION_CHANCE):
        self.n = n  # кількість робіт
        self.m = m  # кількість машин
        self.k = k  # умова завершення
        self.L = L  # кількість осіб в популяції
        self.q = q  # ймовірність мутації
        self.tasks = tasks # масив задач

    def fitness(self, schedule):
        """Розрахуємо ефективність розкладу."""
        total_income = 0
        for machine_schedule in schedule:
            current_time = 0
            for task in machine_schedule:
                if current_time + task.duration <= task.deadline:
                    current_time += task.duration
                    total_income += task.income
        return total_income

    def initialize_population(self):
        """Сгенеруємо початкову популяцію розкладів."""
        population = []
        for _ in range(self.L):
            schedule = [[] for _ in range(self.m)]
            tasks = deepcopy(self.tasks)
            random.shuffle(tasks)
            for task in tasks:
                machine = random.randint(0, self.m - 1)
                schedule[machine].append(task)
            population.append(schedule)
        return population

    def select_parents(self, population, fitnesses):
        """Оберемо батьків для кросовера на основі їхньої ефективності."""
        total_fitness = sum(fitnesses)
        probabilities = [fitness / total_fitness for fitness in fitnesses]
        parents = random.choices(population, weights=probabilities, k=2)
        return parents

    def crossover(self, parent1, parent2):
        """Виконаємо кросовер між двома батьками для створення нащадків."""
        crossover_point = random.randint(0, self.n - 1)
        child1 = deepcopy(parent1[:crossover_point] + parent2[crossover_point:])
        child2 = deepcopy(parent2[:crossover_point] + parent1[crossover_point:])
        return child1, child2

    def mutate(self, schedule):
        """Мутуємо розклад, помінявши місцями дві задачі між машинами."""
        if random.random() < self.q:
            machine1, machine2 = random.sample(range(self.m), 2)
            if schedule[machine1] and schedule[machine2]:
                task1, task2 = random.choice(schedule[machine1]), random.choice(schedule[machine2])
                schedule[machine1].remove(task1)
                schedule[machine2].remove(task2)
                schedule[machine1].append(task2)
                schedule[machine2].append(task1)

    def run(self):
        """Запустимо генетичний алгоритм без локального покращення."""
        population = self.initialize_population()
        fitnesses = [self.fitness(schedule) for schedule in population]
        best_schedule = deepcopy(population[fitnesses.index(max(fitnesses))])
        best_fitness = max(fitnesses)
        generations = 0

        while generations < self.k:
            new_population = []
            for _ in range(self.L // 2):
                parent1, parent2 = self.select_parents(population, fitnesses)
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1)
                self.mutate(child2)
                new_population.extend([child1, child2])
            
            population = new_population
            fitnesses = [self.fitness(schedule) for schedule in population]
            current_best_fitness = max(fitnesses)
            current_best_schedule = deepcopy(population[fitnesses.index(current_best_fitness)])

            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_schedule = current_best_schedule
                generations = 0 
            else:
                generations += 1

        final_best_schedule = []
        final_bf = 0
        for bs in best_schedule:
            worker_bs = []
            passed_time = 0
            for task in bs:
                if task.duration + passed_time <= task.deadline:
                    passed_time = passed_time + task.duration
                    worker_bs.append(task)
                    final_bf = final_bf + task.income
                else:
                    break
            final_best_schedule.append(worker_bs)

        return final_best_schedule, final_bf
