class Employee:
    def __init__(self):
        print('Employee created.')
    def __del__(self):
        print('Destructer called, Employee deleted.')

obj = Employee()
del obj