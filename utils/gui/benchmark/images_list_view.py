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
from gi.repository import Pango as pango

import webbrowser

TREE_VIEW_COLUMN_LABEL_LIST = ["File name", "Event ID", "Tel ID", "MC energy", "NPE"]

class ImagesListView(gtk.TreeView):

    def __init__(self, liststore, callback_container):
        """
        ...
        """

        super(ImagesListView, self).__init__(liststore)

        self.callback_container = callback_container 

        # Creating the treeview, making it use the filter as a model, and
        # adding the columns
        for column_index, column_title in enumerate(TREE_VIEW_COLUMN_LABEL_LIST):
            renderer = gtk.CellRendererText()

            column = gtk.TreeViewColumn(column_title, renderer, text=column_index)

            column.set_resizable(True)       # Let the column be resizable

            if column_title == "File name":
                renderer.set_property("ellipsize", pango.EllipsizeMode.END)
                renderer.set_property("ellipsize-set", True)

            if column_title == "File name":
                column.set_sort_column_id(0)
            elif column_title == "Event ID":
                column.set_sort_column_id(1)
            elif column_title == "Tel ID":
                column.set_sort_column_id(2)
            elif column_title == "MC energy":
                column.set_sort_column_id(3)
            elif column_title == "NPE":
                column.set_sort_column_id(4)

            self.append_column(column)

        # Connect to the "changed" signal (simple click)
        select = self.get_selection()
        select.connect("changed", self.treeViewSelectionChangedCallBack)


    def treeViewSelectionChangedCallBack(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            file_name = model[treeiter][0]
            #event_id = model[treeiter][1]
            #tel_id = model[treeiter][2]
            #mc_energy = model[treeiter][3]
            #npe = model[treeiter][4]

            #text  = "File name: {}\n".format(file_name)
            #text += "Event ID: {}\n".format(event_id)
            #text += "Tel ID: {}\n".format(tel_id)
            #text += "MC energy: {}\n".format(mc_energy)
            #text += "NPE: {}\n".format(npe)

            self.callback_container.selection_changed_callback(file_name)

