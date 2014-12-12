# Copyright 2007 World Wide Workshop Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# If you find this activity useful or end up using parts of it in one of your
# own creations we would love to hear from you at info@WorldWideWorkshop.org !
#

from gi.repository import Gtk
from sugar3.graphics import style


# TODO- height seems bust
class CanvasListBox(Gtk.ScrolledWindow):

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        self._entries_div = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._entries_div.set_spacing(style.DEFAULT_SPACING)

        # props not set properly in constructor
        """
    self._entries_div.props.background_color=theme.COLOR_PAGE.get_int()
    self._entries_div.props.padding=10
    FIXME: background_color = modify_bg(Gtk.StateType.NORMAL, color)
    ^ get color.
    no idea about padding.

    """

        scroller = Gtk.ScrolledWindow()
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add_with_viewport(self._entries_div)
        self.show_all()

    def append(self, entry, *args):
        self._entries_div.append(entry, *args)
