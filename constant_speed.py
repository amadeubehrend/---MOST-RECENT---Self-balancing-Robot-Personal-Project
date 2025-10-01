from gpiozero import OutputDevice
from time import sleep

# --- User Configuration ---
# Set your target speed in Revolutions Per Second
TARGET_RPS = 7  # <--- CHANGE THIS VALUE TO TEST DIFFERENT SPEEDS

# --- Physical Constants (Do not change unless you change drivers/motors) ---
# This is the value you calibrated. It's for a 200-step motor with 1/8 microstepping.
STEPS_PER_REVOLUTION = 1600

# --- Hardware Pin Definitions (BCM numbering) ---
DIR_PIN = OutputDevice(21)
STEP_PIN = OutputDevice(18)

# --- Calculations ---
# Calculate the number of steps per second needed for the target RPS
steps_per_second = TARGET_RPS * STEPS_PER_REVOLUTION

# Calculate the delay between each step pulse.
# The time for one full step cycle (on/off) is 1 / steps_per_second.
# We have two sleep calls per cycle, so we divide the total time by 2.
if steps_per_second > 0:
    step_delay = (1 / steps_per_second) / 2
else:
    step_delay = 0

# --- Main Program ---
print(f"Running motor at a constant {TARGET_RPS} RPS.")
print(f"Calculated step delay: {step_delay * 1000:.4f} milliseconds")


# Set a direction (1 for Clockwise, 0 for Counter-Clockwise)
DIR_PIN.on()

try:
    if step_delay > 0:
        # This loop will run forever, pulsing the motor at a constant rate
        while True:
            STEP_PIN.on()
            sleep(step_delay)
            STEP_PIN.off()
            sleep(step_delay)
    else:
        print("Target RPS is 0. Motor will not move.")

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    print("Exiting.")
    # gpiozero automatically handles cleanup