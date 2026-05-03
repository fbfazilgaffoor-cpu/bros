list = ['orange', 'apple', 'dragonfruit', 'grapes', 'mango', 'banana']

print("Length Of List:", len(list))
print("First Element:", list[0])
print("Last Element:", list[-1])

list.append('pear')
print("Updated List :", list)

list.remove('mango')
print("Updated List :", list)

list.sort()
print("Sorted List :", list)

list.pop(1)
print("Updated List :", list)

list.reverse()
print("Reversed List :", list)

print("Multiplication On List:",list*2)

list = list[:4]
print("Sliced List:", list)

list.clear()
print("Updated List :", list)