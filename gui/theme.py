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


# This is all rather horrible - but it will keep us afloat while Sugar
# stabilizes


# colors #######################################################################

COLOR_LIGHT_GREEN = style.Color('#66CC00')
COLOR_DARK_GREEN = style.Color('#027F01')
COLOR_PINK = style.Color('#FF0198')
COLOR_YELLOW = style.Color('#FFFF00')
COLOR_GRAY = style.Color('#ACACAC')
COLOR_LIGHT_GRAY = style.Color('#E2E2E3')
COLOR_RED = style.Color('#FF0000')
COLOR_WHITE = style.Color('#FFFFFF')
COLOR_BLACK = style.Color('#000000')
COLOR_BLUE = style.Color('#0000FF')

# deprecated colors from style.COLOR_*
COLOR_PANEL_GREY = style.Color('#C0C0C0')
COLOR_TOOLBAR_GREY = style.Color('#404040')
COLOR_TEXT_FIELD_GREY = style.Color('#E5E5E5')


COLOR_FG_BUTTONS = (
  (Gtk.StateType.NORMAL,      style.Color('#CCFF99')),
  (Gtk.StateType.ACTIVE,      style.Color('#CCFF99')),
  (Gtk.StateType.PRELIGHT,    style.Color('#CCFF99')),
  (Gtk.StateType.SELECTED,    style.Color('#CCFF99')),
  (Gtk.StateType.INSENSITIVE, style.Color('#CCFF99')),
)
COLOR_BG_BUTTONS = (
  (Gtk.StateType.NORMAL,      style.Color('#027F01')),
  (Gtk.StateType.ACTIVE,      style.Color('#014D01')),
  (Gtk.StateType.PRELIGHT,    style.Color('#016D01')),
  (Gtk.StateType.SELECTED,    style.Color('#027F01')),
  (Gtk.StateType.INSENSITIVE, style.Color('#027F01')),
)
COLOR_BG_RADIOBUTTONS = (
  (Gtk.StateType.NORMAL,      COLOR_LIGHT_GRAY),
  (Gtk.StateType.ACTIVE,      COLOR_LIGHT_GRAY),
  (Gtk.StateType.PRELIGHT,    COLOR_LIGHT_GRAY),
  (Gtk.StateType.SELECTED,    COLOR_LIGHT_GRAY),
  (Gtk.StateType.INSENSITIVE, COLOR_LIGHT_GRAY),
)
COLOR_FG_RADIOBUTTONS = (
  (Gtk.StateType.NORMAL,      COLOR_DARK_GREEN),
  (Gtk.StateType.ACTIVE,      COLOR_DARK_GREEN),
  (Gtk.StateType.PRELIGHT,    COLOR_DARK_GREEN),
  (Gtk.StateType.SELECTED,    COLOR_DARK_GREEN),
  (Gtk.StateType.INSENSITIVE, COLOR_DARK_GREEN),
)


# ui elements ##################################################################

COLOR_BACKGROUND      = COLOR_LIGHT_GREEN
COLOR_FRAME           = COLOR_YELLOW
COLOR_PAGE            = COLOR_WHITE
COLOR_PAGE_BORDER     = COLOR_PINK
COLOR_LIST_BACKGROUND = COLOR_PANEL_GREY
COLOR_LIST_BORDER     = COLOR_TOOLBAR_GREY
COLOR_LIST_ROW        = COLOR_TEXT_FIELD_GREY
COLOR_LIST_ROW_ALT    = COLOR_GRAY
COLOR_TEXTBOX         = COLOR_PAGE
COLOR_LINK            = COLOR_BLUE
COLOR_TAB_ACTIVE      = COLOR_DARK_GREEN
COLOR_TAB_INACTIVE    = COLOR_LIGHT_GREEN
COLOR_TAB_SEPERATOR   = COLOR_LIGHT_GRAY
COLOR_TAB_TEXT        = COLOR_WHITE


# constants ####################################################################

zoom = style.zoom

PADDING_TAB = style.zoom(6)
DEFAULT_PADDING = style.zoom(6)
DEFAULT_SPACING = style.zoom(8)
BORDER_WIDTH = style.zoom(6) 
BORDER_WIDTH_CONTROL = style.zoom(12) 
BORDER_WIDTH_IMAGE = style.zoom(1)
SPACER_VERTICAL = style.zoom(20)
SPACER_HORIZONTAL = style.zoom(20)

# images #######################################################################

IMAGE_CHOOSE = 'resources/image.png'
AUDIO_CHOOSE = 'resources/audio.png'


# helpers ######################################################################

# TODO - deprecate in favor of Gtkrc
def theme_widget(widget, width=-1, height=-1, highlight=False):
  """Apply colors to Gtk Widgets

  widget         is the widget
  width, height  are optional width and height for resizing the widget
  highlight      is a boolean to override the theme and apply a
                 different color to show "you are here".

  returns the modified widget.
  """
  
  return widget

  #if widget == None:
    #print 'theme.theme_widget(widget=None) !'
    #return

  #for state, color in COLOR_BG_BUTTONS:
    #if highlight:
      #widget.modify_bg(state, Gdk.color_parse("#CCFF99"))
    #else:
      #widget.modify_bg(state, color.get_gdk_color())

  #if hasattr(widget, 'get_child'):
    #c = widget.get_child()
    #if c is not None:
      #for state, color in COLOR_FG_BUTTONS:
        #if highlight:
          #c.modify_fg(state, COLOR_DARK_GREEN.get_gdk_color())
        #else:
          #c.modify_fg(state, color.get_gdk_color())
    #else:
      #for state, color in COLOR_FG_BUTTONS:
        #widget.modify_fg(state, color.get_gdk_color())

  #if width > 0 or height > 0:
    #widget.set_size_request(width, height)

  #return widget



