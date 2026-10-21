from .animal import Animal

class Turtle(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def get_age_in_human_years(self):
        if self.get_age() <= 0:
            return 0
        return 15 + (self.get_age() - 1) * 2

    def express(self):
        print("""
   _____     _____
  /     \\   |  o |
 |       |/ ___\\|
 |_______/
 |_| |_| |_|
""")