file = open('Codingal.txt', 'r')
print(file.read())
file.close()

file = open('Codingal.txt', 'r')
print("\n Read in parts \n")
print(file.read(8))
file.close()

file = open('Codingal', 'a')
file.write(" Hi! I Am A Penguin An I Am 1 yr old.")
file.close()