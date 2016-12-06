#!/usr/bin/env python3
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
...
"""

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk

import argparse
#import fcntl  # TODO: use GtkApplication instead
import os
import sys

print(sys.path)

import benchmark_plots_container as benchmark_plots_container_mod
import images_list_view as images_list_view_mod
import image_information_container as image_information_container_mod

import images_list_model as images_list_model_mod

LOCK_FILENAME = ".lock"  # TODO: use GtkApplication instead

class MainWindow(gtk.Window):

    def __init__(self, input_directory_path):

        self.images_list_model = images_list_model_mod.ImagesListModel(input_directory_path)

        # Build the main window
        gtk.Window.__init__(self, title="Benchmark")
        self.maximize()
        self.set_border_width(4)

        notebook_container = gtk.Notebook()
        self.add(notebook_container)


        # Image information container #########################################

        # Images treeview
        self.images_treeview1 = images_list_view_mod.ImagesListView(self.images_list_model.liststore, None) # TODO!!!

        scrolled_images_treeview1 = gtk.ScrolledWindow()
        scrolled_images_treeview1.set_border_width(18)
        scrolled_images_treeview1.set_shadow_type(gtk.ShadowType.IN)
        scrolled_images_treeview1.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
        scrolled_images_treeview1.add(self.images_treeview1)

        # Information container
        self.information_container = image_information_container_mod.ImageInformationContainer(self, self.images_list_model)

        # Paned container
        image_information_paned_container = gtk.Paned(orientation=gtk.Orientation.VERTICAL)
        image_information_paned_container.add1(scrolled_images_treeview1)
        image_information_paned_container.add2(self.information_container)

        # The position in pixels of the divider (i.e. the default size of the top pane)
        image_information_paned_container.set_position(400)


        # Benchmark container #################################################

        # Images treeview
        self.images_treeview2 = images_list_view_mod.ImagesListView(self.images_list_model.liststore, None) # TODO!!!

        scrolled_images_treeview2 = gtk.ScrolledWindow()
        scrolled_images_treeview2.set_border_width(18)
        scrolled_images_treeview2.set_shadow_type(gtk.ShadowType.IN)
        scrolled_images_treeview2.set_policy(gtk.PolicyType.AUTOMATIC, gtk.PolicyType.ALWAYS)
        scrolled_images_treeview2.add(self.images_treeview2)

        # Benchmark plots container
        self.benchmark_plots_container = benchmark_plots_container_mod.BenchmarkPlotsContainer(self.images_list_model)

        # Paned container
        benchmark_paned_container = gtk.Paned(orientation=gtk.Orientation.VERTICAL)
        benchmark_paned_container.add1(scrolled_images_treeview2)
        benchmark_paned_container.add2(self.benchmark_plots_container)

        # The position in pixels of the divider (i.e. the default size of the top pane)
        benchmark_paned_container.set_position(400)


        #######################################################################

        image_information_label = gtk.Label(label="Image information")
        notebook_container.append_page(image_information_paned_container, image_information_label)

        benchmark_label = gtk.Label(label="Benchmark")
        notebook_container.append_page(benchmark_paned_container, benchmark_label)


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="GUI for datapipe benchmarks.")

    parser.add_argument("fileargs", nargs=1, metavar="DIRECTORY",
                        help="The directory containing input images (FITS files) used for the benchmark.")

    args = parser.parse_args()

    input_directory_path = args.fileargs[0]

    if not os.path.isdir(input_directory_path):
        raise Exception("{0} is not a directory.".format(input_directory_path))

    ###########################################################################

    # Acquire an exclusive lock on LOCK_FILENAME
    fd = open(LOCK_FILENAME, "w")  # TODO: use GtkApplication instead

#    try:  # TODO: use GtkApplication instead
#        # LOCK_EX = acquire an exclusive lock on fd
#        # LOCK_NB = make a nonblocking request
#        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # TODO: use GtkApplication instead
#
#        ###################################

    window = MainWindow(input_directory_path)

    window.connect("delete-event", gtk.main_quit) # ask to quit the application when the close button is clicked
    window.show_all()                             # display the window
    gtk.main()                                    # GTK+ main loop

        ###################################

#        # LOCK_UN = unlock fd
#        fcntl.flock(fd, fcntl.LOCK_UN)  # TODO: use GtkApplication instead
#    except IOError:  # TODO: use GtkApplication instead
#        #print(LOCK_FILENAME + " is locked ; another instance is running. Exit.")
#        dialog = gtk.MessageDialog(parent=None, flags=0, message_type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK, message_format="Another instance is running in the same directory")
#        dialog.format_secondary_text("Exit.")
#        dialog.run()
#        dialog.destroy()
#
#        sys.exit(1)


if __name__ == '__main__':
    main()

