#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
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

__all__ = ['count_simtel_events',
           'list_simtel_content',
           'show_image']

import argparse

import ctapipe
import ctapipe.visualization
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt

###############################################################################

def count_simtel_events(simtel_file_path):
    """
    Count the number of events per telescope in a simtel file.

    Returns the number of events per telescope and the total number of events.
    """

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    #
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path,
                                 allowed_tels=None,
                                 max_events=None)

    num_event_dict = {}   # Number of events per telescope
    total_num_events = 0  # Total number of events

    for event in source:
        total_num_events += 1

        for telescope_id in event["trig"]["tels_with_trigger"]:
            if telescope_id not in num_event_dict:
                num_event_dict[telescope_id] = 0
            num_event_dict[telescope_id] += 1

    return num_event_dict, total_num_events


def main_count_simtel_events():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    num_event_dict, total_num_events = count_simtel_events(simtel_file_path)

    print("Number of events per telescope:")
    for telescope_id, num_events in num_event_dict.items():
        print("- Telescope {:03}: {} event{}".format(telescope_id, num_events, "s" if num_events > 1 else ""))

    print()
    print("Total number of events:", total_num_events)


###############################################################################


def list_simtel_content(simtel_file_path):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path,
                                 allowed_tels=[1],  
                                 max_events=1)

    for event in source:
        print("Count:", event["count"])
        print("Trigger data:", event["trig"])
        print("Monte-Carlo shower data:", event["mc"])
        print("Raw data:", event["dl0"])

        #print("Simtel file path:", event.meta["hessio__input"])
        print("Pixel pos:", event.meta["pixel_pos"])
        #print("Max events:", event.meta["hessio__max_events"])

        print()


def main_list_simtel_content():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    list_simtel_content(simtel_file_path)


###############################################################################


def show_image(simtel_file_path, tel_num=1, channel=0, event_index=0):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path,
                                 allowed_tels=[tel_num],
                                 max_events=event_index+1)

    event_list = list(source)          # TODO
    event = event_list[event_index]    # TODO

    # INIT PLOT #############################################################

    x, y = event.meta.pixel_pos[tel_num]
    geom = ctapipe.io.CameraGeometry.guess(x, y)
    disp = ctapipe.visualization.CameraDisplay(geom, title='CT%d' % tel_num)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    disp.axes.set_title('CT{:03d}, event {:010d}'.format(tel_num, event.dl0.event_id))

    # DISPLAY TIME-VARYING EVENT ############################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    disp.image = data[:, ii]
    #    #disp.set_limits_percent(70)   # TODO help(disp.set_limits_percent)
    #    disp.set_limits_minmax(0, 400)
    #    plt.savefig('CT{:03d}_EV{:010d}_S{:02d}.png'.format(tel_num, event.dl0.event_id, ii))

    # DISPLAY INTEGRATED EVENT ##############################################

    #disp.image = event.dl0.tel[tel_num].adc_sums[channel]  # ctapipe 0.3.0
    disp.image = event.r0.tel[tel_num].adc_sums[channel]    # ctapipe 0.4.0
    #disp.set_limits_percent(70)        # TODO help(disp.set_limits_percent)
    disp.set_limits_minmax(0, 9000)
    plt.savefig('CT{:03d}_EV{:010d}.png'.format(tel_num, event.dl0.event_id))

    # PLOT ##################################################################

    plt.show()


def main_show_image():

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, default=1,
                        metavar="INTEGER",
                        help="The telescope number to query")

    parser.add_argument("--channel", "-c", type=int, default=0,
                        metavar="INTEGER",
                        help="The channel number to query")

    parser.add_argument("--event", "-e", type=int, default=0,
                        metavar="INTEGER",
                        help="The event to extract")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_index = args.event
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    show_image(simtel_file_path, tel_num, channel, event_index)


###############################################################################


def show_pe_image(simtel_file_path, tel_num=1, channel=0, event_index=0):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path,
                                 allowed_tels=[tel_num],
                                 max_events=event_index+1)

    event_list = list(source)          # TODO
    event = event_list[event_index]    # TODO

    # INIT PLOT #############################################################

    x, y = event.meta.pixel_pos[tel_num]
    geom = ctapipe.io.CameraGeometry.guess(x, y)
    disp = ctapipe.visualization.CameraDisplay(geom, title='CT%d' % tel_num)
    disp.enable_pixel_picker()
    disp.add_colorbar()

    disp.axes.set_title('CT{:03d}, event {:010d}'.format(tel_num, event.dl0.event_id))

    # DISPLAY TIME-VARYING EVENT ############################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    disp.image = data[:, ii]
    #    #disp.set_limits_percent(70)   # TODO help(disp.set_limits_percent)
    #    disp.set_limits_minmax(0, 400)
    #    plt.savefig('CT{:03d}_EV{:010d}_S{:02d}.png'.format(tel_num, event.dl0.event_id, ii))

    # DISPLAY INTEGRATED EVENT ##############################################

    #disp.image = event.dl0.tel[tel_num].adc_sums[channel]
    #disp.set_limits_percent(70)        # TODO help(disp.set_limits_percent)


    # TODO: check that (taken from https://github.com/tino-michael/tino_cta/blob/e6cc6db3e64135c9ac92bce2dae6e6f81a36096a/sandbox/show_ADC_and_PE_per_event.py)
    for jj in range(len(event.mc.tel[tel_num].photo_electrons)):
        #event.dl0.tel[tel_num].adc_sums[channel][jj] = event.mc.tel[tel_num].photo_electrons[jj]
        event.r0.tel[tel_num].adc_sums[channel][jj] = event.mc.tel[tel_num].photo_electrons[jj]
    signals2 = event.dl0.tel[tel_num].adc_sums[channel].astype(float)
    disp.image = signals2


    disp.set_limits_minmax(0, 9000)
    plt.savefig('CT{:03d}_EV{:010d}.png'.format(tel_num, event.dl0.event_id))

    # PLOT ##################################################################

    plt.show()


def main_show_pe_image():

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, default=1,
                        metavar="INTEGER",
                        help="The telescope number to query")

    parser.add_argument("--channel", "-c", type=int, default=0,
                        metavar="INTEGER",
                        help="The channel number to query")

    parser.add_argument("--event", "-e", type=int, default=0,
                        metavar="INTEGER",
                        help="The event to extract")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_index = args.event
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    show_pe_image(simtel_file_path, tel_num, channel, event_index)
