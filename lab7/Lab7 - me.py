import numpy as np
from matplotlib import pyplot as plt
from vpython import *
import argparse
import pandas as pd

def getdata(args):
    """
    This functions gets the data from the user or the file.  
    Pramater1 : args to get the file if it is there.  
    """
    data = pd.DataFrame()

    if args.file == "no file":
        # initial location in x
        data.loc['Mercury', 'x'] = 5.791*10**10
        data.loc['Mercury', 'y'] = 0
        data.loc['Mercury', 'z'] = 0
        data.loc['Venus', 'x'] = 1.082*10**11
        data.loc['Venus', 'y'] = 0
        data.loc['Venus', 'z'] = 0
        data.loc['Earth+Moon barycenter', 'x'] = 1.5*10**11
        data.loc['Earth+Moon barycenter', 'y'] = 0
        data.loc['Earth+Moon barycenter', 'z'] = 0
        data.loc['Mars', 'x'] = 2.279*10**11
        data.loc['Mars', 'y'] = 0
        data.loc['Mars', 'z'] = 0

        # initial velocity
        data.loc['Mercury', 'vx'] = 0
        data.loc['Mercury', 'vy'] = 4.8*10**4
        data.loc['Mercury', 'vz'] = 0
        data.loc['Venus', 'vx'] = 0
        data.loc['Venus', 'vy'] = 3.5*10**4
        data.loc['Venus', 'vz'] = 0
        data.loc['Earth+Moon barycenter', 'vx'] = 0
        data.loc['Earth+Moon barycenter', 'vy'] = 3*10**4
        data.loc['Earth+Moon barycenter', 'vz'] = 0
        data.loc['Mars', 'vx'] = 0
        data.loc['Mars', 'vy'] = 2.4*10**4
        data.loc['Mars', 'vz'] = 0
    else:
        data = pd.read_csv(args.file, skiprows=[0], index_col='planet')
        data.rename(columns=lambda x: x.strip(), inplace=True)
        data = data.multiply(1.5*10**11)  # multiply the data by 1 au in meters.
    
    return data


def setupPlanets(data):
    """    
    This functions uses the data to set up the simulation then calls the animate function 
    Pramater1 : list of solor system data. 
    """

    scene.title = "Assignment 7: N-Body simulation of the solar system"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate.
    """

    # mass
    M_sun = 1.99*10**30
    M_mercury = 3.285*10**23
    M_venus = 4.867*10**24
    M_earth = 5.97*10**24
    M_mars = 6.39*10**23
    

    # 6.371*10**6

    # Set up initial values
    sun = sphere(pos=vector(0,0,0), radius=695.51*10**7, mass=M_sun, emissive=True,
    acceleration=vector(0,0,0), velocity=vector(0,0,0), color=color.yellow)

    mercury = sphere(pos=vector(data.loc['Mercury', 'x'], data.loc['Mercury', 'y'], data.loc['Mercury', 'z']),
     radius=695.51*10**6, mass=M_mercury, acceleration=vector(0,0,0),  color=color.white, make_trail=True, emissive=True,
     velocity=vector(data.loc['Mercury', 'vx'], data.loc['Mercury', 'vy'], data.loc['Mercury', 'vz']))

    venus = sphere(pos=vector(data.loc['Venus', 'x'], data.loc['Venus', 'y'], data.loc['Venus', 'z']),
     radius=695.51*10**6, mass=M_venus, acceleration=vector(0,0,0),  color=color.purple, make_trail=True, emissive=True,
     velocity=vector(data.loc['Venus', 'vx'], data.loc['Venus', 'vy'], data.loc['Venus', 'vz']))

    earth = sphere(pos=vector(data.loc['Earth+Moon barycenter', 'x'], data.loc['Earth+Moon barycenter', 'y'], data.loc['Earth+Moon barycenter', 'z']),
     radius=695.51*10**6, mass=M_earth, acceleration=vector(0,0,0),  color=color.blue, make_trail=True, emissive=True,
     velocity=vector(data.loc['Earth+Moon barycenter', 'vx'], data.loc['Earth+Moon barycenter', 'vy'], data.loc['Earth+Moon barycenter', 'vz']))

    mars = sphere(pos=vector(data.loc['Mars', 'x'], data.loc['Mars', 'y'], data.loc['Mars', 'z']),
     radius=695.51*10**6, mass=M_mars, acceleration=vector(0,0,0),  color=color.red, make_trail=True, emissive=True,
     velocity=vector(data.loc['Mars', 'vx'], data.loc['Mars', 'vy'], data.loc['Mars', 'vz']))

    planets = []
    planets.append(sun)
    planets.append(mercury)
    planets.append(venus)
    planets.append(earth)
    planets.append(mars)

    animatePlanets(planets)

def animatePlanets(objects):
    """
    This functions animates pre-loaded planets 
    Pramater1 : list of solor system objects. 
    """
    # time 
    dt = 6.3*10**4
    totalTime = 3.15*10**7
    time = 0
    G = 6.67408*10**-11

    while time < totalTime:
        rate(33)
        for i in objects:
            i.acceleration = vector(0,0,0)
            for j in objects:
                if i != j:
                    dist = j.pos - i.pos
                    i.acceleration = i.acceleration + G * j.mass * dist / mag(dist)**3
        for i in objects:
            i.velocity = i.velocity + i.acceleration*dt
            i.pos = i.pos + i.velocity * dt

    time = time + dt



def main():
    """
    """
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Assignment 7: N-Body simulation of the solar system")
    parser.add_argument("--file", "-f", action="store", dest="file", type=str, default="no file", help="full path of file to parse")
    args = parser.parse_args()

    #getdata(args)
    setupPlanets(getdata(args))

    

if __name__ == "__main__":
    main()
    exit(0)