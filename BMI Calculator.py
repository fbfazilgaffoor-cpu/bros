height = float(input("Enter Your Height In Centieters:"))
weight = float(input("Enter Your Weight In Kilograms:"))

BMI = weight / (height/100)**2

print("Your BMI iS", BMI)
if BMI <= 18.4:
    print(" You Are Underweight.")
elif BMI <= 24.9:
    print(" You Are Healthy.")
elif BMI <= 29.9:
    print("You Are Overweight.")
elif BMI <= 34.9:
    print("You Are Severely Overweight.")
elif BMI <= 39.9:
    print("You Are Obese.")
else:
    print("You Are Severely Obese")