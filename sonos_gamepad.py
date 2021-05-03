import argparse
import logging
import sys
import time

import pygame
import soco


def main():
    try:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        pygame.init()

        # Parse arguments
        parser = argparse.ArgumentParser(description="Pause Sonos using a controller.")
        parser.add_argument("speaker_name", type=str, help="Sonos speaker name")
        args = parser.parse_args()

        # Find a plugged in controller. Throws exception if no controller found.
        js = pygame.joystick.Joystick(0)
        logging.info(f"Found a connected game controller.")

        # Search for the Sonos speaker with given name.
        logging.info(f"Searching for Sonos speaker named {args.speaker_name}...")
        device = soco.discovery.by_name(args.speaker_name)
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
            time.sleep(0.5)

    except KeyboardInterrupt:
        logging.info("Shutting down.")


if __name__ == "__main__":
    main()