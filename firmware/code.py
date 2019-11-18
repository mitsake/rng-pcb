import board
import busio
import sys
import touchio
import adafruit_ssd1306
from analogio import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
noise_in = AnalogIn(board.A0)
touch_r = touchio.TouchIn(board.A4)
touch_l = touchio.TouchIn(board.A3)

oled.fill(0)
oled.text("Right: pattern", 0, 0, 1)
oled.text("Left: noise values", 0, 10, 1)
oled.show()

while True:
    if touch_r.value:
        oled.fill(0)
        oled.show()
        for row in range(124):
            for col in range(32):
                last_digit = noise_in.value % 10
                if last_digit in [2, 4]:
                    oled.pixel(row, col, 0)
                    # print(0)
                elif last_digit in [6, 8]:
                    oled.pixel(row, col, 1)
                    # print(1)
        oled.show()

    if touch_l.value:
        oled.fill(0)
        oled.text("RNG -> serial", 0, 0, 1)
        oled.show()
        while True:
            out_byte = 0
            count = 0
            while count < 8:
                last_digit = noise_in.value % 10
                if last_digit in [2, 4]:
                    count = count + 1
                    #print(0)
                elif last_digit in [6, 8]:
                    mask = 1 << count
                    out_byte = out_byte ^ mask
                    count = count + 1
                    #print(1)
            sys.stdout.write(bytes([out_byte]))
                    
