import random
from ..task import Task

class TaskGenerator:
    def __init__(self, n, max_income, max_duration, max_deadline):
        """
        Ініціалізація параметрів генератора задач
        n: кількість задач
        max_income: максимальний дохід від задачі
        max_duration: максимальна тривалість задачі
        max_deadline: максимальний директивний строк
        """
        self.n = n
        self.max_income = max_income
        self.max_duration = max_duration
        self.max_deadline = max_deadline

    def generate_tasks(self):
        tasks = []
        for i in range(1, self.n + 1):
            income = random.randint(1, self.max_income)
            duration = random.randint(1, self.max_duration)
            deadline = random.randint(duration, self.max_deadline)  # дедлайн має бути не менше тривалості
            tasks.append(Task(i, income, duration, deadline))
        return tasks
