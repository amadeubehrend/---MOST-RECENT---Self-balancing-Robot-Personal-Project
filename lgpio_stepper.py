import lgpio
import time

# --- Configuration & Constants ---
# We can go back to using GPIO 20, as lgpio is more flexible.
STEP_PIN = 20
DIR_PIN = 21

# Your calibrated value
STEPS_PER_REVOLUTION = 1600

# GPIO chip on all modern Raspberry Pis is 0
GPIO_CHIP = 0

# --- Initialization ---
try:
    # Get a handle to the GPIO chip
    h = lgpio.gpiochip_open(GPIO_CHIP)

    # Set pin modes
    lgpio.gpio_claim_output(h, DIR_PIN)
    lgpio.gpio_claim_output(h, STEP_PIN)
    print("lgpio initialized successfully. Ready to run motor.")

except Exception as e:
    print(f"Error initializing lgpio: {e}")
    print("This may need to be run with 'sudo'.")
    exit()

def set_motor_speed(rps):
    """
    Sets the motor speed using lgpio's PWM function.
    rps: Revolutions Per Second
    """
    # Set a direction (1 for Clockwise, 0 for Counter-Clockwise)
    lgpio.gpio_write(h, DIR_PIN, 1)

    if rps > 0:
        frequency = rps * STEPS_PER_REVOLUTION
        print(f"Setting frequency to {frequency:.2f} Hz for {rps} RPS.")
        # Start PWM: tx_pwm(handle, gpio, frequency, duty_cycle_percent)
        lgpio.tx_pwm(h, STEP_PIN, frequency, 50) # 50% duty cycle
    else:
        print("Setting frequency to 0 Hz (motor stopped).")
        # A frequency of 0 stops the PWM signal
        lgpio.tx_pwm(h, STEP_PIN, 0, 0)

# --- Main Program Logic ---
try:
    print("\n--- Running lgpio Test Sequence ---")

    print("\nRunning at 0.5 RPS for 3 seconds...")
    set_motor_speed(0.5)
    time.sleep(3)

    print("\nRunning at 2.0 RPS for 3 seconds...")
    set_motor_speed(2.0)
    time.sleep(3)

    print("\n--- Test Sequence Complete ---")

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    # This is a critical cleanup step for lgpio
    print("Stopping motor and cleaning up.")
    if 'h' in locals():
        try:
            # Turn off PWM before releasing the pin
            lgpio.tx_pwm(h, STEP_PIN, 0, 0)
            # Free all claimed pins
            lgpio.gpiochip_close(h)
        except Exception as e:
            print(f"Cleanup error: {e}")