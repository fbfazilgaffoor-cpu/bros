class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f"I am a Cat. My name is {self.name} and i am {self.age} years old.")

    def make_sound(self):
        print("Meow")


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f"I am a Dog. My name is {self.name} and i am {self.age} years old")

    def make_sound(self):
        print("Bark")

cat1 = Cat("Mike", 2.5)
dog1 = Dog("Lebron",1.2)

for animal in (cat1, dog1):
    animal.make_sound()
    animal.info()