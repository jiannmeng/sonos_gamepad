import argparse
import logging
import sys
import time

import pygame
import soco

PLAY_OR_PAUSE = [0, 3] # Xbox: A or Y
PLAY = [2]          # Xbox: X
PAUSE = [1]         # Xbox: B


def main():
    try:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        pygame.init()

        # Parse arguments
        parser = argparse.ArgumentParser(description="Pause Sonos using a controller.")
        parser.add_argument("-n", "--name", type=str, help="Sonos speaker name")
        args = parser.parse_args()

        # Find a plugged in controller. Throws exception if no controller found.
        js = pygame.joystick.Joystick(0)
        logging.info(f"Found a connected game controller.")

        # Search for the Sonos speaker with given name.
        device = None
        while not device:
            if not args.name:
                args.name = input("Enter Sonos speaker name to control: ")
            logging.info(f"Searching for Sonos speaker named {args.name}...")
            device = soco.discovery.by_name(args.name)
            if not device:
                print(f"Sonos speaker {args.name} not found.")
                args.name = None
        logging.info(f"Sonos speaker found. Ready to receive input.")
        
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN:
                    logging.info("Button pressed.")

                    logging.info("Querying Sonos state...")
                    cti = device.get_current_transport_info()["current_transport_state"]
                    status = cti
                    logging.info(f"Sonos status is {status}.")

                    if status == "PLAYING":
                        logging.info("Sending PAUSE to speaker...")
                        device.pause()
                    else:
                        logging.info("Sending PLAY to speaker...")
                        device.play()

                elif event.type == pygame.JOYHATMOTION:
                    logging.info("D-pad pressed.")

                    x, y = event.dict['value']
                    if x < 0 or y < 0:
                        device.volume -= 5
                        logging.info(f"Volume reduced to {device.volume}.")
                    elif x > 0 or y > 0:
                        device.volume += 5
                        logging.info(f"Volume increased to {device.volume}.")
                    
            time.sleep(0.5)

    except KeyboardInterrupt:
        logging.info("Shutting down.")


if __name__ == "__main__":
    main()
