# Import the library file we just created
from gpiozero_tm1637 import TM1637
import time
import datetime

# Define the GPIO pins you are using (BCM numbering)
CLK_PIN = 23
DIO_PIN = 24

# Initialize the display
display = TM1637(clk=CLK_PIN, dio=DIO_PIN)

print("Starting display test...")

display.set_brightness(7)

try:
    # Set the brightness (0-7). This now calls the corrected method.


    while True:
        # Get the current time from the Raspberry Pi
        now = datetime.datetime.now()
        
        # Format the time as a four-digit string (e.g., "2347" for 11:47 PM)
        time_str = now.strftime("%H%M")
        
        # Determine if the colon should be on or off for blinking effect
        # It will be on for even seconds and off for odd seconds
        should_blink = now.second % 2 == 0

        # Send the time string and the colon state to the display
        display.show(time_str, colon=should_blink)
        
        # Wait for one second before updating again
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    print("Test finished.")