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


import os
from gi.repository import Gtk
from gi.repository import Pango
import logging
from gettext import gettext as _

from globals import Globals
from gui.page import Page
from gui import theme
from gui.canvaslistbox import CanvasListBox

from pages.joke import JokeViewer

import pages.edit


class Preview(Page):
  
  def __init__(self, jokebook):
    Page.__init__(self)
    
    preview_box = CanvasListBox()
    
    # cover
    cover = self.make_listrow()
    cover.props.orientation= Gtk.Orientation.VERTICAL

    cover.pack_start(Gtk.Label('"' + (jokebook.title or '')+ '" ' +
        _('started by') + ' ' + (jokebook.owner or '')), False, False, 0)

    cover_picture = self.make_imagebox(jokebook, 'image', 480, 360, False)    
    cover.pack_start(cover_picture, False, False, 0)

    preview_box.pack_start(cover, False, False, 0)
    
    # jokes
    for joke in jokebook.jokes:
      list_row = self.make_listrow(JokeViewer(joke, jokebook.title))
      preview_box.pack_start(list_row, False, False, 0)
    self.pack_start(preview_box, True, True, 0)
    
    button = Gtk.Button(_('Edit'))
    button.connect('clicked', self.__do_clicked_edit, jokebook)    
    self.pack_start(button, False, False, 0)

  
  def __do_clicked_edit(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
 
 
 
