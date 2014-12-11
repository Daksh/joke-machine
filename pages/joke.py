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
from gettext import gettext as _
import logging

from globals import Globals
from gui.page import Page
from gui import theme
from util.audioplayer import AudioPlayer

import pages.submit

import persistence.joke

class JokeViewer(Page):

  def __init__(self, joke, jokebook_title=''):
    Page.__init__(self)
    self.left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    joke_image = self.make_imagebox(joke, 'image', 320, 240, False)
    self.left.pack_start(joke_image, False, False, 0)
    self.left.pack_start(Gtk.Label(jokebook_title), False, False, 0)
    self.left.pack_start(Gtk.Label(_('Joke') + ' ' + str(joke.id)), False, False, 0)
    self.left.pack_start(Gtk.Label(_('By') + ' ' + str(joke.joker)), False, False, 0)

    # right column 
    self.right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.right.pack_start(Gtk.Label(_('Question')), False, False, 0)
    self.right.pack_start(self.make_bodytext(joke.text), False, False, 0)

    self.answer_box = Gtk.Box()
    self.answer_box.pack_start(Gtk.Label(_('Answer')), False, False, 0)
    self.answer_box.pack_start(self.make_bodytext(joke.answer), False, False, 0)    
    self.right.pack_start(self.answer_box, False, False, 0)

    self.pack_start(self.left, False, False, 0)
    self.pack_start(self.right, False, False, 0)



class Joke(Page):

  def __init__(self, jokebook, joke_id = 0):
    Page.__init__(self)

    # handle empty jokebook
    if len(jokebook.jokes) <= joke_id:
      self.append(self.make_bodytext(_('This Jokebook is empty')))
      if not Globals.JokeMachineActivity.is_initiator:
        button = Gtk.Button(_('Submit a Joke'))
        button.connect('clicked', self.__do_clicked_submit, jokebook, joke_id)        
        self.pack_start(button, False, False, 20)
      else:
        button = Gtk.Button(_('Add Jokes'))
        button.connect('clicked', self.__do_clicked_add, jokebook, joke_id)        
        self.pack_start(button, False, False, 20)
      return
      
    # the joke box
    joke = jokebook.jokes[joke_id]
    self.joke_box = JokeViewer(joke, jokebook.title)
    self.joke_box.answer_box.set_visible(False)

    # the navigation box
    self.navigation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

    # the answer button
    button = Gtk.Button(_('Answer'))
    button.connect('clicked', self.__do_clicked_answer, jokebook, joke_id)        
    self.navigation_box.pack_start(button, False, False, 0)
    self.joke_box.right.pack_start(self.navigation_box, False, False, 0)
    self.pack_start(self.joke_box, False, False, 0)


  # for forcing the joke into the answered state from page.submit
  def force_answer(self, jokebook, joke_id):
    self.__do_clicked_answer(None, jokebook, joke_id)


  def __do_clicked_answer(self, button, jokebook, joke_id):
    # play a sound if the jokebook has one
    player = AudioPlayer()
    if jokebook.sound_blob != None:
      player.raw = jokebook.sound_blob
    else: # default laugh
      logging.debug('Playing default sound: %s', Globals.laugh_uri)
      player.uri = Globals.laugh_uri
    player.play()        
    
    # show the answer
    self.joke_box.answer_box.set_visible(True)
    
    # reconfigure navigation box
    self.navigation_box.clear()
    
    # check if there are any more jokes left
    if len(jokebook.jokes) > joke_id + 1:
      button = Gtk.Button(_('Next'))
      button.connect('clicked', self.__do_clicked_next, jokebook, joke_id + 1)  
      self.navigation_box.pack_start(button, False, False, 0)      


    # only allow submitting a joke if activity is shared and you are the one joining
    if not Globals.JokeMachineActivity.is_initiator:
      button = Gtk.Button(_('Submit a Joke'))
      button.connect('clicked', self.__do_clicked_submit, jokebook, joke_id)        
      self.navigation_box.pack_start(button, False, False, 0)  
      
    
  def __do_clicked_add(self, button, jokebook, joke_id):
    page = Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
    tab = page.do_tab_clicked(pages.edit.EditJokes)
    tab.do_clicked_add_joke(None, jokebook)

  def __do_clicked_submit(self, button, jokebook, joke_id):
    Globals.JokeMachineActivity.set_page(pages.submit.Submit, jokebook, joke_id)


  def __do_clicked_next(self, button, jokebook, joke_id):
    Globals.JokeMachineActivity.set_page(pages.joke.Joke, jokebook, joke_id)
    
  
