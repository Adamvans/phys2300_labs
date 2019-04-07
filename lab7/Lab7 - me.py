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
    mass = []

    if args.file == "no file":

        # keep asking untill you get a valid answer. 

        error = True
        while(error):
            # try catch to see if it is a valed number. 
            try:
                mass.append(float(input("Please enter the Mass of the Sun: "))) 
                error = False
            except:
                print("That is not a number. Please enter a number. ie 1.99e30")
                error = True
        
        error = True
        while(error):
            # try catch to see if it is a valed number. 
            try:
                data.loc['Earth+Moon barycenter', 'x'] = float(input("Please enter the initial distance of earth from the sun: "))
                data.loc['Earth+Moon barycenter', 'y'] = 0
                data.loc['Earth+Moon barycenter', 'z'] = 0
                error = False
            except:
                print("That is not a number. Please enter a number. ie 1.5e11")
                error = True
        
        error = True
        while(error):
            # try catch to see if it is a valed number. 
            try:
                data.loc['Earth+Moon barycenter', 'vy'] = float(input("Please enter the initial velocity of earth: "))
                data.loc['Earth+Moon barycenter', 'vx'] = 0
                data.loc['Earth+Moon barycenter', 'vz'] = 0
                error = False
            except:
                print("That is not a number. Please enter a number. ie 3e4")
                error = True

        error = True
        while(error):
            # try catch to see if it is a valed number. 
            try:
                mass.append(float(input("Please enter the Mass of earth: "))) 
                error = False
            except:
                print("That is not a number. Please enter a number. ie 5.97e24")
                error = True

        # # initial location in x
        # data.loc['Mercury', 'x'] = 5.791*10**10
        # data.loc['Mercury', 'y'] = 0
        # data.loc['Mercury', 'z'] = 0
        # data.loc['Venus', 'x'] = 1.082*10**11
        # data.loc['Venus', 'y'] = 0
        # data.loc['Venus', 'z'] = 0
        # data.loc['Earth+Moon barycenter', 'x'] = 1.5e11
        # data.loc['Earth+Moon barycenter', 'y'] = 0
        # data.loc['Earth+Moon barycenter', 'z'] = 0
        # data.loc['Mars', 'x'] = 2.279*10**11
        # data.loc['Mars', 'y'] = 0
        # data.loc['Mars', 'z'] = 0

        # # initial velocity
        # data.loc['Mercury', 'vx'] = 0
        # data.loc['Mercury', 'vy'] = 4.8*10**4
        # data.loc['Mercury', 'vz'] = 0
        # data.loc['Venus', 'vx'] = 0
        # data.loc['Venus', 'vy'] = 3.5*10**4
        # data.loc['Venus', 'vz'] = 0
        # data.loc['Earth+Moon barycenter', 'vx'] = 0
        # data.loc['Earth+Moon barycenter', 'vy'] = 3e4
        # data.loc['Earth+Moon barycenter', 'vz'] = 0
        # data.loc['Mars', 'vx'] = 0
        # data.loc['Mars', 'vy'] = 2.4*10**4
        # data.loc['Mars', 'vz'] = 0
    else:
        data = pd.read_csv(args.file, skiprows=[0], index_col='planet')
        data.rename(columns=lambda x: x.strip(), inplace=True)
        data = data.multiply(1.5e11)  # multiply the data by 1 au in meters.
    
    return data,mass


def setupPlanets(data, mass):
    """    
    This functions uses the data to set up the simulation then calls the animate function 
    Pramater1 : list of solor system data. 
    pramater2 : if the mass is provieded by input from the user this is used to pull that data. 
    """

    scene.title = "Assignment 7: N-Body simulation of the solar system"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate.
    """

    if len(mass) == 0:
        # mass
        M_sun = 1.99e30
        M_mercury = 3.285e23
        M_venus = 4.867e24
        M_earth = 5.97e24
        M_mars = 6.39e23
        M_jupiter = 1.898e27
        M_saturn = 5.683e26
        M_uranus = 8.681e25
        M_neptune = 1.024e26
        M_pluto = 1.309e22
    else:
        M_sun = mass[0]
        M_earth = mass[1]
    

    # 6.371*10**6
    planets = []
    # Set up initial values
    sun = sphere(pos=vector(0,0,0), radius=695.51e7, mass=M_sun, emissive=True,
    acceleration=vector(0,0,0), velocity=vector(0,0,0), color=color.yellow)

    earth = sphere(pos=vector(data.loc['Earth+Moon barycenter', 'x'], data.loc['Earth+Moon barycenter', 'y'], data.loc['Earth+Moon barycenter', 'z']),
     radius=6.371e6, mass=M_earth, acceleration=vector(0,0,0),  color=color.blue, make_trail=True, emissive=True,
     velocity=vector(data.loc['Earth+Moon barycenter', 'vx'], data.loc['Earth+Moon barycenter', 'vy'], data.loc['Earth+Moon barycenter', 'vz']))

    if len(mass) == 0:
        mercury = sphere(pos=vector(data.loc['Mercury', 'x'], data.loc['Mercury', 'y'], data.loc['Mercury', 'z']),
        radius=2.4397e6, mass=M_mercury, acceleration=vector(0,0,0),  color=color.white, make_trail=True, emissive=True,
        velocity=vector(data.loc['Mercury', 'vx'], data.loc['Mercury', 'vy'], data.loc['Mercury', 'vz']))

        venus = sphere(pos=vector(data.loc['Venus', 'x'], data.loc['Venus', 'y'], data.loc['Venus', 'z']),
        radius=6.0518e6, mass=M_venus, acceleration=vector(0,0,0),  color=color.purple, make_trail=True, emissive=True,
        velocity=vector(data.loc['Venus', 'vx'], data.loc['Venus', 'vy'], data.loc['Venus', 'vz']))

        mars = sphere(pos=vector(data.loc['Mars', 'x'], data.loc['Mars', 'y'], data.loc['Mars', 'z']),
        radius=3.3895e6, mass=M_mars, acceleration=vector(0,0,0),  color=color.red, make_trail=True, emissive=True,
        velocity=vector(data.loc['Mars', 'vx'], data.loc['Mars', 'vy'], data.loc['Mars', 'vz']))

        jupiter = sphere(pos=vector(data.loc['Jupiter', 'x'], data.loc['Jupiter', 'y'], data.loc['Jupiter', 'z']),
        radius=69.911e6, mass=M_jupiter, acceleration=vector(0,0,0),  color=color.orange, make_trail=True, emissive=True,
        velocity=vector(data.loc['Jupiter', 'vx'], data.loc['Jupiter', 'vy'], data.loc['Jupiter', 'vz']))

        saturn = sphere(pos=vector(data.loc['Saturn', 'x'], data.loc['Saturn', 'y'], data.loc['Saturn', 'z']),
        radius=58.232e6, mass=M_saturn, acceleration=vector(0,0,0),  color=color.magenta, make_trail=True, emissive=True,
        velocity=vector(data.loc['Saturn', 'vx'], data.loc['Saturn', 'vy'], data.loc['Saturn', 'vz']))

        uranus = sphere(pos=vector(data.loc['Uranus', 'x'], data.loc['Uranus', 'y'], data.loc['Uranus', 'z']),
        radius=25.362e6, mass=M_neptune, acceleration=vector(0,0,0),  color=color.cyan, make_trail=True, emissive=True,
        velocity=vector(data.loc['Uranus', 'vx'], data.loc['Uranus', 'vy'], data.loc['Uranus', 'vz']))

        neptune = sphere(pos=vector(data.loc['Neptune', 'x'], data.loc['Neptune', 'y'], data.loc['Neptune', 'z']),
        radius=24.622e6, mass=M_uranus, acceleration=vector(0,0,0),  color=color.green, make_trail=True, emissive=True,
        velocity=vector(data.loc['Neptune', 'vx'], data.loc['Neptune', 'vy'], data.loc['Neptune', 'vz']))

        pluto = sphere(pos=vector(data.loc['Pluto', 'x'], data.loc['Pluto', 'y'], data.loc['Pluto', 'z']),
        radius=1.1883e6, mass=M_pluto, acceleration=vector(0,0,0),  color=color.white, make_trail=True, emissive=True,
        velocity=vector(data.loc['Pluto', 'vx'], data.loc['Pluto', 'vy'], data.loc['Pluto', 'vz']))

        planets.append(mercury)
        planets.append(venus)
        planets.append(mars)
        planets.append(jupiter)
        planets.append(saturn)
        planets.append(uranus)
        planets.append(neptune)
        planets.append(pluto)



    planets.append(sun)
    planets.append(earth)
    

    animatePlanets(planets)

def animatePlanets(objects):
    """
    This functions animates pre-loaded planets 
    Pramater1 : list of solor system objects. 
    """
    # time 
    dt = 6.3e4
    totalTime = 3.15e7
    time = 0
    G = 6.67408e-11

    while time < totalTime:
        rate(300)
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

    data, mass = getdata(args)
    setupPlanets(data, mass)

    

if __name__ == "__main__":
    main()
    exit(0)