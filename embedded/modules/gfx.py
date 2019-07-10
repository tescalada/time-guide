# Port of Adafruit GFX Arduino library to MicroPython.
# Based on: https://github.com/adafruit/Adafruit-GFX-Library
# Author: Tony DiCola (original GFX author Phil Burgess)
# License: MIT License (https://opensource.org/licenses/MIT)


class GFX:

    def __init__(self, width, height, pixel, hline = None, vline = None):
        # Create an instance of the GFX drawing class.  You must pass in the
        # following parameters:
        #  - width = The width of the drawing area in pixels.
        #  - height = The height of the drawing area in pixels.
        #  - pixel = A function to call when a pixel is drawn on the display.
        #            This function should take at least an x and y position
        #            and then any number of optional color or other parameters.
        #  You can also provide the following optional keyword argument to
        #  improve the performance of drawing:
        #  - hline = A function to quickly draw a horizontal line on the display.
        #            This should take at least an x, y, and width parameter and
        #            any number of optional color or other parameters.
        #  - vline = A function to quickly draw a vertical line on the display.
        #            This should take at least an x, y, and height paraemter and
        #            any number of optional color or other parameters.
        self.width = width
        self.height = height
        self._pixel = pixel
        # Default to slow horizontal & vertical line implementations if no
        # faster versions are provided.
        if hline is None:
            self.hline = self._slow_hline
        else:
            self.hline = hline
        if vline is None:
            self.vline = self._slow_vline
        else:
            self.vline = vline

    def _slow_hline(self, x0, y0, width, *args, **kwargs):
        # Slow implementation of a horizontal line using pixel drawing.
        # This is used as the default horizontal line if no faster override
        # is provided.
        if y0 < 0 or y0 > self.height or x0 < -width or x0 > self.width:
            return
        for i in range(width):
            self._pixel(x0+i, y0, *args, **kwargs)

    def _slow_vline(self, x0, y0, height, *args, **kwargs):
        # Slow implementation of a vertical line using pixel drawing.
        # This is used as the default vertical line if no faster override
        # is provided.
        if y0 < -height or y0 > self.height or x0 < 0 or x0 > self.width:
            return
        for i in range(height):
            self._pixel(x0, y0+i, *args, **kwargs)

    def circle(self, x0, y0, radius, *args, **kwargs):
        # Circle drawing function.  Will draw a single pixel wide circle with
        # center at x0, y0 and the specified radius.
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        self._pixel(x0, y0 + radius, *args, **kwargs)
        self._pixel(x0, y0 - radius, *args, **kwargs)
        self._pixel(x0 + radius, y0, *args, **kwargs)
        self._pixel(x0 - radius, y0, *args, **kwargs)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self._pixel(x0 + x, y0 + y, *args, **kwargs)
            self._pixel(x0 - x, y0 + y, *args, **kwargs)
            self._pixel(x0 + x, y0 - y, *args, **kwargs)
            self._pixel(x0 - x, y0 - y, *args, **kwargs)
            self._pixel(x0 + y, y0 + x, *args, **kwargs)
            self._pixel(x0 - y, y0 + x, *args, **kwargs)
            self._pixel(x0 + y, y0 - x, *args, **kwargs)
            self._pixel(x0 - y, y0 - x, *args, **kwargs)

    def fill_circle(self, x0, y0, radius, *args, **kwargs):
        # Filled circle drawing function.  Will draw a filled circule with
        # center at x0, y0 and the specified radius.
        self.vline(x0, y0 - radius, 2*radius + 1, *args, **kwargs)
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.vline(x0 + x, y0 - y, 2*y + 1, *args, **kwargs)
            self.vline(x0 + y, y0 - x, 2*x + 1, *args, **kwargs)
            self.vline(x0 - x, y0 - y, 2*y + 1, *args, **kwargs)
            self.vline(x0 - y, y0 - x, 2*x + 1, *args, **kwargs)