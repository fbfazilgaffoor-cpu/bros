def recur_factorial(n):
    if n == 1:
        return n
    else:
        return n*recur_factorial(n-1)
num = int(input("Enter A Number: "))

if num < 0:
    print("Sorry, Factorial Does Not Exist For Negative Numbers")
elif num == 0:
    print("The Factorial Of 0 Is 1")
else:
    print("The Factorial Of", num, "is", recur_factorial(num))