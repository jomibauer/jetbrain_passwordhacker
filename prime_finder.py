# Next Prime Number - Have the program find prime numbers until the user chooses to stop asking for the next one.

#take our current prime, add one to it.  divide it by each number in the prime list.  if we never get a % == 0, thats the new prime

def prime_finder():
    prime_l = [2]
    prime = 2
    while True:
        print('prime is ' + str(prime))
        print('want prime?')
        ans = input('y or n\n')
        if ans.lower() == 'n':
            print('ok')
            print('primes are')
            print(', '.join([str(i) for i in prime_l]))
            break
        elif ans.lower() != 'y':
            print('huh try again')
        else:
            prime = gen_prime(prime, prime_l)
            prime_l.append(prime)

def gen_prime(temp_prime, prime_l):
    while True:
        temp_prime += 1
        limit = temp_prime ** 0.5
        for i in prime_l:
            if i > limit:
                return temp_prime
            if temp_prime % i == 0:
                break

def is_prime(x):

    for i in range(3, int(x**0.5)+1, 2):
        print(i)

prime_finder()