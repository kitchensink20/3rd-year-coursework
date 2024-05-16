class Task:
    def __init__(self, id, income, duration, deadline):
        """
        Ініціалізація параметрів роботи
        id: унікальний ідентифікатор роботи
        income: дохід від виконання роботи
        duration: тривалість роботи
        deadline: директивний строк закінчення роботи
        """
        self.id = id
        self.income = income
        self.duration = duration
        self.deadline = deadline

    def __repr__(self):
        return f"Задача(id={self.id}, прибуток={self.income}, тривалість={self.duration}, директивний строк={self.deadline})"