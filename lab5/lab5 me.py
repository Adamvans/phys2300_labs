import argparse 

def main():
    """
    Main function
    two args req, one optional 
    --velocity (required)
    --angle (required)
    --height(optional, set default to 1.2 meters)
    :return: Nothing
    """
    parser = argparse.ArgumentParser(description="Demo")

    parser.add_argument("--velocity", "-v", action="store", dest="velocity", type=float, required=True, help="Initial velocity in m/s")

    parser.add_argument("--height", "-hi", action="store", dest="height", type=float, default=1.2, help="Height in meters")
    args = parser.parse_args()

    print(args.velocity, args.height)
    

if __name__ == '__main__':
    main()
    exit(0)