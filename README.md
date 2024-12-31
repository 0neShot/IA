# Interdisziplinäres Arbeiten (IA)

This project demonstrates a robot control system integrating a PS5 DualSense controller with a Raspberry Pi Pico. It includes features for remote control and line-following capabilities using a PID controller.

## Features
- **Controller Integration:** Utilize a PS5 DualSense controller for robot operations.
- **Line Following:** Line tracking capability with a digital IR sensor array.
- **Modular Design:** Configurable settings for sensors, motors, and PID parameters.
- **Network Connection:** Seamless integration with local WiFi networks.
- **Custom GUI:** Easy-to-use interface for remote operations.


## Requirements
- **Hardware:** Raspberry Pi Pico, PS5 DualSense controller, IR sensor array, and DC motors.
- **Libraries:**
  - [PyDualSense](https://github.com/flok/pydualsense) - For controller support (Windows/Linux only).
  - [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - GUI framework.
  - Python's built-in libraries for GPIO and PWM control.

## Setup Instructions

### Step 1: Configure Settings
1. Open `config.py`.
2. Update settings to match your hardware, including:
   - Motor pins
   - Sensor pins
   - WiFi credentials.

### Step 2: Upload Files
1. Transfer the following files to the Raspberry Pi Pico:
   - `config.py`
   - `main.py`
   - `PiConnectionPC.py`
   - `motor_controll.py`
   - `PID.py`

### Step 3: Connect to Network
1. Power on the Raspberry Pi Pico.
2. Wait for the onboard LED to turn green, indicating a successful network connection.

### Step 4: Run the Controller
1. Execute `LocalPC.py` on your computer.
2. Ensure the controller vibrates to confirm a connection.

## Usage
1. Connect the robot to power.
2. Use the GUI to send commands via the DualSense controller.
3. Adjust PID parameters and motor speeds for optimal performance.

## Future Enhancements
- Expanded sensor support.
- Improved error handling and robustness.
- Enhanced documentation.
