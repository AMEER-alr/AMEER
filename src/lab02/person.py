from .pet import Pet

class Person:
    def __init__(self, name: str, pet: Pet = None):
        self._name = name
        self._pet = pet

    def set_pet(self, pet: Pet):
        self._pet = pet

    def get_pet_info(self):
        print("-------------------------")
        if self._pet is None:
            print(f"{self._name} has no pet yet")
            print("-------------------------")
            return
        
        print(f"Pet for {self._name} is named {self._pet.get_name()}")
        print(f"Age: {self._pet.get_age()} year(s), about {self._pet.get_age_in_human_years()} human years")
        print("And it expresses itself like this:")
        self._pet.express()
        print("-------------------------")