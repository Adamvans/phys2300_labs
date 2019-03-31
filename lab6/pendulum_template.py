import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 1    # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
framerate = 100
steps_per_frame = 10

def set_scene():
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 6: Pendulum motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate.
    """
    box(pos = vector(0,0,0), length=1, height=.01, width=1, color=color.red)

def f_x(r):
    """
    Pendulum
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta)
    return np.array([ftheta, fomega], float)

def main():
    """
    """
    set_scene()
    # Set up initial values

    h = 1.0/(framerate * steps_per_frame)
    r = np.array([np.pi*179/180, 0], float)
    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    ball = sphere(pos=vector(x,y,0), radius=R, color=color.cyan)
    rod=cylinder(pos=vector(0,0,0) ,axis=ball.pos ,radius=W , color=color.green)


    # get data into list to plot. 
    xpoints = [] 
    tpoints = []
    # Loop over some time interval
    dt = 0.01
    t = 0
    while t < 60:
        rate(framerate)
        # Use the 4'th order Runga-Kutta approximation
#        for i in range(steps_per_frame):
        r += h*f_x(r)

        t += dt
        # Update positions
        x = l*np.sin(r[0])
        y = -l*np.cos(r[0])

        # save pint to plot 
        xpoints.append(x)
        tpoints.append(t)
        # Update the pendulum's bob
        ball.pos = vector(x,y,0)
        # Update the cylinder axis
        rod.axis = ball.pos

    plt.plot(tpoints, xpoints)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.show()

if __name__ == "__main__":
    main()
    exit(0)