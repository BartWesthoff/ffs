from random import *

if __name__ == "__main__":
    # userinterface().mainScreen()
    for i in range(9):
        id = [str(randint(0 if i == 0 else 1, 9)) for i in range(0, 9)]
        last_digit = sum(int(i) for i in id) % 10
        id = ''.join(id) + str(last_digit)
        print(id)
