"""
fizzbuzz

Write a python script which prints the numbers from 1 to 100,
but for multiples of 3 print "fizz" instead of the number,
for multiples of 5 print "buzz" instead of the number,
and for multiples of both 3 and 5 print "fizzbuzz" instead of the number.
"""
def fizz_buzz_helper(n):
    if (n%3 == 0) and (n%5 != 0):
        return 'fizz'
    elif (n%3 != 0) and (n%5 == 0):
        return 'buzz'
    elif (n%3 == 0) and (n%5 == 0):
        return 'fizzbuzz'
    return n

def fizzbuzz(n):
    for i in range(1,n+1):
        print(fizz_buzz_helper(i))
    return None

if __name__ == '__main__':
    fizzbuzz(100)
    