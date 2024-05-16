import random
from task import Task
from constants import *

class TaskGenerator:
    def generate_tasks(n):
        tasks = []
        for i in range(1, n + 1):
            income = random.randint(MIN_TASK_INCOME, MAX_TASK_INCOME)
            deadline = random.randint(MIN_TASK_DEADLINE, MAX_TASK_DEADLINE)
            duration = random.randint(MIN_TASK_DURATION, deadline)
            task = Task(i, income, duration, deadline)
            tasks.append(task)
        
        return tasks