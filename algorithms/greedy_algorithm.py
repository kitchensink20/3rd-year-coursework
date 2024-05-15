class GreedyAlgorithm:
    def __init__(self, n, m, tasks):
        self.n = n  # кількість робіт
        self.m = m  # кількість машин
        self.tasks = tasks

    def maximize_income(self):
        # Ініціалізація
        F_m = [0] * self.m  # Поточний загальний час на кожній машині
        S_m = [[] for _ in range(self.m)]  # Розклад виконання робіт для кожної машини
        Z = 0  # Загальний дохід від виконаних робіт

        # Упорядкувати вектор робіт J за зменшенням c_i/p_i
        self.tasks.sort(key=lambda task: task.income / task.duration, reverse=True)

        # Для кожної роботи i в J
        for task in self.tasks:
            # Знайти машину j з мінімальним F_j
            j = F_m.index(min(F_m))
            
            # Якщо F_j + p_i ≤ d_i
            if F_m[j] + task.duration <= task.deadline:
                # Додати роботу i до розкладу S_i на машині j
                S_m[j].append(task)
                
                # Збільшити поточний загальний час виконання роботи F_j на машині j
                F_m[j] += task.duration
                
                # Додати прибуток c_i від виконання роботи i в загальний дохід Z
                Z += task.income
        
        return S_m, Z