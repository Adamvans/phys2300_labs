from vpython import *
from math import sin, cos
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
    scene.x = -1
    # Set background: floor, table, etc
    box(pos = vector(0,0,0), length=200, height=100, width=1)


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(pos=vector(-25, data['init_height'], 0),
                        radius=1, color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position
    ball.velocity=vector(0,5,0)
    # Animate


def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    pass


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
#    set_scene(data)
    # 2) No Drag Animation
#    motion_no_drag(data)
    # 3) Drag Animation
#     motion_drag(data)
    # 4) Plot Information: extra credit
#     plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)
