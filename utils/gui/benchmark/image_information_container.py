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

from gi.repository import Gtk as gtk

import json
import os

from datapipe.io import images

class ImageInformationContainer(gtk.Grid):

    def __init__(self, input_directory_path):
        """
        ...
        """

        super(ImageInformationContainer, self).__init__()

        self.input_directory_path = input_directory_path

        # Make textview widget
        self.desc_textview = gtk.TextView()
        self.desc_textview.set_editable(False)

        # Image information
        self.desc_textview.set_wrap_mode(gtk.WrapMode.WORD)

        desc_scrolled_window = gtk.ScrolledWindow()
        desc_scrolled_window.set_border_width(3)
        desc_scrolled_window.set_shadow_type(gtk.ShadowType.OUT)
        desc_scrolled_window.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
        desc_scrolled_window.add(self.desc_textview)

        # The grid container
        self.set_border_width(18)

        # Set hexpand, vexpand, halign, valign
        # See https://developer.gnome.org/gtk3/stable/ch29s02.html
        desc_scrolled_window.set_hexpand(True)
        desc_scrolled_window.set_vexpand(True)

        # Add the widgets to the container
        self.attach(desc_scrolled_window, left=0, top=0, width=1, height=1)


    def selection_changed_callback(self, file_name):
        file_path = os.path.join(self.input_directory_path, file_name)

        # Read the selected file #########
        fits_images_dict, fits_metadata_dict = images.load_benchmark_images(file_path)

        # Fill the dict ###############
        text  = "File: {}\n\n".format(file_path)
        text += "Event ID: {}\n".format(fits_metadata_dict["event_id"])
        text += "Tel ID: {}\n".format(fits_metadata_dict["tel_id"])
        text += "NPE: {}\n".format(fits_metadata_dict["npe"])
        text += "MC Energy: {} {}\n".format(fits_metadata_dict["mc_energy"], fits_metadata_dict["mc_energy_unit"])

        # Update the widget
        self.desc_textview.get_buffer().set_text(text)
