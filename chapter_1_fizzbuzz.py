# Original code/example from Alex Kenan's PYMAE project:
# https://github.com/alexkenan/pymae
# Explanatory comments added by me, Ethan Koh.
# Changes made: added comments explaining how each section works.

# Loop through each number from 1 to 100.
# range(1, 101) starts at 1 and stops before 101.
for number in range(1, 101):

    # First, check if the number is divisible by both 3 and 5.
    # The modulo operator (%) gives the remainder after division.
    # If both remainders are 0, print "FizzBuzz".
    if (number % 3 == 0) and (number % 5 == 0):
        print('FizzBuzz')

    # If the number is not divisible by both 3 and 5,
    # check whether it is divisible by 5 only.
    elif number % 5 == 0:
        print('Buzz')

    # If the number is not divisible by 5,
    # check whether it is divisible by 3 only.
    elif number % 3 == 0:
        print('Fizz')

    # If none of the conditions above are true,
    # print the number itself.
    else:
        print(number)
