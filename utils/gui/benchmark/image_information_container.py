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

class ImageInformationContainer(gtk.Grid):

    def __init__(self, main_window, job_adverts_model):
        """
        ...
        """

        super(ImageInformationContainer, self).__init__()

        self.main_window = main_window
        self.job_adverts_model = job_adverts_model

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

        #######################################################################

        self.desc_textview.get_buffer().set_text("TODO...")

