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

from gi.repository import GObject
from gi.repository import Gtk
import logging

from gettext import gettext as _

from globals import Globals

from util.decorators import Property
from gui import theme

import pages.choose
import pages.edit

from persistence.jokebook import Jokebook
from gui.lessonplanwidget import LessonPlanWidget

class Frame(Gtk.Box):
  
  def __init__(self):
    Gtk.Box.__init__(self)
    
    # Root Frame ###############################################################
    # Holds: Everything
    self.set_orientation(Gtk.Orientation.VERTICAL)

    # Application Header #######################################################
    # Holds: App logo, language box, lessons plan box    
    self.__header = self.__make_header()
    self.pack_start(self.__header, False, False, 0)    
    
    # Page Container ###########################################################
    # Holds: The currently open UI page
    self.__container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.pack_start(self.__container, True, True, 0)
    

    self.__page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.__container.pack_start(self.__page, True, True, 0)
    
    self.__page_class = None
    
    # Application Footer #######################################################
    # Holds: Task buttons
    self.__footer = self.__make_footer()
    self.__container.pack_start(self.__footer, False, False, 0)



  def __make_header(self):
    ret = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    
    # logo
    logo = Gtk.Image()
    logo.set_from_file(Globals.logo)
    ret.pack_start(logo, False, False, 0)
    
    # lesson plans
    lesson_plans = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    button = Gtk.Button(_('Lesson Plans'))
    button.set_size_request(200, -1)
    button.active = False
    button.connect('clicked', self.__do_clicked_lessonplans)
    lesson_plans.pack_start(button, True, True, 0)
    ret.pack_start(lesson_plans, True, True, 0)
    
    return ret
  
  
  
  def __make_footer(self):
    ret = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    button = Gtk.Button(_('Read Jokebooks'))
    button.connect('clicked', self.__do_clicked_read)
    self.__button_read = button

    ret.pack_start(button, False, False, 0)

    button = Gtk.Button(_('Make Jokebook'))
    button.connect('clicked', self.__do_clicked_make)
    self.__button_make = button
    ret.pack_start(button, False, False, 0)
    return ret
 

  
  @property
  def page_class(self):
    if self.__page_class is None:
      # say, for e.g. we're connecting to another activity and we haven't set a
      # default page yet
      self.__page_class = pages.choose.Choose
    return self.__page_class
 
 
  @Property
  def page(): 
    def get(self): return self.__page
    def set(self, value): 
      self.__page_class = type(value)
      #self.__page.clear()
      self.__page.pack_start(value, True, True, 0)

      # some rules for the buttons in the footer
      if not Globals.JokeMachineActivity.is_initiator \
         and type(value) is pages.choose.Choose:
        self.__button_read.set_visible(False)
        self.__button_make.set_visible(False)      
      elif not Globals.JokeMachineActivity.is_initiator:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)      
      elif type(value) is pages.choose.Choose:
        self.__button_read.set_visible(False)
        self.__button_make.set_visible(True)
      elif type(value) is pages.edit.Edit:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)
      elif type(value) is pages.preview.Preview:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)
      else:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)



  def __do_clicked_read(self, button):
    Globals.JokeMachineActivity.set_page(pages.choose.Choose)



  def __do_clicked_make(self, button):
    # create a new jokebook
    jokebook = Jokebook()
    jokebook.id = Globals.JokeMachineState.next_jokebook_id
    logging.info('Created new jokebook with id: %d' % jokebook.id)
    jokebook.owner = Globals.nickname
    Globals.JokeMachineState.jokebooks.append(jokebook)
    Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
 
 
  def __do_clicked_lessonplans(self, button):
    if button.active:
      button.set_label(_('Lesson Plans'))
      button.active = False
      Globals.JokeMachineActivity.set_page(pages.choose.Choose)
    else:
      button.set_label(_('Close Lessons'))
      button.active = True
      widget_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
      widget_box.pack_start(Gtk.Label(_("Lesson Plans:")), False, False, 0)

      lesson_plans = LessonPlanWidget(Globals.pwd)
      widget_box.pack_start(lesson_plans, True, True, 0)

      self.page = widget_box
      self.__button_read.set_visible(False)
      self.__button_make.set_visible(False)            
