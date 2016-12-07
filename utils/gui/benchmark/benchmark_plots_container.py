# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
See: http://gtk3-matplotlib-cookbook.readthedocs.org/en/latest/
     http://matplotlib.org/1.4.2/examples/user_interfaces/index.html
"""

from gi.repository import Gtk as gtk

import datetime
import math
import os

import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from datapipe.io import images

###############################################################################

DEFAULT_COLOR_MAP = "gnuplot2" # "gray"

# histogram types : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HISTOGRAM_TYPE = 'bar'

#IMAGE_INTERPOLATION = 'bilinear'   # "smooth" map
IMAGE_INTERPOLATION = 'nearest'    # "raw" (non smooth) map

###############################################################################

class BenchmarkPlotsContainer(gtk.Box):

    def __init__(self, input_directory_path):

        super(BenchmarkPlotsContainer, self).__init__(orientation=gtk.Orientation.VERTICAL, spacing=6)

        self.input_directory_path = input_directory_path

        # Box attributes ##############

        self.set_border_width(18)

        # Matplotlib ##################

        self.fig = plt.figure()

        self.color_map = DEFAULT_COLOR_MAP
        self.show_color_bar = True

        # Scrolled window #############

        scrolled_window = gtk.ScrolledWindow()
        self.pack_start(scrolled_window, expand=True, fill=True, padding=0)

        canvas = FigureCanvas(self.fig)
        scrolled_window.add_with_viewport(canvas)

    
    def selection_changed_callback(self, file_name):
        file_path = os.path.join(self.input_directory_path, file_name)

        # Read the selected file #########

        fits_images_dict, fits_metadata_dict = images.load_benchmark_images(file_path)

        input_img = fits_images_dict["input_image"]
        reference_img = fits_images_dict["reference_image"]

        if input_img.ndim != 2:
            raise Exception("Unexpected error: the input FITS file should contain a 2D array.")

        if reference_img.ndim != 2:
            raise Exception("Unexpected error: the input FITS file should contain a 2D array.")

        # Update the widget ###########

        self.clear_figure()

        ax1 = self.fig.add_subplot(241)
        ax2 = self.fig.add_subplot(242)
        ax3 = self.fig.add_subplot(243)
        ax4 = self.fig.add_subplot(244)
        ax5 = self.fig.add_subplot(245)
        ax6 = self.fig.add_subplot(246)
        ax7 = self.fig.add_subplot(247)
        ax8 = self.fig.add_subplot(248)

        #self._draw_image(ax1, input_img)
        #self._draw_image(ax2, reference_img)
        self._draw_histogram(ax5, input_img)
        self._draw_histogram(ax6, reference_img)

        self.fig.canvas.draw()


    def clear_figure(self):
        self.fig.clf()
        self.fig.canvas.draw()


    def _draw_histogram(self, axis, image_array):

        #axis.set_title(self.file_path)
        bins = math.ceil(image_array.max() - image_array.min())
        print(bins)

        # nparray.ravel(): Return a flattened array.
        values, bins, patches = axis.hist(image_array.ravel(),
                                          histtype=HISTOGRAM_TYPE,
                                          bins=bins,
                                          #range=(0., 255.),
                                          fc='k',
                                          ec='k')

        axis.set_xlim([image_array.min(), image_array.max()])


    def _draw_image(self, axis, image_array):

            if image_array.ndim == 1:
                image_array = np.tile(image_array, (256, 1))  # TODO ?
                axis.get_yaxis().set_visible(False)

            im = axis.imshow(image_array,
                             origin='lower',
                             interpolation=IMAGE_INTERPOLATION,
                             cmap=self.color_map)

            #axis.set_axis_off()

            if self.show_color_bar:
                plt.colorbar(im) # draw the colorbar
