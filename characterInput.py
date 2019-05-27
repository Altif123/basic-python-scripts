name = str(input('Please enter your name: '))
age = int(input('please enter your age as an integer: '))

age100 = 100 - age

message = "name: ", name, " age: ", str(age), " years left to reach 100 years old: ", str(age100)
print(message)
repeat = int(input('how many times print message: '))


count = 0
for i in range(repeat):
    print(format(message))
    count += 1

print("number of times printed: " + str(count))
