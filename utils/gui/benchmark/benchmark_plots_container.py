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

import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class BenchmarkPlotsContainer(gtk.Box):

    def __init__(self, images_list_model):

        super(BenchmarkPlotsContainer, self).__init__(orientation=gtk.Orientation.VERTICAL, spacing=6)

        self.set_border_width(18)


        # Matplotlib

        # TODO: plot nb d'annonces ajoutées (pour chaque catégories) par jour
        # TODO: plot nb sites web visités par jour (full et partial)
        # TODO: plot nb de candidatures envoyées
        x_list = range(90)
        y_list = [0 for x in x_list]

        today = datetime.date.today()
        day_interval = datetime.timedelta(days=1)

        for i in x_list:
            date_str = datetime.date.isoformat(today - i * day_interval)
            y_list[i] = 0

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x_list, y_list)


        # Scrolled window

        scrolled_window = gtk.ScrolledWindow()
        self.pack_start(scrolled_window, expand=True, fill=True, padding=0)

        canvas = FigureCanvas(fig)
        scrolled_window.add_with_viewport(canvas)

        # Label

        num_job_adverts = 0
        label = gtk.Label(label="{} job adverts registred".format(num_job_adverts))
        self.pack_start(label, expand=False, fill=False, padding=0)

