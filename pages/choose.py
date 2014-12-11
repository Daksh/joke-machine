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

from gui.canvaslistbox import CanvasListBox

from globals import Globals
from gui.page import Page
from gui import theme

import pages.cover
import pages.edit

#from persistence.jokemachinestate import JokeMachineState
#from persistence.jokebook import Jokebook

class Choose(Page):

  def __init__(self):
    Page.__init__(self)

    # page title
    self.pack_start(Gtk.Label(_('Choose a Jokebook to read:')), False, False, 0)
    
    # list of Jokebooks 
    allow_edit = Globals.JokeMachineActivity.is_initiator
    jokebooks_div = CanvasListBox()
    for jokebook in Globals.JokeMachineState.jokebooks:
      jokebooks_div.pack_start(self.__make_jokebook_div(jokebook, allow_edit), False, False, 0)
    self.pack_start(jokebooks_div, True, True, 0)


  def __do_clicked_title(self, control, event, jokebook):
    Globals.JokeMachineActivity.set_page(pages.cover.Cover, jokebook)
    

  def __do_clicked_edit(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)

    
  def __do_clicked_delete(self, button, jokebook):
    message = _('Are you sure you want to delete your ') 
    if jokebook.title is not None:
      message += '\'' + jokebook.title + '\' ' 
    message += _('jokebook ?')
    confirm = Gtk.MessageDialog(Globals.JokeMachineActivity, 
                                Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
                                Gtk.MESSAGE_QUESTION,
                                Gtk.BUTTONS_YES_NO,
                                message)
    response = confirm.run()
    confirm.hide()
    confirm.destroy()
    del confirm
    if response == Gtk.RESPONSE_YES:
      logging.debug('Deleting jokebook: %s' % jokebook.title)
      Globals.JokeMachineState.jokebooks.remove(jokebook)
      Globals.JokeMachineActivity.set_page(pages.choose.Choose)
      
    
  def __make_jokebook_div(self, jokebook, edit = False):
    list_row = self.make_listrow()

    # thumbnail
    thumbnail = self.make_imagebox(jokebook, 'image', 80, 60, False, 10)
    list_row.pack_start(thumbnail, False, False, 0)

    # title
    title = Gtk.Label((jokebook.title or '')+ "\n" + (jokebook.owner or ''))
    title_box = Gtk.EventBox()
    title_box.add(title)
    title_box.connect('button-press-event', self.__do_clicked_title, jokebook)    
    list_row.pack_start(title_box, True, True, 0) 
    
    # list_row.append(hippo.CanvasBox(box_width=theme.SPACER_HORIZONTAL)) # TODO spacer    
    
    # buttons
    if edit:
      button = Gtk.Button(_('Edit'))
      button.connect('clicked', self.__do_clicked_edit, jokebook)
      list_row.pack_start(button, False, False, 0)

      button = Gtk.Button(_('Delete'))
      button.connect('clicked', self.__do_clicked_delete, jokebook)
      list_row.pack_start(button, False, False, 0)

    return list_row


  def __make_column_div(self, width, content):
    ret = Gtk.Box()
    ret.append(content)
    return ret



