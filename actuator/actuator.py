
from SSD1305 import SSD1305
from machine import SPI, Pin
from neopixel import NeoPixel
import time
import math


class Actuator:

    def __init__(self):
        self._spi = SPI(1, baudrate=25000000, sck = Pin(18), mosi = Pin(19), polarity = 0, phase = 0)
        self._neoPixel = NeoPixel(Pin(4), 12, timing = True)
        self._display = SSD1305(self._spi, dc=Pin(5), cs=Pin(21), rst=Pin(22))
        self._fanPin = Pin(27, Pin.OUT, value = 0)

    def flourish(self):
        self.fan = 1
        self.showSplash()
        self.testNeopixels()

        self.display.clear()
        self.fan = 0
        self.display.display()
        

    def showSplash(self):
        with open('splash.mono', 'rb') as f:
            bitmap = f.read()
        
        self.display.drawXBitmap(0, 0, bitmap, 128, 64, 1)
        self.display.display()

    def pulseNeopixels(self, c, delay = .007):

        np = self.np
        n = np.n
        i = 0.0

        while i < math.pi:
            s = math.sin(i)
            d = [int(x * s) for x in c]
            for j in range(n):
                np[j] = d
            np.write()
            i += .05
            time.sleep(delay)



    def testNeopixels(self):
        np = self.np
        n = np.n

        self.pulseNeopixels((255,0,0))
        self.pulseNeopixels((0,255,0))
        self.pulseNeopixels((0,0,255))

        for j in range(3):
            d = (0,0,0)
            for q in range(15):
                d = (q * 10, q * 10, q * 10)
                for k in range(n):
                    i = (k + j) % n
                    if k % 3 == 0:
                        np[i] = d
                np.write()
                time.sleep(.008)

        for j in range(26):
            for i in range(n):
                np[i] = [max(x - 10,0) for x in np[i]]
            np.write()
            time.sleep(.015)

    @property
    def fan(self):
        return self._fanPin()

    @fan.setter
    def fan(self, f):
        self._fanPin(f)

    @property
    def np(self):
        return self._neoPixel

    @property
    def display(self):
        return self._display
