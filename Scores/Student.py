class Student:
    """學生類別"""

    def __init__(self, student_id: str, name: str, chinese: int,
                 english: int, math: int, science: int):
        self.student_id = student_id
        self.name = name
        self.chinese = chinese
        self.english = english
        self.math = math
        self.science = science
        self.total = chinese + english + math + science
        self.average = self.total / 4
        self.rank = 0

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, 總分:{self.total})"


    