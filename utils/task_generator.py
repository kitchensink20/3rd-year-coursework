import random
from task import Task
from constants import *

class TaskGenerator:
    def __init__(self, n, m):
        self.n = n  # кількість робіт
        self.m = m  # кількість машин
        self.tasks = [] # масив результуючих задач

    def generate_tasks(self):
        for i in range(1, self.n + 1):
            income = random.randint(MIN_TASK_INCOME, MAX_TASK_INCOME)
            deadline = random.randint(MIN_TASK_DEADLINE, MAX_TASK_DEADLINE)
            duration = random.randint(MIN_TASK_DURATION, deadline)
            task = Task(i, income, duration, deadline)
            self.tasks.append(task)
        
        return self.tasks

    def __repr__(self):
        return f"Task(id={self.id}, income={self.income}, duration={self.duration}, deadline={self.deadline})"