from .animal import Animal

class Parrot(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def get_age_in_human_years(self):
        return self.get_age() * 5

    def express(self):
        print(f"{self.get_name()}: \"Hello!\"")
        print("""
   \\
   (o>
 \\_//)
  \_/_)
   _|_
""")