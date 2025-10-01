import time
import board
import adafruit_mpu6050
import math # We need this for the math functions

try:
    i2c = board.I2C()
    mpu = adafruit_mpu6050.MPU6050(i2c)
    print("MPU-6050 Found!")
except ValueError:
    print("MPU-6050 not found! Check wiring.")
    exit()

print("Tilt Angle Test. Press Ctrl+C to stop.")
print("-" * 30)

# Function to convert accelerometer values to degrees of tilt
def get_tilt_angles(accel_x, accel_y, accel_z):
    # Calculate Roll (rotation around X-axis)
    roll = math.atan2(accel_y, accel_z) * 180 / math.pi

    # Calculate Pitch (rotation around Y-axis)
    # The formula is slightly more complex to avoid issues when the sensor is vertical
    pitch = math.atan2(-accel_x, math.sqrt(accel_y * accel_y + accel_z * accel_z)) * 180 / math.pi

    return roll, pitch

try:
    while True:
        # Read the accelerometer data
        ax, ay, az = mpu.acceleration

        # Calculate the roll and pitch
        roll_deg, pitch_deg = get_tilt_angles(ax, ay, az)

        # Print the results
        print(f"Roll: {roll_deg:.2f} degrees")
        print(f"Pitch: {pitch_deg:.2f} degrees")
        print("-" * 30)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nTest stopped.")