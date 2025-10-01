# Summer 2025 Self-balancing Robot Project

## Overview
This project uses a Raspberry Pi, IMU sensor unit, two stepper motors, and an buck converter connected to a 14.8V Lipo battery to power everything.  Real-time sensor data from the Inertial Measuring Unit is used as input for a PID control loop by the Raspberry Pi.  This core software algorithm calculates the needed motor response which determines how fast and in which direciton the wheels need to turn to counteract falling.  The pi then sends Pulse With Modulation (PWM) signals to the motor drivers to control the speed of the stepper motors based on the frequency of the pulses.

## Robot Pictures
![Front View](Robot_front.png)
***
![Back view](Robot_back.png)
***
![Back view](Robot_top.png)

## Main Driver Code

```python
# proportional_driver.py
def set_motor_speed(rps):
    """
    Sets the motor speed using lgpio's PWM function.
    rps: Revolutions Per Second
    """
    if rps > 0:
        frequency = rps * STEPS_PER_REVOLUTION

        # Start PWM: tx_pwm(handle, gpio, frequency, duty_cycle_percent)
        lgpio.tx_pwm(h, STEP_PIN, frequency, 50) # 50% duty cycle
    else:

        # A frequency of 0 stops the PWM signal
        lgpio.tx_pwm(h, STEP_PIN, 0, 0)

# Initialization
try:
    i2c = board.I2C()
    mpu = adafruit_mpu6050.MPU6050(i2c)
    print("MPU-6050 sensor initialized successfully.")
except Exception as e:
    print(f"Error initializing MPU-6050: {e}")
    exit()

# Main Control Loop
print("Starting balancing loop... Press Ctrl+C to stop.")

try:
    while True:
        # This outer loop only calculates the target speed.
        start_time = time()
        current_time = time()
        delta_time = current_time - last_time

        # 1. Read sensor and calculate pitch
        raw_ax, raw_ay, raw_az = mpu.acceleration
        ax = raw_ax - AX_OFFSET
        ay = raw_ay - AY_OFFSET
        az = raw_az  # Assuming no offset needed for Z
        try:
            pitch = math.atan2(-ax, math.sqrt(ay * ay + az * az)) * 180 * 0.31830988618
        except ZeroDivisionError:
            continue

        # 2. PID Control Calculation
        error = pitch - TARGET_ANGLE
        derivative = (error - last_error) / delta_time if delta_time > 0 else 0.0
        pid_output_rps = Kp * error + Kd * derivative
        target_rps = min(MAX_RPS, abs(pid_output_rps))  # Limit to MAX_RPS

        # 3. Check if we are outside the dead zone
        if abs(error) > DEAD_ZONE:
            # Set motor direction
            if error > 0: lgpio.gpio_write(h, DIR_PIN, 1) 
            else: lgpio.gpio_write(h, DIR_PIN, 0)
            set_motor_speed(target_rps)
            motor_moving = True
            print(f"Pitch: {pitch:2f} | Target RPS: {target_rps:.2f}")
        else:
            # The robot is balanced, so do nothing and print status.
            if motor_moving:
                set_motor_speed(0)
                motor_moving = False
            print(f"Pitch: {pitch:.2f} | Status: Balanced")
        elapsed_time = time() - start_time
        sleep_time = LOOP_TIME - elapsed_time
        if sleep_time > 0:
            sleep(sleep_time)
        # Update last values for next iteration
        last_error = error
        last_time = current_time
