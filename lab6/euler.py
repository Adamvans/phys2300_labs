import numpy as np
from matplotlib import pyplot as plt

def f_x(x, t):
    """
    Euler's method
    """
    return -x**3 + np.sin(t)


def main():
    """
    """
    a = 0.0         # Start of interval
    b = 10.0        # End of interval
    N = 1000        # Number of steps
    h = (b-a)/N     # Size of single step
    x = 0.0         # Initial condition

    tpoints = np.arange(a, b, h)
    xpoints = []
    # loop over time interval
    for t in tpoints:
        xpoints.append(x)
        x += h*f_x(x, t)

    # Plot Values
    plt.plot(tpoints, xpoints)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.show()

if __name__ == "__main__":
    main()
    exit(0)
