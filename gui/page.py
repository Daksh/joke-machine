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
from gi.repository import Gtk, GdkPixbuf
from gi.repository import Gdk
from gi.repository import Pango
import logging
import StringIO

from gettext import gettext as _

from sugar3.graphics import style
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3 import mime


from util.persistence import Persistent, PersistentProperty

from util.audioplayer import AudioPlayer


from gui import theme
from globals import Globals


THUMB_SIZE = min(Gdk.Screen.width(), Gdk.Screen.height()) / 2


class Page(Gtk.Box):

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        self.__alternate_color_listrows = False
        self.__color_listrow = theme.COLOR_LIST_ROW_ALT.get_int()

    def append(self, item, *args, **kwargs):
        self.pack_start(item, False, False, 0)  # FIXME: No idea if works

    @property
    def color_listrow(self):
        if not self.__alternate_color_listrows:
            return theme.COLOR_LIST_ROW.get_int()
        if self.__color_listrow == theme.COLOR_LIST_ROW_ALT.get_int():
            self.__color_listrow = theme.COLOR_LIST_ROW.get_int()
        else:
            self.__color_listrow = theme.COLOR_LIST_ROW_ALT.get_int()
        return self.__color_listrow

    def make_listrow(self, contents=None, *args):
        list_row = RoundBox()
        # properties not being set properly by constructor
        list_row.props.border = 0
        list_row.props.padding = theme.DEFAULT_PADDING
        # list_row.props.padding_right=0
        list_row.props.background_color = self.color_listrow
        if contents is not None:
            list_row.append(contents, *args)
        return list_row

    def make_audiobox(self, obj, property, width):

        image_file = os.path.join(Globals.pwd, theme.AUDIO_CHOOSE)
        if not os.path.exists(image_file):
            logging.debug('cannot find %s' % image_file)
            return Gtk.Box()

        surface = GdkPixbuf.Pixbuf.new_from_file(image_file)
        preview_sound_img = Gtk.Image.new_from_pixbuf(surface)
        preview_sound = Gtk.EventBox()
        preview_sound.add(preview_sound_img)
        preview_sound.connect(
            'button-press-event',
            self.__do_clicked_preview_sound,
            obj,
            property)

        if hasattr(obj, property) and getattr(obj, property) is not None:
            sound_name = getattr(obj, property)
        else:
            sound_name = _('Click to choose a sound')

        choose_sound_label = Gtk.Label(sound_name)
        choose_sound = Gtk.EventBox()
        choose_sound.add(choose_sound_label)

        choose_sound.connect(
            'button-press-event',
            self.__do_clicked_choose_sound,
            obj,
            property)

        sound_box = Gtk.Box()
        sound_box.pack_start(prewiew_sound, False, False, 0)
        sound_box.pack_start(choose_sound, False, False, 0)
        sound_box.set_size_request(width, -1)

        return sound_box

    def make_imagebox(
            self,
            obj,
            property=None,
            width=-1,
            height=-1,
            editable=True,
            padding=0):
        image = self.__get_property_value(obj, property)
        if image == '' or image is None:
            image = theme.IMAGE_CHOOSE
        file_name = os.path.join(Globals.pwd, image)
        logging.debug('make_imagebox(%r)' % file_name)

        # TODO -> handle landscape/portrait properly

        # load image - could be cleaner on the whole... :)
        try:
            if hasattr(
                    obj,
                    'image_blob') and getattr(
                    obj,
                    'image_blob') is not None:
                image_file = StringIO.StringIO(obj.image_blob)
                surface = Gdk.Pixbuf.new_from_file_at_size(
                    image_file,
                    width,
                    height)
            else:
                surface = Gdk.Pixbuf.new_from_file_at_size(
                    file_name,
                    width,
                    height)
        except Exception as e:
            logging.error('Error while loading image: %r' % e)

        # the image itself
        cover_image = Gtk.Image.new_from_pixbuf(surface)

        if editable:
            cover_image.set_clickable(True)
            cover_image.connect(
                'button-press-event',
                self.__do_clicked_image,
                obj,
                'image_blob')
            image_box = Gtk.EventBox()
            image_box.override_background_color(
                Gtk.StateType.NORMAL,
                theme.COLOR_DARK_GREEN.get_rgba())
            image_box.add(cover_image)
        else:
            image_box = cover_image

        deglitch_box = Gtk.VBox()
        deglitch_box.pack_start(image_box, False, False, 0)
        return deglitch_box

    def make_bodytext(self, text, width=-1, **args):
        msg = Gtk.TextView()
        text_buffer = msg.get_buffer()
        text_buffer.set_text(text)
        msg.set_buffer(text_buffer)
        return msg

    def make_textbox(
            self,
            obj,
            property,
            width=300,
            height=100,
            editable=True):
        value = self.__get_property_value(obj, property)
        textbox = self.__textview(value, width, height, editable, True)
        textbox.control.get_buffer().connect(
            'changed',
            self.__do_changed_control,
            obj,
            property)
        return textbox

    def make_field(
            self,
            label,
            label_width,
            obj,
            property,
            field_width,
            editable=True):
        value = self.__get_property_value(obj, property)
        field_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label(label)
        label.set_size_request(label_width, -1)
        field_box.pack_start(label, False, False, 0)

        textfield = self.__textview(value, field_width, -1, editable, False)
        textfield.control.get_buffer().connect(
            'changed',
            self.__do_changed_control,
            obj,
            property)
        field_box.pack_start(textfield, False, False, 0)

        return field_box

    def __textview(
            self,
            text,
            width=300,
            height=-1,
            editable=True,
            multiline=False):
        textview = Gtk.TextView()
        textview.get_buffer().set_text(text)

        # control props
        textview.set_wrap_mode(Gtk.WRAP_WORD)
        textview.modify_base(
            Gtk.StateType.NORMAL,
            theme.COLOR_TEXTBOX.get_gdk_color())
        textview.set_editable(editable)
        textview.set_cursor_visible(editable)
        if height == -1:
            context = textview.create_pango_context()
            layout = Pango.Layout(context)
            layout.set_text(text[: text.find('\n')])
            (w, h) = layout.get_pixel_size()
            # + theme.BORDER_WIDTH_CONTROL / 2
            # fudge factor - on the XO-1 hardware all known
            # solutions evaporate
            height = h
        textview.set_size_request(width, height)
        textview.set_border_window_size(Gtk.TEXT_WINDOW_LEFT, 0)
        textview.set_border_window_size(Gtk.TEXT_WINDOW_RIGHT, 0)
        textview.set_border_window_size(Gtk.TEXT_WINDOW_TOP, 0)
        textview.set_border_window_size(Gtk.TEXT_WINDOW_BOTTOM, 0)
        textview.show()

        return textview

    def __get_property_value(self, obj, property):
        # TODO - Clean entire Model/View mechanism up so that we're not
        #        passing objects and text properties around at all
        if obj is None:
            return ''
        if isinstance(obj, str):
            return obj
        if hasattr(
                obj,
                '__metaclass__') and obj.__metaclass__ is Persistent \
                and hasattr(
                obj,
                property):
            value = getattr(obj, property)
            if value is None:
                return ''
            return value
        logging.debug(
            '__get_property_value error: Unknown object type %r',
            type(obj))
        return obj

    def __do_changed_control(self, control, obj, property):
        '''Update object model with control values'''
        if hasattr(obj, property) and hasattr(control.props, 'text'):
            setattr(obj, property, control.props.text)
        else:
            print 'NO PROPERTY OR TEXT'

    def __do_clicked_image(self, control, event, obj, property):
        if hasattr(mime, 'GENERIC_TYPE_IMAGE'):
            filter = {'what_filter': mime.GENERIC_TYPE_IMAGE}
        else:
            filter = {}

        # Courtesy of Write.activity - toolbar.py
        chooser = ObjectChooser(title=_('Choose image'),
                                # ._parent,
                                parent=Globals.JokeMachineActivity,
                                flags=Gtk.DIALOG_MODAL |
                                Gtk.DIALOG_DESTROY_WITH_PARENT,
                                **filter)
        try:
            result = chooser.run()
            if result == Gtk.RESPONSE_ACCEPT:
                logging.debug(
                    'ObjectChooser: %r' %
                    chooser.get_selected_object())
                journal_object = chooser.get_selected_object()
                if hasattr(
                        obj,
                        'image_blob') and journal_object \
                        and journal_object.file_path:
                    logging.debug(
                        'Getting journal object: %r, %s',
                        journal_object,
                        journal_object.file_path)
                    # Set the image now
                    raw = _load_image(journal_object.file_path)
                    obj.image = str(journal_object.metadata['title'])
                    obj.image_blob = raw
                    # refresh the image
                    image_file = StringIO.StringIO(obj.image_blob)
                    surface = cairo.ImageSurface.create_from_png(image_file)
                    control.props.image = surface
        finally:
            # chooser.hide()
            chooser.destroy()
            del chooser

    def __do_clicked_choose_sound(self, control, event, obj, property):
        if hasattr(mime, 'GENERIC_TYPE_AUDIO'):
            filter = {'what_filter': mime.GENERIC_TYPE_AUDIO}
        else:
            filter = {}

        logging.debug('choosing sound file')
        chooser = ObjectChooser(title=_('Choose Sound'),
                                # ._parent,
                                parent=Globals.JokeMachineActivity,
                                flags=Gtk.DIALOG_MODAL |
                                Gtk.DIALOG_DESTROY_WITH_PARENT,
                                **filter)
        try:
            result = chooser.run()
            if result == Gtk.RESPONSE_ACCEPT:
                logging.debug(
                    'ObjectChooser: %r' %
                    chooser.get_selected_object())
                journal_object = chooser.get_selected_object()
                if hasattr(
                        obj,
                        'sound_blob') and journal_object \
                        and journal_object.file_path:
                    logging.debug(
                        'Getting journal object: %r, %s, %s',
                        journal_object,
                        journal_object.file_path,
                        journal_object.metadata['title'])
                    # Set the sound now
                    f = open(journal_object.file_path, 'r')
                    raw = f.read()
                    f.close()
                    obj.sound = str(journal_object.metadata['title'])
                    obj.sound_blob = raw
                    control.props.text = obj.sound
        finally:
            # chooser.hide()
            chooser.destroy()
            del chooser

    def __do_clicked_preview_sound(self, control, event, obj, property):

        if not hasattr(
                obj,
                'sound_blob') or getattr(
                obj,
                'sound_blob') is None:
            logging.debug('No sound to preview')
            return

        player = AudioPlayer()
        # player.uri = sound_file
        player.raw = obj.sound_blob
        player.play()


def _load_image(file_name):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(file_name,
                                                    THUMB_SIZE, THUMB_SIZE)
    if pixbuf is None:
        return None
    stream = StringIO.StringIO()
    pixbuf.save_to_callbackv(lambda data: stream.write(data), 'png')
    return stream.getvalue()
