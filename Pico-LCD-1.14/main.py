# main.py
from machine import Pin, PWM
import time
from lcd_1inch14 import LCD_1inch14

def draw_static_ui(lcd: LCD_1inch14) -> None:
    lcd.fill(lcd.white)

    lcd.text("Raspberry Pi Pico", 90, 40, lcd.red)
    lcd.text("PicoGo", 90, 60, lcd.green)
    lcd.text("Pico-LCD-1.14", 90, 80, lcd.blue)

    lcd.hline(10, 10, 220, lcd.blue)
    lcd.hline(10, 125, 220, lcd.blue)
    lcd.vline(10, 10, 115, lcd.blue)
    lcd.vline(230, 10, 115, lcd.blue)

    lcd.show()


def setup_keys():
    # A/B
    keyA = Pin(15, Pin.IN, Pin.PULL_UP)
    keyB = Pin(17, Pin.IN, Pin.PULL_UP)

    # D-pad like keys
    key2 = Pin(2, Pin.IN, Pin.PULL_UP)    # UP
    key3 = Pin(3, Pin.IN, Pin.PULL_UP)    # CTRL / MID
    key4 = Pin(16, Pin.IN, Pin.PULL_UP)   # LEFT
    key5 = Pin(18, Pin.IN, Pin.PULL_UP)   # DOWN
    key6 = Pin(20, Pin.IN, Pin.PULL_UP)   # RIGHT

    return keyA, keyB, key2, key3, key4, key5, key6


def set_button_box(lcd: LCD_1inch14, x, y, pressed: bool, label: str) -> None:
    if pressed:
        lcd.fill_rect(x, y, 20, 20, lcd.red)
        print(label)
    else:
        lcd.fill_rect(x, y, 20, 20, lcd.white)
        lcd.rect(x, y, 20, 20, lcd.red)


def main():
    lcd = LCD_1inch14()
    lcd.setup_backlight(duty_u16=32768)

    draw_static_ui(lcd)

    keyA, keyB, key2, key3, key4, key5, key6 = setup_keys()

    while True:
        set_button_box(lcd, 208, 12,  keyA.value() == 0, "A")
        set_button_box(lcd, 208, 103, keyB.value() == 0, "B")

        set_button_box(lcd, 37, 35,  key2.value() == 0, "UP")
        set_button_box(lcd, 37, 60,  key3.value() == 0, "CTRL")
        set_button_box(lcd, 12, 60,  key4.value() == 0, "LEFT")
        set_button_box(lcd, 37, 85,  key5.value() == 0, "DOWN")
        set_button_box(lcd, 62, 60,  key6.value() == 0, "RIGHT")

        lcd.show()

        # lille sleep så loopet ikke spammer SPI/CPU unødigt
        time.sleep_ms(20)


if __name__ == "__main__":
    main()
