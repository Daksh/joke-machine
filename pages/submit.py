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

from persistence.joke import Joke

import pages.joke
import pages.choose


class JokeEditor(Page):
  
  def __init__(self, joke):
    Page.__init__(self)
    
     # left column 
    self.left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    joke_image = self.make_imagebox(joke, 'image', 320, 240, True)
    self.left.pack_start(joke_image, False, False, 0)
    
    # right column 
    self.right.pack_start(Gtk.Label(_('Question')), False, False, 0)
    self.right.pack_start(self.make_textbox(joke, 'text'), False, False, 0)

    self.right.pack_start(Gtk.Label(_('Answer')), False, False, 0)

    self.right.pack_start(self.make_textbox(joke, 'answer'), False, False, 0)
    
    self.pack_start(self.left, False, False, 0)
    self.pack_start(self.right, True, True, 0)


class Submit(Page):
  
  def __init__(self, jokebook, last_joke=0): # last_joke is for 'back' button
    Page.__init__(self, spacing=10)

    # create a new joke
    joke = Joke() 
    joke.id = jokebook.next_joke_id
    logging.info('Created new joke with id: %d' % joke.id)
    joke.joker = Globals.nickname

    # info
    self.pack_start(self.make_field(_('Submission For:'), 250, jokebook, 'title', 300, False), False, False, 0)
    self.pack_start(self.make_field(_('Your Name:'),  250, joke, 'joker', 300, True), False, False, 0)

    # joke editor
    jokebox = JokeEditor(joke)        
    nav = Gtk.Box(Gtk.Orientation.HORIZONTAL)
    button = Gtk.Button(_('Submit'))
    button.connect('clicked', self.__do_clicked_submit, jokebook, joke)    

    nav.pack_start(button, False, False, 0)
    button = Gtk.Button(_('Back'))
    button.connect('clicked', self.__do_clicked_back, jokebook, last_joke)    

    nav.pack_start(button, False, False, 0)
    jokebox.right.pack_start(nav, False, False, 0)
    self.pack_start(jokebox, False, False, 0)


  def __do_clicked_back(self, button, jokebook, last_joke):
    joke_page = Globals.JokeMachineActivity.set_page(pages.joke.Joke, jokebook, last_joke)
    joke_page.force_answer(jokebook, last_joke) # force joke into answered state


  def __do_clicked_submit(self, button, jokebook, joke):

    Globals.JokeMachineActivity.set_page(pages.choose.Choose)
    
    # TODO -> Factor out of the page ? Should be transparent to UI layer ?
    if not Globals.JokeMachineActivity.is_shared:
      logging.error('pages.submit.Submit -> CANNOT SUBMIT WITHOUT A TUBE')
      return
    
    logging.debug('Submitting joke to remote')
    pickle = joke.dumps()
    Globals.JokeMachineActivity.tube.Submit(jokebook.id, pickle)
    logging.debug('Submitted joke to remote')
    
    
    
    

