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
import os

import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from datapipe.io import images

class BenchmarkPlotsContainer(gtk.Box):

    def __init__(self, input_directory_path):

        super(BenchmarkPlotsContainer, self).__init__(orientation=gtk.Orientation.VERTICAL, spacing=6)

        self.input_directory_path = input_directory_path

        # Box attributes ##############

        self.set_border_width(18)

        # Matplotlib ##################

        self.fig = plt.figure()

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

        # Fill the dict ###############
        
        text  = "File: {}\n\n".format(file_path)
        text += "Event ID: {}\n".format(fits_metadata_dict["event_id"])
        text += "Tel ID: {}\n".format(fits_metadata_dict["tel_id"])
        text += "NPE: {}\n".format(fits_metadata_dict["npe"])
        text += "MC Energy: {} {}\n".format(fits_metadata_dict["mc_energy"], fits_metadata_dict["mc_energy_unit"])

        # Update the widget ###########

        self.clear_figure()

        ax = self.fig.add_subplot(111)

        x_list = range(90)
        y_list = [fits_metadata_dict["npe"] for x in x_list]

        ax = self.fig.add_subplot(111)
        ax.plot(x_list, y_list)

        self.fig.canvas.draw()


    def clear_figure(self):
        self.fig.clf()
        self.fig.canvas.draw()
