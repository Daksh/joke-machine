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

from util.decorators import Property

from pages.submit import JokeEditor
from pages.joke   import JokeViewer

import pages.preview
import persistence.joke



class PageSelector(Gtk.Box):
  
  def __init__(self, parent, **kwargs):
    Gtk.Box.__init__(self, **kwargs)
    self.__parent = parent

    # self.props.border = 1
    # self.props.border_color=theme.COLOR_TAB_ACTIVE.get_int()
    # self.props.background_color=theme.COLOR_PAGE.get_int()
    self.props.orientation=Gtk.Orientation.VERTICAL
    
    tab_box = Gtk.Box()
    self.__tab_1 = Gtk.Label(_('Edit Jokebook Cover'))
    self.__tab_1.page = EditInfo
    self.__tab_1.connect('button-press-event', self.__do_clicked_tab)    
    tab_box.pack_start(self.__tab_1, True, True, 0)

    self.__tab_2 = Gtk.Label(_("Edit My Jokes"))
    self.__tab_2.page = EditJokes
    self.__tab_2.connect('button-press-event', self.__do_clicked_tab)    

    tab_box.pack_start(self.__tab_2, True, True, 0)

    self.__tab_3 = Gtk.Label(_('Review Submitted Jokes'))
    self.__tab_3.page = EditReview
    self.__tab_3.connect('button-press-event', self.__do_clicked_tab)    
    tab_box.append(self.__tab_3, True, True, 0)
    self.pack_start(tab_box, False, False, 0)
    
    self.__page = Gtk.Box(Gtk.Orientation.VERTICAL)
    self.pack_start(self.__page, True, True, 0)
    
    
  @Property
  def page(): 
    def get(self): return self.__page.the_page
    def set(self, value): 
      self.__page.clear()
      self.__page.pack_start(value, True, True, 0)
      self.__page.the_page = value
    
    
  def __do_clicked_tab(self, control, event):
    self.__tab_1.props.background_color=theme.COLOR_TAB_INACTIVE.get_int()
    self.__tab_2.props.background_color=theme.COLOR_TAB_INACTIVE.get_int()
    self.__tab_3.props.background_color=theme.COLOR_TAB_INACTIVE.get_int()
    control.props.background_color=theme.COLOR_TAB_ACTIVE.get_int()
    self.__parent.do_tab_clicked(control.page)



class Edit(Page):

  def __init__(self, jokebook):
    Page.__init__(self)
    
    self.__jokebook = jokebook    
    
    self.__page_selector = PageSelector(self)
    self.pack_start(self.__page_selector, True, True, 0)
    self.__page_selector.page = EditInfo(jokebook, self)
    
    button = Gtk.Button(_('Preview'))
    button.connect('clicked', self.__do_clicked_preview, jokebook)    
    self.pack_start(button, False, False, 0)


  def __do_clicked_preview(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.preview.Preview, jokebook)
  

  def do_tab_clicked(self, page_class):
    print page_class
    self.__page_selector.page = page_class(self.__jokebook, self)
    return self.__page_selector.page


class EditInfo(Page): # TODO -> gui.Page should follow this pattern rather
  def __init__(self, jokebook, parent):
    Page.__init__(self)
    
    self.__parent = parent
    
    # page title
    self.pack_start(self.make_field(_('Title of Jokebook:'), 250, jokebook, 'title', 300, True), False, False, 0)
    #field = self.make_field(_('Sound Effect:'), 250, None, '', 300, False)
    
    sound_effect = Gtk.Box()
    sound_effect.pack_start(self.make_bodytext(_('Sound Effect:'), 250, hippo.ALIGNMENT_START, theme.COLOR_DARK_GREEN), False, False, 0)
    sound_effect.pack_start(self.make_audiobox(jokebook, 'sound', 316), False, False, 0)
    self.pack_start(sound_effect, False, False, 0)
    

    # cover picture
    cover_image = self.make_imagebox(jokebook, 'image', 320, 240, True)
    self.pack_start(cover_image, False, False, 0)
    
    # punchline sound
    #self.append(self.make_audiobox(jokebook, 'sound'))
    
  
class EditJokes(Page):
  
  def __init__(self, jokebook, parent):
    Page.__init__(self)
    
    self.__parent = parent
    
    # list of jokes
    jokes_div = CanvasListBox()
    jokes_div.props.border=0
    for joke in jokebook.jokes:
      button = Gtk.Button(' ' + _('Delete') + ' ')
      button.connect('clicked', self.__do_clicked_delete, jokebook, joke)
      list_row = self.make_listrow(JokeEditor(joke))
      list_row.pack_end(button, False, False, 0)
      jokes_div.pack_start(list_row, False, False, 0)

    self.pack_start(jokes_div, True, True, 0)
    
    # new joke button
    buttons = Gtk.Box()
    button = Gtk.Button(_('Add New Joke'))
    button.connect('clicked', self.do_clicked_add_joke, jokebook)    
    buttons.pack_start(button, False, False, 0)    
    jokes_div.pack_start(buttons, False, False, 0)
    
    
  def __do_clicked_delete(self, button, jokebook, joke):
    confirm = Gtk.MessageDialog(Globals.JokeMachineActivity, 
                                Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
                                Gtk.MESSAGE_QUESTION,
                                Gtk.BUTTONS_YES_NO,
                                _('Are you sure you want to delete this joke ?'))
    response = confirm.run()
    confirm.hide()
    confirm.destroy()
    del confirm
    if response == Gtk.RESPONSE_YES:
      logging.debug('Deleting joke: %s' % joke.id)
      jokebook.jokes.remove(joke)
      self.__parent.do_tab_clicked(EditJokes)
    
    
  def do_clicked_add_joke(self, button, jokebook):
    # create a new joke
    joke = persistence.joke.Joke() 
    joke.id = jokebook.next_joke_id
    logging.info('Created new joke with id: %d' % joke.id)
    joke.joker = Globals.nickname
    jokebook.jokes.append(joke)
    
    # reload tab
    self.__parent.do_tab_clicked(EditJokes)
  
    
    
class EditReview(Page):
  def __init__(self, jokebook, parent):
    Page.__init__(self)
    
    self.__parent = parent
    
    jokes_div = CanvasListBox()  
    jokes_div.props.border=0
    for joke in jokebook.submissions:
      list_row = self.make_listrow(JokeViewer(joke, jokebook.title))
      list_row.props.orientation=Gtk.Orientation.VERTICAL
      
      buttons = Gtk.Box()
      
      button = Gtk.Button(' ' + _('Reject') + ' ')
      button.connect('clicked', self.__do_clicked_reject, jokebook, joke)
      buttons.pack_start(button, False, False, 0)

      button = Gtk.Button(' ' + _('Accept') + ' ')
      button.connect('clicked', self.__do_clicked_accept, jokebook, joke)
      buttons.pack_start(button, False, False, 0)
 
      list_row.append(buttons)
      
      jokes_div.append(list_row)
      
    self.append(jokes_div)
    
    
  def __do_clicked_accept(self, button, jokebook, joke):
    jokebook.jokes.append(joke)
    jokebook.submissions.remove(joke)
    self.__parent.do_tab_clicked(EditReview)
    if Globals.JokeMachineActivity.is_shared:
      # broadcast submission onto the mesh
      logging.debug('Broadcasting joke to mesh')
      pickle = joke.dumps()
      Globals.JokeMachineActivity.tube.BroadcastJoke(jokebook.id, pickle, Globals.nickname)
      logging.debug('Broadcasted joke to mesh')

  
  def __do_clicked_reject(self, button, jokebook, joke):
    jokebook.submissions.remove(joke)
    self.__parent.do_tab_clicked(EditReview)
