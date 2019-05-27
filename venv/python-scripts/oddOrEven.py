print('This program will tell you if the number you enter is true or false')
number = int(input('enter a number:'))

if number % 2 == 0:
    print('number is even')
else:
    print('number is odd')

if number % 4 == 0:
    print('Number is divisible by 4')
else:
    print('number not divisible by 4')

number2 = int(input('enter a another number:'))
print('New number = ', number2)
if number % number2 == 0:
    print(number, 'new number divides evenly in to old number' , number2)
else:
    print(number, 'does not divide evenly in to', number2)
