# lcd_1inch14.py
from machine import Pin, SPI, PWM
import framebuf
import time


class LCD_1inch14(framebuf.FrameBuffer):
    """
    Driver for 1.14" 240x135 RGB565 LCD (ST7789-like init) used on PicoGo / Pico LCD 1.14 boards.
    """

    def __init__(
        self,
        bl_pin=13,
        dc_pin=8,
        rst_pin=12,
        cs_pin=9,
        sck_pin=10,
        mosi_pin=11,
        spi_id=1,
        spi_baudrate=10_000_000,
        spi_polarity=0,
        spi_phase=0,
    ):
        self.width = 240
        self.height = 135

        # Pins
        self.bl_pin = bl_pin  # used by main (PWM), stored for convenience
        self.cs = Pin(cs_pin, Pin.OUT, value=1)
        self.rst = Pin(rst_pin, Pin.OUT, value=1)
        self.dc = Pin(dc_pin, Pin.OUT, value=1)

        # SPI
        self.spi = SPI(
            spi_id,
            baudrate=spi_baudrate,
            polarity=spi_polarity,
            phase=spi_phase,
            sck=Pin(sck_pin),
            mosi=Pin(mosi_pin),
            miso=None,
        )

        # Framebuffer
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

        # Common colors (NOTE: keep your original values even if naming looks swapped)
        self.red = 0x07E0
        self.green = 0x001F
        self.blue = 0xF800
        self.white = 0xFFFF
        self.black = 0x0000

        self.init_display()
    
    def setup_backlight(self,freq=1000, duty_u16=32768) -> PWM:
        pwm = PWM(Pin(self.bl_pin))
        pwm.freq(freq)
        pwm.duty_u16(duty_u16)  # max 65535
        return pwm
    
    def write_cmd(self, cmd: int) -> None:
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd & 0xFF]))
        self.cs(1)

    def write_data(self, data: int) -> None:
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([data & 0xFF]))
        self.cs(1)

    def reset(self) -> None:
        self.rst(1)
        time.sleep_ms(10)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(10)

    def init_display(self) -> None:
        """Initialize display controller."""
        self.reset()

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)

    def show(self) -> None:
        """Flush framebuffer to LCD."""
        # Column address set
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        # Row address set
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        # Memory write
        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
