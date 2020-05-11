def fizz_buzz(x):
    for i in range(1, x+1):
        f = i%3 == 0
        b = i%5 == 0
        fb = f and b
        if fb:
            print('FizzBuzz')
        elif b:
            print('Buzz')
        elif f:
            print('Fizz')
        else:
            print(i)

fizz_buzz(100)