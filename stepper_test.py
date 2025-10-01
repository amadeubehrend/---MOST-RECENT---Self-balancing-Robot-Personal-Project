from gpiozero import OutputDevice
from time import sleep

# Define the GPIO pins using gpiozero's OutputDevice class
# BCM pin numbers are used by default
DIR_PIN = OutputDevice(21)
STEP_PIN = OutputDevice(18)

# Define rotation direction constants
CW = 1  # Clockwise
CCW = 0 # Counter-clockwise

# Simple delay function to control speed
delay = 0.0005

try:
    # --- Turn Clockwise ---
    print("Turning Clockwise")
    DIR_PIN.on() # Set direction to Clockwise (HIGH = CW)

    # Run 200 steps, which is one full revolution for a 1.8-degree motor
    for _ in range(1600):
        STEP_PIN.on()  # Send a high pulse
        sleep(delay)
        STEP_PIN.off() # Send a low pulse
        sleep(delay)

    sleep(1) # Pause for a second

    # --- Turn Counter-Clockwise ---
    print("Turning Counter-Clockwise")
    DIR_PIN.off() # Set direction to Counter-clockwise (LOW = CCW)

    for _ in range(1600):
        STEP_PIN.on()
        sleep(delay)
        STEP_PIN.off()
        sleep(delay)

    print("Test complete.")

except KeyboardInterrupt:
    print("Program stopped.")

# No GPIO.cleanup() is needed. 
# The gpiozero library handles this automatically when the script ends.