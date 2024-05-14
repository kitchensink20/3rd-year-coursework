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
        return f"Task(id={self.id}, income={self.income}, duration={self.duration}, deadline={self.deadline})"