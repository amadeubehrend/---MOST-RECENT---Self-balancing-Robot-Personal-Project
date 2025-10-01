import lgpio
import time

# --- Hardware Pin Definitions ---
DIR_PIN = 21
STEP_PIN = 20
ENABLE_PIN = 22 # The pin connected to the driver's EN pin
GPIO_CHIP = 0

# --- Test Parameters ---
STEPS_PER_REVOLUTION = 1600
TEST_SPEED_RPS = 1 # Revolutions Per Second
TEST_DURATION_S = 2 # Seconds

h = None
try:
    # Get a handle to the GPIO chip
    h = lgpio.gpiochip_open(GPIO_CHIP)

    # Set pin modes
    lgpio.gpio_claim_output(h, DIR_PIN)
    lgpio.gpio_claim_output(h, STEP_PIN)
    lgpio.gpio_claim_output(h, ENABLE_PIN)

    print("GPIO initialized. Enabling driver...")
    lgpio.gpio_write(h, ENABLE_PIN, 0) # Set LOW to enable driver
    time.sleep(0.1) # Give driver a moment to wake up

    # Test forward direction
    print(f"Testing motor FORWARD for {TEST_DURATION_S} seconds...")
    lgpio.gpio_write(h, DIR_PIN, 0) # Set direction
    frequency = TEST_SPEED_RPS * STEPS_PER_REVOLUTION
    lgpio.tx_pwm(h, STEP_PIN, frequency, 50) # Start motor
    time.sleep(TEST_DURATION_S)
    lgpio.tx_pwm(h, STEP_PIN, 0, 0) # Stop motor
    time.sleep(1)

    # Test reverse direction
    print(f"Testing motor REVERSE for {TEST_DURATION_S} seconds...")
    lgpio.gpio_write(h, DIR_PIN, 1) # Change direction
    lgpio.tx_pwm(h, STEP_PIN, frequency, 50) # Start motor
    time.sleep(TEST_DURATION_S)
    lgpio.tx_pwm(h, STEP_PIN, 0, 0) # Stop motor

    print("\nTest complete.")

finally:
    if h:
        print("Disabling driver and cleaning up GPIO.")
        lgpio.gpio_write(h, ENABLE_PIN, 1) # Set HIGH to disable
        lgpio.gpiochip_close(h)