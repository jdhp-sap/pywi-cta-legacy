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

TREE_VIEW_COLUMN_LABEL_LIST = ["Url", "Tooltip", "File name", "Event ID", "Tel ID", "MC energy", "NPE"]

class ImagesListView(gtk.TreeView):

    def __init__(self, liststore, edit_container):
        """
        ...
        """

        super(ImagesListView, self).__init__(liststore)

        self.edit_container = edit_container

        # Creating the treeview, making it use the filter as a model, and
        # adding the columns
        for column_index, column_title in enumerate(TREE_VIEW_COLUMN_LABEL_LIST):
            renderer = gtk.CellRendererText()

            column = gtk.TreeViewColumn(column_title, renderer, text=column_index)

            column.set_resizable(True)       # Let the column be resizable

            if column_title == "NPE":
                renderer.set_property("ellipsize", pango.EllipsizeMode.END)
                renderer.set_property("ellipsize-set", True)

            if column_title in ("Url", "Tooltip"):
                column.set_visible(False) # Hide the "url" column (this column should not be displayed but is required for tooltip and webbrowser redirection)

            if column_title == "File name":
                column.set_sort_column_id(2)
            elif column_title == "Event ID":
                column.set_sort_column_id(3)
            elif column_title == "Tel ID":
                column.set_sort_column_id(4)
            elif column_title == "MC energy":
                column.set_sort_column_id(5)
            elif column_title == "NPE":
                column.set_sort_column_id(6)

            self.append_column(column)

        self.set_tooltip_column(1)  # set the tooltip

        # Connect to the "changed" signal (simple click)
        select = self.get_selection()
        select.connect("changed", self.treeViewSelectionChangedCallBack)

        # Connect to the "row-activated" signal (double click)
        self.connect("row-activated", treeview_double_click_cb)


    def treeViewSelectionChangedCallBack(self, selection):
        self.edit_container.clearCallBack()


def treeview_double_click_cb(tree_view, tree_path, tree_view_column):
    """Inspired from http://stackoverflow.com/questions/17109634/hyperlink-in-cellrenderertext-markup"""
    model = tree_view.get_model()
    url = model[tree_path][0]
    webbrowser.open(url)

