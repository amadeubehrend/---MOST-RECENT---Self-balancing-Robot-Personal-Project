import lgpio
import time

# --- Configuration ---
# Which motor do you want to test?
# For the Right Motor, use the original pins.
# To test the Left Motor, you would need to know its pins.
# For now, this tests the pins we've defined for parallel operation.
STEP_PIN = 20  # BCM Pin for STEP signal
DIR_PIN = 21   # BCM Pin for DIR signal

# --- Physical Constants ---
STEPS_PER_REVOLUTION = 1600 # Your calibrated value
RPS = 1.0 # Run at a steady 1.0 Revolution Per Second

# --- Initialization ---
GPIO_CHIP = 0
h = None
try:
    h = lgpio.gpiochip_open(GPIO_CHIP)
    lgpio.gpio_claim_output(h, DIR_PIN)
    lgpio.gpio_claim_output(h, STEP_PIN)
except Exception as e:
    print(f"Hardware Error: {e}")
    exit()

# --- Main Program ---
print(f"Testing motor on STEP={STEP_PIN} and DIR={DIR_PIN}.")
print(f"Running at a constant {RPS} RPS. Press Ctrl+C to stop.")

# Calculate frequency and start PWM
frequency = RPS * STEPS_PER_REVOLUTION
lgpio.gpio_write(h, DIR_PIN, 1) # Set direction to clockwise
lgpio.tx_pwm(h, STEP_PIN, frequency, 50) # Start the pulses

try:
    # Let the motor run until you stop it
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping motor.")
finally:
    # Cleanup
    if h:
        lgpio.tx_pwm(h, STEP_PIN, 0, 0) # Stop pulses
        lgpio.gpiochip_close(h) # Release GPIO handle