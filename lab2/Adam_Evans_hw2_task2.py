import numpy as np
import math as m
import matplotlib.pyplot as plt
"""
Adam Evans hw2 task2
this program calulates and displys the projectile motion of an object.
if run as main it will ask you for the inital location and velocity the object 
it will then use this to calculate the projectile motion of the object
"""
# NOTE: You may need to run: $ pip install matplotlib

# Function to calculate projectile motion
def calc_projectile(location,velocity,time,acceleration):
    """
    Function to calculate projectile motion in one dimension. 

    Param 1:
    initial location of the object
    Param 2:
    initial velocity of the object in the direction of the dimension 
    Param 3:
    total time from when the object was at the initial location. 
    Param 4:
    the acceleration of the object in the direction of the dimension 
    """
    return location + velocity*time + 0.5*acceleration*time**2

# Function to plot data
def plot_data(initialX,initialXSpeed,initialY,initialYSpeed,delt):
    """
    Function to store all calulated data and plot data.

    Param 1:
    initial x-axis location of the object
    Param 2:
    initial velocity of the object in the direction of the x-axis
    Param 3:
    initial y-axis location of the object
    Param 4:
    initial velocity of the object in the direction of the y-axis
    Param 5:
    the incraments of time to plot the data by. 
    """
    # not friction added 
    accelerationOfX = 0.0
    # define a constant of g 
    accelerationOfY = -9.8           

    # inisilize base data 
    time = 0.0
    x = []
    y = []
    interval = 170

    # loop over data to calulate x,y pairs to plot. 
    for i in range(interval):
        x.append(calc_projectile(initialX,initialXSpeed,time,accelerationOfX))
        y.append(calc_projectile(initialY,initialYSpeed,time,accelerationOfY))
        time = time + delt

        # when y goes negitive set t to get y to 0 then set that to the data point and break. 
        if y[i] < 0.0:
            # use quadtric formula to set y to as close to zero as possible. 
            timeToGroud = (initialYSpeed + m.sqrt(initialYSpeed**2 + (-2*accelerationOfY*initialY)))/(-accelerationOfY)
            x[i] = calc_projectile(initialX,initialXSpeed,timeToGroud,accelerationOfX)
            y[i] = calc_projectile(initialY,initialYSpeed,timeToGroud,accelerationOfY)
            break


    plt.plot(x, y)
    plt.show()

def getInitialLocation(corrd):
    """
    Function to get the input for the initial x and y values. 

    Param 1:
    the value you are looking for X or Y 
    """
    # keep asking untill you get a valid answer. 
    error = True
    while(error):
        # try catch to see if it is a valed number. 
        try:
            initialL = float(input("Please enter number for the initial "+ corrd +" coordinate: "))
            error = False
        except:
            print("That is not a number. Please enter a number.")
            error = True
    
    return initialL

def getInitialVelocity(corrd):
    """
    Function to get the input for the initial x and y velocity. 

    Param 1:
    the value you are looking for X or Y 
    """
    # keep asking untill you get a valid answer. 
    error = True
    while(error):
        # try catch to see if it is a valed number. 
        try:
            initialV = float(input("Please enter the initial velocity for the "+ corrd +" coordinate: "))
            error = False
        except:
            print("That is not a number. Please enter a number.")
            error = True
    
    return initialV

# "Main" Function
def main():
    """
    Function to test and run all other functions. 
    this askes for input then assings input. 
    this only runs if __name__ == "__main__". 
    """
    # initial x location  
    initialX = 1.0
    initialX = getInitialLocation("X")
    # initial y location     
    initialY = 0.0
    initialY = getInitialLocation("Y")
    # initial x velocity
    initialXSpeed = 70.0  
    initialXSpeed = getInitialVelocity("X")     
    # initial y velocity
    initialYSpeed = 80.0   
    initialYSpeed = getInitialVelocity("Y")         
    # distance between each sample in time. 
    delt = 0.1

    plot_data(initialX,initialXSpeed,initialY,initialYSpeed,delt)


if __name__ == "__main__":
    main()
    exit(0)



