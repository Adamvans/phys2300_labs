from vpython import sphere, box, scene, color, vector, rotate, mag, rate, pi
from math import sin, cos, radians
import argparse



def set_scene(data):
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    # zoom in to see the ball moving 
    scene.range = 50

    scene.x = -1
    # the sky is blue
    scene.background = color.blue
    # the ground is green 
    box(pos = vector(0,0,0), length=2000, height=.1, width=1000, color=color.green)


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    # ball is cyan and has a trail.
    ball_nd = sphere(pos=vector(-80, data['init_height'], 0),
                        radius=1, color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position. 
    # set initial velosity to go in the x direcion and rotate via angle. rotate requres radians 
    ball_nd.velocity=rotate(vector(data['init_velocity'],0,0), angle=radians(data['theta']))
    # set the balls mass 
    ball_nd.mass = data['ball_mass']
    # set the balls momentum  
    ball_nd.p=ball_nd.velocity*ball_nd.mass
    # set the force of gravaity vector 
    netForce=vector(0,data['gravity'],0)*ball_nd.mass
    # time is 0 
    t = 0
    # Animate
    while ball_nd._pos.y > ball_nd.radius:
        rate(300)
        # plot via velosty tims deltat + position 
        ball_nd.pos=ball_nd.pos + (ball_nd.p/ball_nd.mass)*data['deltat']
        # set new monmentum 
        ball_nd.p = ball_nd.p + netForce*data['deltat']
        # set new time
        t = t + data['deltat']

def motion_drag(data):
    """
    Create animation for projectile motion with dragging force
    """
    ball_nd = sphere(pos=vector(-80, data['init_height'], 0),
                        radius=1, color=color.purple, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position. 
    # set initial velosity to go in the x direcion and rotate via angle. rotate requres radians 
    ball_nd.velocity=rotate(vector(data['init_velocity'],0,0), angle=radians(data['theta']))
    ball_nd.mass = data['ball_mass']
    # set the balls momentum  
    ball_nd.p=ball_nd.velocity*ball_nd.mass
    # foce of gravaty - force of air fiction (alpha*velosity^2) * a vector of 1 in the balls direction of movement. 
    netForce=((vector(0,data['gravity'],0)*ball_nd.mass) - (data['alpha']*mag(ball_nd.p/ball_nd.mass)**2 * (ball_nd.p/mag(ball_nd.p)))) 

    t = 0
    # Animate
    while ball_nd._pos.y > ball_nd.radius:
        rate(300)
        # plot via velosty tims deltat + position 
        ball_nd.pos=ball_nd.pos + (ball_nd.p/ball_nd.mass)*data['deltat']
        # air friction changes with speed of the ball. 
        netForce = ((vector(0,data['gravity'],0)*ball_nd.mass) - (data['alpha']*mag(ball_nd.p/ball_nd.mass)**2 * (ball_nd.p/mag(ball_nd.p)))) 
        # set new monmentum 
        ball_nd.p = ball_nd.p + netForce * data['deltat']
         # set new time
        t = t + data['deltat']


def main():
    """
    Main function
    two args req, one optional 
    --velocity (required)
    --angle (required)
    --height(optional, set default to 1.2 meters)
    :return: Nothing
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Assignment 5: Projectile motion")
    parser.add_argument("--velocity", "-v", action="store", dest="velocity", type=float, required=True, help="Initial velocity in m/s")
    parser.add_argument("--angle", "-a", action="store", dest="angle", type=float, required=True, help="Angle of Projectile")
    parser.add_argument("--height", "-hi", action="store", dest="height", type=float, default=1.2, help="Height in meters")
    args = parser.parse_args()
    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['init_height'] = args.height   # y-axis
    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle       # degrees
    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
#     plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)
