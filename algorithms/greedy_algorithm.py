from ..task import Task

class GreedyAlgorithm:
    def __init__(self, m, tasks):
        """
        Ініціалізація вхідних даних
        m: кількість машин
        tasks: список об'єктів Task
        """
        self.m = m
        self.tasks = tasks
        self.F = [0] * m  # Поточний загальний час на машині m
        self.S = [[] for _ in range(m)]  # Множина розкладів виконання робіт для кожної машини
        self.Z = 0  # Цільова функція, загальний дохід від виконаних робіт

    def maximize_income(self):
        # Упорядкувати вектор робіт за зменшенням c_i/p_i
        self.tasks.sort(key=lambda task: task.income / task.duration, reverse=True)

        # Для кожної роботи в self.tasks
        for task in self.tasks:
            # Знайти машину j з мінімальним F_j
            j = min(range(self.m), key=lambda x: self.F[x])

            # Перевірка умови
            if self.F[j] + task.duration <= task.deadline:
                # Додати роботу до розкладу S_j на машині j
                self.S[j].append(task)
                # Збільшити поточний загальний час виконання роботи F_j на машині j
                self.F[j] += task.duration
                # Додати прибуток від виконання роботи в загальний дохід Z
                self.Z += task.income

        return self.S, self.Z

# Приклад використання класу GreedyAlgorithm з Task
tasks = [
    Task(1, 100, 2, 3),
    Task(2, 200, 4, 5),
    Task(3, 150, 3, 4),
    Task(4, 120, 1, 3),
    Task(5, 180, 2, 5)
]

algorithm = GreedyAlgorithm(3, tasks)
S, Z = algorithm.maximize_income()

# Вивести результат
print("Розклад робіт для кожної машини:")
for i, machine_tasks in enumerate(S):
    print(f"Машина {i + 1}: {machine_tasks}")
print("Загальний дохід від виконаних робіт:", Z)
