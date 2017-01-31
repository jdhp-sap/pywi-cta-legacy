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

import common_functions as common

import datetime
import math
import numpy as np
import os
import time

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import LogNorm

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from datapipe.io import images
from datapipe.denoising import tailcut as tailcut_mod
from datapipe.denoising import wavelets_mrfilter as wavelets_mod
from datapipe.benchmark import assess as assess_mod

from ctapipe.utils import linalg

import astropy.units as u
from ctapipe.image.hillas import hillas_parameters_1 as hillas_parameters_1
from ctapipe.image.hillas import hillas_parameters_2 as hillas_parameters_2

from datapipe.image.kill_isolated_pixels import kill_isolated_pixels as scipy_kill_isolated_pixels

###############################################################################

DEFAULT_COLOR_MAP = plt.cm.gnuplot2  # plt.cm.OrRd # plt.cm.gray

# histogram types : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HISTOGRAM_TYPE = 'bar'

#IMAGE_INTERPOLATION = 'bilinear'   # "smooth" map
IMAGE_INTERPOLATION = 'nearest'    # "raw" (non smooth) map

###############################################################################

class BenchmarkPlotsContainer(gtk.Box):

    def __init__(self, input_directory_path):

        super(BenchmarkPlotsContainer, self).__init__(orientation=gtk.Orientation.VERTICAL, spacing=6)

        self.input_directory_path = input_directory_path
        self.current_file_path = None

        # Plot options ################

        self.plot_histogram = False
        self.plot_log_scale = False
        self.plot_ellipse_shower = False
        self.show_scores = True
        self.plot_perpendicular_hit_distribution = False
        self.kill_isolated_pixels_on_ref = False

        # Wavelets options ############

        self.kill_isolated_pixels = False
        self.offset_after_calibration = None
        self.input_image_scale = 'linear'

        # Box attributes ##############

        self.set_border_width(18)

        # Matplotlib ##################

        self.fig = plt.figure()

        self.color_map = DEFAULT_COLOR_MAP
        self.color_map.set_bad(color='black')   # Set to black pixels with value <= 0 in log scale (by default it's white). See http://stackoverflow.com/questions/22548813/python-color-map-but-with-all-zero-values-mapped-to-black

        self.show_color_bar = True

        # Plot histogram ##############

        self.plot_histogram_switch = gtk.Switch()
        self.plot_histogram_switch.connect("notify::active", self.plot_histogram_switch_callback)
        self.plot_histogram_switch.set_active(False)

        plot_histogram_label = gtk.Label(label="Plot histograms")

        # Plot log scale ##############

        self.plot_log_scale_switch = gtk.Switch()
        self.plot_log_scale_switch.connect("notify::active", self.plot_log_scale_switch_callback)
        self.plot_log_scale_switch.set_active(False)

        plot_log_scale_label = gtk.Label(label="Plot log scale")

        # Plot ellipse shower #########

        self.plot_ellipse_shower_switch = gtk.Switch()
        self.plot_ellipse_shower_switch.connect("notify::active", self.plot_ellipse_shower_switch_callback)
        self.plot_ellipse_shower_switch.set_active(False)

        plot_ellipse_shower_label = gtk.Label(label="Plot ellipse shower")

        # Plot perpendicular hit distribution

        self.plot_perpendicular_hit_distribution_switch = gtk.Switch()
        self.plot_perpendicular_hit_distribution_switch.connect("notify::active", self.plot_perpendicular_hit_distribution_switch_callback)
        self.plot_perpendicular_hit_distribution_switch.set_active(False)

        plot_perpendicular_hit_distribution_label = gtk.Label(label="Plot PHD")

        # Kill isolated pixels on ref #

        self.kill_isolated_pixels_on_ref_switch = gtk.Switch()
        self.kill_isolated_pixels_on_ref_switch.connect("notify::active", self.kill_isolated_pixels_on_ref_switch_callback)
        self.kill_isolated_pixels_on_ref_switch.set_active(False)

        kill_isolated_pixels_on_ref_label = gtk.Label(label="Kill isolated pixels on ref.")

        # Save plots ##################

        self.save_plots_button = gtk.Button(label="Save")
        self.save_plots_button.connect("clicked", self.save_plots_button_callback)

        # Wavelets options entry ######

        self.wavelets_options_entry = gtk.Entry()
        self.wavelets_options_entry.set_text("-K -k -C1 -m3 -s3 -n4")
        self.wavelets_options_entry.connect("activate", self.update_plots)  # call "print_text()" function when the "Enter" key is pressed in the entry

        # Kill isolated pixels ########

        self.kill_isolated_pixels_switch = gtk.Switch()
        self.kill_isolated_pixels_switch.connect("notify::active", self.kill_isolated_pixels_switch_callback)
        self.kill_isolated_pixels_switch.set_active(False)

        kill_isolated_pixels_label = gtk.Label(label="Kill isolated pixels")

        # Log image ###################

        self.log_image_switch = gtk.Switch()
        self.log_image_switch.connect("notify::active", self.log_image_switch_callback)
        self.log_image_switch.set_active(False)

        log_image_label = gtk.Label(label="Log image")

        # Fill the box container ######

        # Plot options box
        plot_options_horizontal_box = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children

        plot_options_horizontal_box.pack_start(plot_histogram_label, expand=False, fill=False, padding=0)
        plot_options_horizontal_box.pack_start(self.plot_histogram_switch, expand=False, fill=False, padding=0)

        plot_options_horizontal_box.pack_start(plot_log_scale_label, expand=False, fill=False, padding=0)
        plot_options_horizontal_box.pack_start(self.plot_log_scale_switch, expand=False, fill=False, padding=0)

        plot_options_horizontal_box.pack_start(plot_ellipse_shower_label, expand=False, fill=False, padding=0)
        plot_options_horizontal_box.pack_start(self.plot_ellipse_shower_switch, expand=False, fill=False, padding=0)

        plot_options_horizontal_box.pack_start(plot_perpendicular_hit_distribution_label, expand=False, fill=False, padding=0)
        plot_options_horizontal_box.pack_start(self.plot_perpendicular_hit_distribution_switch, expand=False, fill=False, padding=0)

        plot_options_horizontal_box.pack_start(kill_isolated_pixels_on_ref_label, expand=False, fill=False, padding=0)
        plot_options_horizontal_box.pack_start(self.kill_isolated_pixels_on_ref_switch, expand=False, fill=False, padding=0)

        plot_options_horizontal_box.pack_start(self.save_plots_button, expand=False, fill=False, padding=0)

        # Wavelet options box
        wavelets_options_horizontal_box = gtk.Box(orientation = gtk.Orientation.HORIZONTAL, spacing=6)   # 6 pixels are placed between children

        wavelets_options_horizontal_box.pack_start(self.wavelets_options_entry, expand=True, fill=True, padding=0)

        wavelets_options_horizontal_box.pack_start(kill_isolated_pixels_label, expand=False, fill=False, padding=0)
        wavelets_options_horizontal_box.pack_start(self.kill_isolated_pixels_switch, expand=False, fill=False, padding=0)

        wavelets_options_horizontal_box.pack_start(log_image_label, expand=False, fill=False, padding=0)
        wavelets_options_horizontal_box.pack_start(self.log_image_switch, expand=False, fill=False, padding=0)

        ###
        canvas = FigureCanvas(self.fig)

        self.pack_start(canvas, expand=True, fill=True, padding=0)
        self.pack_start(plot_options_horizontal_box, expand=False, fill=False, padding=0)
        self.pack_start(wavelets_options_horizontal_box, expand=False, fill=False, padding=0)


    def plot_histogram_switch_callback(self, data=None, param=None):
        if self.plot_histogram_switch.get_active():
            self.plot_histogram = True
        else:
            self.plot_histogram = False
        self.update_plots()


    def plot_log_scale_switch_callback(self, data=None, param=None):
        if self.plot_log_scale_switch.get_active():
            self.plot_log_scale = True
        else:
            self.plot_log_scale = False
        self.update_plots()


    def plot_ellipse_shower_switch_callback(self, data=None, param=None):
        if self.plot_ellipse_shower_switch.get_active():
            self.plot_ellipse_shower = True
        else:
            self.plot_ellipse_shower = False
        self.update_plots()


    def plot_perpendicular_hit_distribution_switch_callback(self, data=None, param=None):
        if self.plot_perpendicular_hit_distribution_switch.get_active():
            self.plot_perpendicular_hit_distribution = True
        else:
            self.plot_perpendicular_hit_distribution = False
        self.update_plots()


    def kill_isolated_pixels_on_ref_switch_callback(self, data=None, param=None):
        if self.kill_isolated_pixels_on_ref_switch.get_active():
            self.kill_isolated_pixels_on_ref = True
        else:
            self.kill_isolated_pixels_on_ref = False
        self.update_plots()


    def save_plots_button_callback(self, data=None, param=None):
        self.update_plots(save=True)


    def kill_isolated_pixels_switch_callback(self, data=None, param=None):
        if self.kill_isolated_pixels_switch.get_active():
            self.kill_isolated_pixels = True
        else:
            self.kill_isolated_pixels = False
        self.update_plots()


    def log_image_switch_callback(self, data=None, param=None):
        if self.log_image_switch.get_active():
            # Switch is "true"
            self.offset_after_calibration = 10   # TODO
            #self.input_image_scale = 'sqrt'
            self.input_image_scale = 'log'
        else:
            # Switch is on "false"
            self.offset_after_calibration = None   # TODO
            self.input_image_scale = 'linear'
        self.update_plots()
    

    def selection_changed_callback(self, file_name):
        self.current_file_path = os.path.join(self.input_directory_path, file_name)
        self.update_plots()


    def update_plots(self, data=None, save=False):        # data is for event callers

        if self.current_file_path is not None:
            # Read the selected file #########

            fits_images_dict, fits_metadata_dict = images.load_benchmark_images(self.current_file_path)

            input_img = fits_images_dict["input_image"]
            reference_img = fits_images_dict["reference_image"]
            pixels_position = fits_images_dict["pixels_position"]

            if input_img.ndim != 2:
                raise Exception("Unexpected error: the input FITS file should contain a 2D array.")

            if reference_img.ndim != 2:
                raise Exception("Unexpected error: the input FITS file should contain a 2D array.")

            if self.kill_isolated_pixels_on_ref:
                reference_img = scipy_kill_isolated_pixels(reference_img)

            # Tailcut #####################

            #input_img_copy = copy.deepcopy(input_img)
            input_img_copy = input_img.astype('float64', copy=True)

            tailcut = tailcut_mod.Tailcut()
            
            initial_time = time.perf_counter()
            tailcut_cleaned_img = tailcut.clean_image(input_img_copy,
                                                      high_threshold=10,
                                                      low_threshold=5,
                                                      kill_isolated_pixels=self.kill_isolated_pixels)
            tailcut_execution_time = time.perf_counter() - initial_time

            # Wavelets ####################

            #input_img_copy = copy.deepcopy(input_img)
            input_img_copy = input_img.astype('float64', copy=True)

            wavelets = wavelets_mod.WaveletTransform()

            option_string = self.wavelets_options_entry.get_text()
            print(option_string)
            
            initial_time = time.perf_counter()
            wavelets_cleaned_img = wavelets.clean_image(input_img_copy,
                                                        kill_isolated_pixels=self.kill_isolated_pixels,
                                                        input_image_scale=self.input_image_scale,
                                                        offset_after_calibration=self.offset_after_calibration,
                                                        verbose=True,
                                                        raw_option_string=option_string)
            wavelets_execution_time = time.perf_counter() - initial_time

            # Execution time ##############

            print("Tailcut execution time: ", tailcut_execution_time) # TODO
            print("Wavelets execution time: ", wavelets_execution_time) # TODO

            # Tailcut scores ##############

            tailcut_title_suffix = ""
            try:
                tailcut_score_tuple, tailcut_score_name_tuple = assess_mod.assess_image_cleaning(input_img,
                                                                                                 tailcut_cleaned_img,
                                                                                                 reference_img,
                                                                                                 benchmark_method="all")

                if self.show_scores:
                    tailcut_title_suffix += " ("
                    for name, score in zip(tailcut_score_name_tuple, tailcut_score_tuple):
                        if name == "e_shape":
                            tailcut_title_suffix += " Es="
                            tailcut_title_suffix += "{:.2e}".format(score)
                        elif name == "e_energy":
                            tailcut_title_suffix += " Ee="
                            tailcut_title_suffix += "{:.2e}".format(score)
                        elif name == "hillas_theta":
                            tailcut_title_suffix += " Th="
                            tailcut_title_suffix += "{:.2f}".format(score)
                    tailcut_title_suffix += " )"

                print("Tailcut:")
                for name in tailcut_score_name_tuple:
                    print("{:>20}".format(name), end=" ")
                print()
                for score in tailcut_score_tuple:
                    print("{:20.12f}".format(score), end=" ")
                print()
            except assess_mod.AssessError:
                print("Tailcut: ", str(assess_mod.AssessError))

            # Wavelets scores #############

            wavelets_title_suffix = ""
            try:
                wavelets_score_tuple, wavelets_score_name_tuple = assess_mod.assess_image_cleaning(input_img,
                                                                                                   wavelets_cleaned_img,
                                                                                                   reference_img,
                                                                                                   benchmark_method="all")

                if self.show_scores:
                    wavelets_title_suffix += " ("
                    for name, score in zip(wavelets_score_name_tuple, wavelets_score_tuple):
                        if name == "e_shape":
                            wavelets_title_suffix += " Es="
                            wavelets_title_suffix += "{:.2e}".format(score)
                        elif name == "e_energy":
                            wavelets_title_suffix += " Ee="
                            wavelets_title_suffix += "{:.2e}".format(score)
                        elif name == "hillas_theta":
                            wavelets_title_suffix += " Th="
                            wavelets_title_suffix += "{:.2f}".format(score)
                    wavelets_title_suffix += " )"

                print("Wavelets:")
                for name in wavelets_score_name_tuple:
                    print("{:>20}".format(name), end=" ")
                print()
                for score in wavelets_score_tuple:
                    print("{:20.12f}".format(score), end=" ")
                print()
            except assess_mod.AssessError:
                print("Wavelets: ", str(assess_mod.AssessError))

            # Update the widget ###########

            self.clear_figure()

            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax3 = self.fig.add_subplot(223)
            ax4 = self.fig.add_subplot(224)

            if self.plot_histogram:
                self._draw_histogram(ax1, input_img, "Input")
                self._draw_histogram(ax2, reference_img, "Reference")
                self._draw_histogram(ax3, tailcut_cleaned_img, "Tailcut" + tailcut_title_suffix)
                self._draw_histogram(ax4, wavelets_cleaned_img, "Wavelets" + wavelets_title_suffix)
            else:
                self._draw_image(ax1, input_img, "Input", pixels_position=pixels_position)
                self._draw_image(ax2, reference_img, "Reference", pixels_position=pixels_position)
                if self.plot_perpendicular_hit_distribution:
                    #bins = np.linspace(-0.04, 0.04, 41)
                    bins = np.linspace(-0.04, 0.04, 21)
                    common.plot_perpendicular_hit_distribution(ax3,
                                                               [reference_img, wavelets_cleaned_img],
                                                               pixels_position,
                                                               bins=bins,
                                                               label_list=["Ref.", "Cleaned"],
                                                               hist_type="step")
                    ax3.set_title("Perpendicular hit distribution")
                    ax3.set_xlabel("Distance to the shower axis (in meter)", fontsize=16)
                    ax3.set_ylabel("Photoelectrons", fontsize=16)
                else:
                    self._draw_image(ax3, tailcut_cleaned_img, "Tailcut" + tailcut_title_suffix, pixels_position=pixels_position)
                self._draw_image(ax4, wavelets_cleaned_img, "Wavelets" + wavelets_title_suffix, pixels_position=pixels_position)

                if self.plot_ellipse_shower:
                    try:
                        common.plot_ellipse_shower_on_image_meter(ax2, reference_img, pixels_position)
                    except Exception as e:
                        print(e)

                    if not self.plot_perpendicular_hit_distribution:
                        try:
                            # Show ellipse only if "perpendicular hit distribution" is off
                            common.plot_ellipse_shower_on_image_meter(ax3, tailcut_cleaned_img, pixels_position)
                        except Exception as e:
                            print(e)

                    try:
                        common.plot_ellipse_shower_on_image_meter(ax4, wavelets_cleaned_img, pixels_position)
                    except Exception as e:
                        print(e)

            plt.suptitle("{:.3f} TeV ({} photoelectrons in reference image) - Event {} - Telescope {}".format(fits_metadata_dict["mc_energy"], int(fits_metadata_dict["npe"]), fits_metadata_dict["event_id"], fits_metadata_dict["tel_id"]), fontsize=18)

            if save:
                output_file_path_base = "ev{}_tel{}".format(fits_metadata_dict["event_id"], fits_metadata_dict["tel_id"]) # TODO: add WT options

                if self.plot_histogram:
                    output_file_path_base += "_hist"

                if self.plot_log_scale:
                    output_file_path_base += "_log"

                ## Save in PDF
                #output_file_path = output_file_path_base + ".pdf"
                #print("Save", output_file_path)
                #plt.savefig(output_file_path, bbox_inches='tight')

                ## Save in SVG
                #output_file_path = output_file_path_base + ".svg"
                #print("Save", output_file_path)
                #plt.savefig(output_file_path, bbox_inches='tight')

                # Save in PNG
                output_file_path = output_file_path_base + ".png"
                print("Save", output_file_path)
                plt.savefig(output_file_path, bbox_inches='tight')
            else:
                self.fig.canvas.draw()


    def clear_figure(self):
        self.fig.clf()
        self.fig.canvas.draw()


    def _draw_image(self, axis, image_array, title, pixels_position=None):

        axis.axis('equal')

        # See http://matplotlib.org/examples/pylab_examples/pcolor_demo.html

        if pixels_position is None:
            dx, dy = 1, 1

            # generate 2 2d grids for the x & y bounds
            y, x = np.mgrid[slice(0, image_array.shape[0], dy), slice(0, image_array.shape[1], dx)]  # TODO !!!

            axis.set_xlabel("Pixel index", fontsize=12)
            axis.set_ylabel("Pixel index", fontsize=12)
        else:
            x, y = pixels_position[0], pixels_position[1]
            axis.set_xlabel("Pixel position (in meter)", fontsize=12)
            axis.set_ylabel("Pixel position (in meter)", fontsize=12)

        z_min, z_max = image_array.min(), image_array.max()

        if self.plot_log_scale:
            # See http://matplotlib.org/examples/pylab_examples/pcolor_log.html
            #     http://stackoverflow.com/questions/2546475/how-can-i-draw-a-log-normalized-imshow-plot-with-a-colorbar-representing-the-raw
            im = axis.pcolor(x, y, image_array, norm=LogNorm(vmin=0.01, vmax=image_array.max()), cmap=self.color_map)  # TODO: "vmin=0.01" is an arbitrary choice...
        else:
            im = axis.pcolor(x, y, image_array, cmap=self.color_map, vmin=z_min, vmax=z_max)

        if self.show_color_bar:
            plt.colorbar(im, ax=axis)

        axis.set_title(title)

        # IMSHOW DOESN'T WORK WITH PYTHON GTK3 THROUGH CAIRO ("NOT IMPLEMENTED ERROR") !
        #im = axis.imshow(image_array)
        #im = axis.imshow(image_array,
        #                 origin='lower',
        #                 interpolation=IMAGE_INTERPOLATION,
        #                 cmap=self.color_map)
        #axis.set_axis_off()
        #if self.show_color_bar:
        #    plt.colorbar(im) # draw the colorbar


    def _draw_histogram(self, axis, image_array, title):

        image_array_copy = image_array.astype('float64', copy=True)
        image_array_1d = image_array.ravel()

        vmin = image_array_1d.min()
        vmax = image_array_1d.max()

        #axis.set_title(self.file_path)
        bins = int(abs(math.ceil(vmax) - math.floor(vmin)))

        if (bins > 100) and self.plot_log_scale and (vmin > 0):  # TODO: workaround when vmin<0 !
            logx = True
            # Setup the logarithmic scale on the X axis
            vmin = np.log10(vmin)
            vmax = np.log10(vmax)
            bins = np.logspace(vmin, vmax, 100) # Make a range from 10**vmin to 10**vmax

            #positive_indices = (image_array_pos > 0)
            #negative_indices = (image_array_pos < 0)
        else:
            logx = False

        # nparray.ravel(): Return a flattened array.
        values, bins, patches = axis.hist(image_array_1d.ravel(),
                                          histtype=HISTOGRAM_TYPE,
                                          bins=bins,
                                          log=self.plot_log_scale,               # Set log scale on the Y axis
                                          #range=(0., 255.),
                                          alpha=0.5)

        if logx:
            axis.set_xscale("log")               # Activate log scale on X axis
        else:
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

        if not self.plot_log_scale:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        axis.set_title(title)

        axis.set_xlim([vmin, vmax + 1])    # TODO: ("+1") is to see the last bin. This line may cause problems when logx == True
        axis.set_ylim(ymin=0.1)            # TODO: it doesn't work, all bins equals to 1 are not visible because they are hidden in the axis

