class student:
    grade = "5th"
    Name = "Ayaan Mohammed Fazil Gaffoor"

    def introduction(self):
        print("Hi My Name Is", self.Name)

    def details(self):
        print("I Am A Student")
        print("I Study In Grade", self.grade)

ob = student()
ob.introduction()
ob.details()