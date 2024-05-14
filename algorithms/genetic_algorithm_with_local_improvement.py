import random
from ..task import Task

class GeneticAlgorithmWithLocalImprovement:
    def __init__(self, m, tasks, K, L, q):
        """
        Ініціалізація вхідних даних та параметрів генетичного алгоритму
        m: кількість машин
        tasks: список об'єктів Task
        K: кількість ітерацій без покращення результату
        L: кількість осіб в популяції
        q: ймовірність мутації
        """
        self.m = m
        self.tasks = tasks
        self.K = K
        self.L = L
        self.q = q

    def initialize_population(self):
        population = []
        for _ in range(self.L):
            individual = list(range(len(self.tasks)))
            random.shuffle(individual)
            population.append(individual)
        return population

    def fitness(self, individual):
        F = [0] * self.m
        total_income = 0
        for i in individual:
            task = self.tasks[i]
            j = min(range(self.m), key=lambda x: F[x])
            if F[j] + task.duration <= task.deadline:
                F[j] += task.duration
                total_income += task.income
        return total_income

    def select_parents(self, population, fitness_scores):
        selected = random.choices(population, weights=fitness_scores, k=2)
        return selected

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + [gene for gene in parent2 if gene not in parent1[:point]]
        child2 = parent2[:point] + [gene for gene in parent1 if gene not in parent2[:point]]
        return child1, child2

    def mutate(self, individual):
        if random.random() < self.q:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]

    def local_improvement(self, individual):
        # Сортувати задачі в розкладі за зростанням дедлайнів
        sorted_individual = sorted(individual, key=lambda i: self.tasks[i].deadline)
        return sorted_individual

    def run(self):
        population = self.initialize_population()
        fitness_scores = [self.fitness(individual) for individual in population]
        best_solution = max(population, key=self.fitness)
        best_score = self.fitness(best_solution)

        no_improvement_count = 0
        while no_improvement_count < self.K:
            new_population = []
            for _ in range(self.L // 2):
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1)
                self.mutate(child2)
                child1 = self.local_improvement(child1)
                child2 = self.local_improvement(child2)
                new_population.extend([child1, child2])

            population = new_population
            fitness_scores = [self.fitness(individual) for individual in population]
            current_best_solution = max(population, key=self.fitness)
            current_best_score = self.fitness(current_best_solution)

            if current_best_score > best_score:
                best_solution = current_best_solution
                best_score = current_best_score
                no_improvement_count = 0
            else:
                no_improvement_count += 1

        return best_solution, best_score

# Приклад використання класу GeneticAlgorithmWithLocalImprovement
tasks = [
    Task(1, 100, 2, 3),
    Task(2, 200, 4, 5),
    Task(3, 150, 3, 4),
    Task(4, 120, 1, 3),
    Task(5, 180, 2, 5)
]

K = 10000  # кількість ітерацій без покращення результату
L = 100   # кількість осіб в популяції
q = 0.1  # ймовірність мутації

algorithm = GeneticAlgorithmWithLocalImprovement(3, tasks, K, L, q)
best_solution, best_score = algorithm.run()

print("Найкращий розклад робіт:", best_solution)
print("Загальний дохід від виконаних робіт:", best_score)
