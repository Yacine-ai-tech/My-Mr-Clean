import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to compute the dot product of vectors x and theta
def h(x, theta):
    return np.dot(x, theta)

# Function to calculate mean squared error
def mean_squared_error(y_predicted, y_label):
    return ((y_predicted - y_label) ** 2).mean()

# Class for performing least squares regression
class LeastSquaresRegression:
    def __init__(self):
        self.theta_ = None

    def fit(self, X, y):
        # Calculates theta that minimizes the MSE and updates self.theta_
        self.theta_ = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

    def predict(self, X):
        # Make predictions for data X, i.e., output y = h(X)
        return h(X, self.theta_)


# Generating random data for linear regression
X = 4 * np.random.rand(100, 1)
y = 10 + 2 * X + np.random.randn(100, 1)

# Adding bias column to feature matrix X
def bias_column(X):
    X_b = np.c_[np.ones((X.shape[0], 1)), X]
    return X_b
X_new = bias_column(X)

# Creating an instance of the least squares regression model
model = LeastSquaresRegression()
model.fit(X_new, y)

# Plotting the original data points and the regression line
def my_plot(X, y, y_new):
    plt.scatter(X, y, color="b", marker="o", s=30)
    plt.plot(X, y_new, color="r")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('my_linear_regression.png')
    plt.show()

# Making predictions using the trained model
y_new = model.predict(X_new)
my_plot(X, y, y_new)

# Class for gradient descent optimization
class GradientDescentOptimizer:
    def __init__(self, f, fprime, start, learning_rate=0.1):
        self.f_ = f                       # The function
        self.fprime_ = fprime             # The gradient of f
        self.current_ = start             # The current point being evaluated
        self.learning_rate_ = learning_rate  # Step size for gradient descent

        # Save history as attributes
        self.history_ = [start]

    def step(self):
        # Take a gradient descent step
        gradient = self.fprime_(self.current_)
        self.current_ -= self.learning_rate_ * gradient
        self.history_.append(self.current_)

    def optimize(self, iterations=100):
        # Use gradient descent to get closer to the minimum
        for _ in range(iterations):
            self.step()

    def print_result(self):
        # Print the final optimized theta and its corresponding function value
        print("Best theta found is " + str(self.current_))
        print("Value of f at this theta: f(theta) = " + str(self.f_(self.current_)))

# Function to compute the value of the given function
# Function to compute the value of the given function
def f(x):
    a = np.array([2, 6])  # Define the vector (2, 6)
    x = np.atleast_2d(x)  # Ensure x is at least 2D
    return 3 + np.sum((x - a)**2, axis=1)  # Compute the squared distance



# Derivative of f
def fprime(x):
    a = np.array([2, 6])  # Define the vector (2, 6)
    return 2 * (x - a)


# Creating an instance of the gradient descent optimizer
grad = GradientDescentOptimizer(f, fprime, np.random.normal(size=(2,)), 0.1)
grad.optimize(10)
grad.print_result()

# Plotting the function f in 3D
# Plotting the function f in 3D
def plot_function_f_3d():
    a = np.linspace(-10, 10, 20)
    b = np.linspace(-10, 10, 20)
    X, Y = np.meshgrid(a, b)
    points = np.column_stack([X.ravel(), Y.ravel()])

    # Evaluate f for each point
    Z = f(points)

    # Reshape Z to have the same shape as X and Y
    Z = Z.reshape(X.shape)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(121, projection='3d')

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='b', alpha=0.1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Function f in 3D')
    plt.savefig('function_f_in_3D.png')
    plt.show()


# Plotting the optimization path on the function f in 3D
def plot_optimization_path():
    a = np.linspace(-10, 10, 20)
    b = np.linspace(-10, 10, 20)
    X, Y = np.meshgrid(a, b)

    # Reshape X and Y to 1D arrays
    X_flat = X.ravel()
    Y_flat = Y.ravel()

    # Combine X and Y into a single 2D array
    points = np.column_stack([X_flat, Y_flat])

    # Evaluate f for each point
    Z = f(points)

    # Reshape Z to have the same shape as X and Y
    Z = Z.reshape(X.shape)

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='b', alpha=0.1)
    ax.plot([t[0] for t in grad.history_], [t[1] for t in grad.history_], markerfacecolor='b', markeredgecolor='b',
            marker='.', markersize=5)
    plt.savefig('progression.png')
    plt.show()

# Plot the function f in 3D
plot_function_f_3d()

# Plot the optimization path on the function f in 3D
plot_optimization_path()
