from config import Config
from gui import Gui
from client import Client
from dualsense import Dualsense
import logging

HOST = "192.168.137.117"
PORT = 80
    
def main():
    # Initialize Connection
    client = Client(HOST, PORT)
    # Initialize Dualsense Controller
    dualsense = Dualsense(client, None)
    # Create GUI
    gui = Gui(client, dualsense)
    # Pass gui to dualsense to update window on events
    dualsense.gui = gui
    gui.mainloop()

    try:
        while True:
            pass  # Keep the script running to listen for events
    except KeyboardInterrupt:
        pass
    finally:
        ds.close()  # Close the controller connection
        gui.destroy() # Close GUI Window

if __name__ == "__main__":
    main()
    
