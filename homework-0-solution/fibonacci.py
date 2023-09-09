"""
fibonacci

functions to compute fibonacci numbers

Complete problems 2 and 3 in this file.
"""

import time # to compute runtimes
from tqdm import tqdm # progress bar
import numpy as np

# Question 2
def fibonacci_recursive(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_recursive(n-1)+fibonacci_recursive(n-2)

# Question 2
def fibonacci_iter(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    a = 0
    b = 1
    for i in range(1,n):
        a,b = b, a+b
    return b


# Question 3
def egyptian_array_power(a, n):
    """
    computes the power a ** n

    assume n is a nonegative integer
    """
    """
    returns the product a * n

    assume n is a nonegative integer
    """
    def isodd(n):
        """
        returns True if n is odd
        """
        return n & 0x1 == 1

    if n == 1:
        return a
    if n == 0:
        return np.array([1,0],[0,1])

    if isodd(n):
        return egyptian_array_power(a @ a, n // 2) @ a
    else:
        return egyptian_array_power(a @ a, n // 2)
    
def fibonacci_power(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    single_evolve = np.array([[1,1],[1,0]],dtype = np.int64)
    fibor_vector = np.array([[1],[0]],dtype = np.int64)
    evolve = egyptian_array_power(single_evolve, n-1) 
    fibor_vector = evolve @ fibor_vector
    return fibor_vector[0,0]
    


if __name__ == '__main__':
    """
    this section of the code only executes when
    this file is run as a script.
    """
    for i in range(1,31):
        print('fibo({i}) = {iter_result} (iter) = {recursive_result} (recursive) = {p_result} (numpy power) '.format(i = i, iter_result = fibonacci_iter(i),\
            recursive_result = fibonacci_recursive(i),p_result = fibonacci_power(i)))
    def get_runtimes(ns, f):
        """
        get runtimes for fibonacci(n)

        e.g.
        trecursive = get_runtimes(range(30), fibonacci_recusive)
        will get the time to compute each fibonacci number up to 29
        using fibonacci_recursive
        """
        ts = []
        for n in tqdm(ns):
            t0 = time.time()
            fn = f(n)
            t1 = time.time()
            ts.append(t1 - t0)

        return ts


    nrecursive = range(35)
    trecursive = get_runtimes(nrecursive, fibonacci_recursive)

    niter = range(10000)
    titer = get_runtimes(niter, fibonacci_iter)

    npower = range(10000)
    tpower = get_runtimes(npower, fibonacci_power)

    ## write your code for problem 4 below...
    import matplotlib.pyplot as plt

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.loglog(nrecursive, trecursive, label='recursive')
    plt.loglog(niter, titer, label='iterative')
    plt.loglog(npower, tpower, label='power')

    # Add a legend
    plt.legend()

    # Add labels and a title
    plt.xlabel('log n')
    plt.ylabel('t')
    plt.title('Fibo algo time complexity')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig('fibonacci_runtime.png')

    plt.show()
