import board
import adafruit_mpu6050
import time

# --- CALIBRATION SCRIPT ---

try:
    i2c = board.I2C()
    mpu = adafruit_mpu6050.MPU6050(i2c)
    print("MPU-6050 Found! Calibrating...")
except Exception as e:
    print("MPU-6050 not found! Check wiring.", e)
    exit()

ax_offset = 0
ay_offset = 0
az_offset = 0
gx_offset = 0
gy_offset = 0
gz_offset = 0
num_readings = 200

print("Place the robot in a stable, level position. Calibration will begin in 3 seconds...")
time.sleep(3)
print("Calibrating...")

for _ in range(num_readings):
    ax, ay, az = mpu.acceleration
    gx, gy, gz = mpu.gyro
    ax_offset += ax
    ay_offset += ay
    az_offset += az
    gx_offset += gx
    gy_offset += gy
    gz_offset += gz
    time.sleep(0.01)

ax_offset /= num_readings
ay_offset /= num_readings
az_offset /= num_readings # You may not need this one
gx_offset /= num_readings
gy_offset /= num_readings
gz_offset /= num_readings

print("\nCalibration Complete. Add these offsets to your main script:")
print(f"AX_OFFSET = {ax_offset}")
print(f"AY_OFFSET = {ay_offset}")
print(f"AZ_OFFSET = {az_offset}")
print(f"GX_OFFSET = {gx_offset}")
print(f"GY_OFFSET = {gy_offset}")
print(f"GZ_OFFSET = {gz_offset}")