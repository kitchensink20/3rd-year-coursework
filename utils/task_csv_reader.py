import csv
from task import Task  
from constants import *

class TaskCSVReader:
    def read_tasks(file_path=CSV_FILE_PATH):
        tasks = []
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task = Task(
                    id=int(row['id']),
                    income=int(row['income']),
                    duration=int(row['duration']),
                    deadline=int(row['deadline'])
                )
                tasks.append(task)
        return tasks

