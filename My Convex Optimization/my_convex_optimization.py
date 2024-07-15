import numpy as np
import matplotlib.pyplot as plt
#function to print 
def print_a_function(f, values):
    plt.plot(values, f(values))
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Plot of f(x)')
    plt.grid(True)
    plt.show()
#this function find the root using the bisection
def find_root_bisection(f, min, max):
    while max - min >= 0.001:
        c = (min + max) / 2
        if f(c) * f(min) < 0:
            max = c
        else:
            min = c
    return c
#use the newton method to find the root
def find_root_newton_raphson(f, f_deriv, x0):
    while True:
        x = x0 - f(x0) / f_deriv(x0)
        if abs(f(x)) < 1e-6:
            return x
        x0 = x
# gradient descent method
def gradient_descent(f,f_prime,start,learning_rate):
    x_current = start
    x_next = x_current - learning_rate * f_prime(x_current)
    precision=0.0001
    while abs(x_next - x_current) >= precision:
        x_current = x_next
        x_next = x_current - learning_rate * f_prime(x_current)
    
    return x_next
# this function use simplex method to solve the problem
def solve_linear_problem(A, b, c):
    from scipy.optimize import linprog
    x0_bounds = (0, None)
    x1_bounds = (0, None)
    res = linprog(c, A_ub=A, b_ub=b,  bounds=(x0_bounds, x1_bounds), method='simplex', options={"disp": True})
    return res.fun,res.x

A = np.array([[2,1],[-4,5],[1,-2]])
b = np.array([10,8,3])
c = np.array([-1,-2])