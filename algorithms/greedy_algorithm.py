class GreedyAlgorithm:
    def __init__(self, n, m, tasks):
        self._n = n  # кількість робіт
        self._m = m  # кількість машин
        self._tasks = tasks

    def maximize_income(self):
        F_m = [0] * self._m 
        S_m = [[] for _ in range(self._m)]  
        Z = 0  

        self._tasks.sort(key=lambda task: task.income / task.duration, reverse=True)

        for task in self._tasks:
            j = F_m.index(min(F_m))
            
            if F_m[j] + task.duration <= task.deadline:
                S_m[j].append(task)
                
                F_m[j] += task.duration
                
                Z += task.income
        
        return S_m, Z