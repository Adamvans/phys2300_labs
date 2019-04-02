import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 1    # meters
W = 0.002   # arm radius
R = 0.01     # ball radius
framerate = 100
steps_per_frame = 10

d = .5  # damping constant

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
    #create ceiling to hang Pendulum from 
    box(pos = vector(0,0,0), length=1, height=.01, width=1, color=color.red)

def f_x(r,t):
    """
    Pendulum equation to create movment. 
    arguments:
     r is the input angles 
     t is the time running 
    """
    theta = r[0]
    omega = r[1]
    # set new change in theta to be old omega 
    ftheta = omega
    # calutation to get the change in omega -(d*omega) is the cw with d being c or the damping constant
    fomega = -(g/l)*np.sin(theta) -(d*omega)
    return np.array([ftheta, fomega], float)



def plotPend():
    """
    Plot the Pendulum  
    and 
    simulate the Pendulum 
    """
    # Set up initial values

    h = 1.0/(framerate * steps_per_frame)
    r = np.array([np.pi*175/180, 0], float)
    rnew = np.array([np.pi*90/180, 0], float)
    r_plot = np.array([np.pi*150/180, 0], float)

    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    xn = l*np.sin(rnew[0])
    yn = -l*np.cos(rnew[0])

    # ceate pendulum objects. 
    ball = sphere(pos=vector(x,y,0), radius=R, color=color.cyan)
    rod=cylinder(pos=vector(0,0,0) ,axis=ball.pos ,radius=W , color=color.cyan)

    ballN = sphere(pos=vector(xn,yn,0), radius=R, color=color.purple)
    rodN  =cylinder(pos=vector(0,0,0) ,axis=ball.pos ,radius=W , color=color.purple)


    # get data into list to plot. 
    xpoints = [] 
    tpoints = []
    # Loop over some time interval
    dt = 0.01
    t = 0
    while t < 20:
        rate(framerate)
        #Use the 4'th order Runga-Kutta approximation
        for i in range(steps_per_frame):
            # Calculate the 4th Order Rung-Kutta
            k1 = h*f_x(r,t)
            k2 = h*f_x(r + 0.5*k1, t + 0.5*h)
            k3 = h*f_x(r + 0.5*k2, t + 0.5*h)
            k4 = h*f_x(r+k3, t+h)
            r += (k1 + 2*k2 + 2*k3 + k4)/6
            # second pendulim 
            n1 = h*f_x(rnew,t)
            n2 = h*f_x(rnew + 0.5*n1, t + 0.5*h)
            n3 = h*f_x(rnew + 0.5*n2, t + 0.5*h)
            n4 = h*f_x(rnew+n3, t+h)
            rnew += (n1 + 2*n2 + 2*n3 + n4)/6

        # use the Pendulum equation directly without the  Runga-Kutta to get the plot. 
        r_plot += h*f_x(r,t)
        t += dt
        # Update positions
        x = l*np.sin(r[0])
        y = -l*np.cos(r[0])

        xn = l*np.sin(rnew[0])
        yn = -l*np.cos(rnew[0])

        
        # save points to plot 
        xpoints.append(l*np.sin(r_plot[0]))
        tpoints.append(t)
        # Update the pendulum's bob
        ball.pos = vector(x,y,0)
        ballN.pos = vector(xn,yn,0)

        # Update the cylinder axis
        rod.axis = ball.pos
        rodN.axis = ballN.pos

    # plot for Task 1  
    plt.plot(tpoints, xpoints)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.show()

def main():
    """
    """
    set_scene() # create scene 
    plotPend() # do the simulation and ploting 

if __name__ == "__main__":
    main()
    exit(0)