__version__ = "prealpha"

#------------------- Imports --------------------------#

from pygame import Surface,Color,event,font,draw,Rect,mouse,key
from pygame.locals import *
from threading import Thread
from time import sleep
from tygame.constants import *
import traceback

#-------------------Globals------------------------------#

_widgets = []
_front_obj = None
_focused = None

#-------------------- Widgets ---------------------------#

#-------------------- In Development --------------------#
class Cascade:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.master = master
        self.bind_obj = None

class MenuButton:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.master = master
        self.cascade = None

class CheckButton:
    pass

class XFrame:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.static = False
        self.alpha = 200
        self.hcolor = Color("Grey")
        self.iconcolor = Color("White")
        self.htitle = ""
        self.htitlebold = False
        self.htitleitalic = False
        self.htitlefont = "Arial"
        self.htitlesize = 12
        self.htitlecolor = Color("white")
        self.master = master
        self.width = 150
        self.height = 150
        self.image = None
        self.font = "Arial"
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("white")
        self.text = ""
        self.borderwidth = 2
        self.bordercolor = Color("Grey")

        self.header = True
        self.isMaster = True
        self.isDragging = False
        self.isRendering = False
        self._priority = 3
        self.placed_obj = []

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "alpha": self.alpha = kwarg[key]
            elif key == "slide": self.slide = kwarg[key]
            elif key == "static": self.static = kwarg[key]
            elif key == "hcolor": self.hcolor = kwarg[key]
            elif key == "iconcolor": self.iconcolor = kwarg[key]
            elif key == "htitle": self.htitle = kwarg[key]
            elif key == "htitlebold": self.htitlebold = kwarg[key]
            elif key == "htitleitalic": self.htitleitalic = kwarg[key]
            elif key == "htitlefont": self.htitlefont = kwarg[key]
            elif key == "htitlesize": self.htitlesize = kwarg[key]
            elif key == "htitlecolor": self.htitlecolor = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            titleFont = font.SysFont(self.htitlefont,self.htitlesize,self.htitlebold,self.htitleitalic)
            titleText = titleFont.render(self.htitle,True,self.htitlecolor)

            if self.image == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            self._header = Surface((self.width+self.borderwidth*2,self.borderwidth+titleText.get_height()+4)) # Make Header
            self._header.fill(self.hcolor)
            draw.line(self._header,self.iconcolor,(self.width-self.borderwidth-12,self.borderwidth),(self.width-self.borderwidth-2,self.borderwidth+titleText.get_height()-3),2)
            draw.line(self._header,self.iconcolor,(self.width-self.borderwidth-12,self.borderwidth+titleText.get_height()-3),(self.width-self.borderwidth-2,self.borderwidth),2)
            self._headerHeight = self._header.get_height()+4

            if self.image == None: # Makes the body
                self.body = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth))
                self.body.fill(self.bordercolor)
                draw.rect(self.body,self.colour,(self.borderwidth,0,self.width,self.height))
            elif self.image != None:
                self.width,self.height = self.image.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth))
                self.body = tmpSurface
        except AttributeError:
            raise TypeError

        self.image = Surface((self._header.get_width(),self._header.get_height()+self.body.get_height()))
        self.image.blit(self._header,(0,0))
        self.image.blit(self.body,(0,self._header.get_height()))

        try:
            self.image.blit(titleText,(self.borderwidth,self.borderwidth))
        except:
            pass

        try:
            self.body.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        _widgets.append(self)

    def close(self):
        self.kill()

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False
        for widget in self.placed_obj:
            widget.forget_place()

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True
        for widget in self.placed_obj:
            widget.remember_place()

    def dragStart(self,mx,my):
        self.isDragging = True
        self.offsetx, self.offsety = mx-self.pos[0],my-self.pos[1]
        self.image.set_alpha(self.alpha)
        while self.isDragging:
            mx,my = mouse.get_pos()
            self.move((mx-self.offsetx,my-self.offsety))

    def dragStop(self):
        self.image.set_alpha(255)
        self.isDragging = False

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)
        for widget in self.placed_obj:
            widget.kill()

    def blit(self,surface,pos):
        self.image.blit(surface,((self.borderwidth+pos[0],self.borderwidth+self._headerHeight+pos[1])))

#-------------------- Completed --------------------#


class DropFrame:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.static = False
        self.hcolor = Color("Grey")
        self.iconcolor = Color("White")
        self.htitle = ""
        self.htitlebold = False
        self.htitleitalic = False
        self.htitlefont = "Arial"
        self.htitlesize = 12
        self.htitlecolor = Color("white")
        self.master = master
        self.width = 150
        self.height = 150
        self.image = None
        self.font = "Arial"
        self.fontsize = 12
        self.bold = False
        self.alpha = 200
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("white")
        self.text = ""
        self.slide = True # Could be added
        self.borderwidth = 2
        self.bordercolor = Color("Grey")

        self.header = True
        self.isMaster = True
        self.isDragging = False
        self.isClosed = False
        self.isRendering = False
        self._priority = 3
        self.placed_obj = []

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "alpha": self.alpha = kwarg[key]
            elif key == "slide": self.slide = kwarg[key] # Could be added
            elif key == "static": self.static = kwarg[key]
            elif key == "hcolor": self.hcolor = kwarg[key]
            elif key == "iconcolor": self.iconcolor = kwarg[key]
            elif key == "htitle": self.htitle = kwarg[key]
            elif key == "htitlebold": self.htitlebold = kwarg[key]
            elif key == "htitleitalic": self.htitleitalic = kwarg[key]
            elif key == "htitlefont": self.htitlefont = kwarg[key]
            elif key == "htitlesize": self.htitlesize = kwarg[key]
            elif key == "htitlecolor": self.htitlecolor = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            titleFont = font.SysFont(self.htitlefont,self.htitlesize,self.htitlebold,self.htitleitalic)
            titleText = titleFont.render(self.htitle,True,self.htitlecolor)

            if self.image == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            self.headermin = Surface((self.width+self.borderwidth*2,self.borderwidth+titleText.get_height()+4)) # Make Header
            self.headermin.fill(self.hcolor)
            self.headeropen = Surface((self.width+self.borderwidth*2,self.borderwidth+titleText.get_height()+4)) # Make Header
            self.headeropen.fill(self.hcolor)
            draw.line(self.headermin,self.iconcolor,(self.width-self.borderwidth-12,self.borderwidth+titleText.get_height()-3),(self.width-self.borderwidth-2,self.borderwidth+titleText.get_height()-3),3)
            draw.rect(self.headeropen,self.iconcolor,(self.width-self.borderwidth-12,self.borderwidth+2,10,titleText.get_height()-2),2)
            self._headerHeight = self.headermin.get_height()+4

            if self.image == None: # Makes the body
                self.body = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth))
                self.body.fill(self.bordercolor)
                draw.rect(self.body,self.colour,(self.borderwidth,0,self.width,self.height))
            elif self.image != None:
                self.width,self.height = self.image.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth))
                self.body = tmpSurface

        except AttributeError:
            raise TypeError

        try:
            self.headermin.blit(titleText,(self.borderwidth,self.borderwidth))
            self.headeropen.blit(titleText,(self.borderwidth,self.borderwidth))
        except:
            pass

        try:
            self.body.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        self.image = Surface((self.headermin.get_width(),self.headermin.get_height()+self.body.get_height()))
        self.image.blit(self.headermin,(0,0))
        self.image.blit(self.body,(0,self.headermin.get_height()))

        _widgets.append(self)

    def close(self):
        self.isClosed = True
        self.image.fill((0,0,0,0))
        self.image.blit(self.headeropen,(0,0))
        for widget in self.placed_obj:
            widget.forget_place()

    def open(self):
        self.isClosed = False
        self.image.fill((0,0,0,0))
        self.image.blit(self.headermin,(0,0))
        self.image.blit(self.body,(0,self.headermin.get_height()))
        for widget in self.placed_obj:
            widget.remember_place()

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                if not self.isClosed:
                    self.image.blit(self.body,(0,self.headermin.get_height()))
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False
        for widget in self.placed_obj:
            widget.forget_place()

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True
        for widget in self.placed_obj:
            widget.remember_place()

    def dragStart(self,mx,my):
        self.isDragging = True
        self.offsetx, self.offsety = mx-self.pos[0],my-self.pos[1]
        self.image.set_alpha(self.alpha)
        while self.isDragging:
            mx,my = mouse.get_pos()
            self.move((mx-self.offsetx,my-self.offsety))

    def dragStop(self):
        self.image.set_alpha(255)
        self.isDragging = False

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)
        for widget in self.placed_obj:
            widget.kill()

    def blit(self,surface,pos):
        self.body.blit(surface,(pos[0]+self.borderwidth,pos[1]))


class HoverFrame:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.object = None
        self.sensorbox = None
        self.fadein = True
        self.fadeout = False
        self.alpha = 255
        self.master = master
        self.width = 100
        self.height = 100
        self.image = None
        self.font = "Arial"
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("white")
        self.text = ""
        self.borderwidth = 2
        self.bordercolor = Color("Grey")
        self.isHovering = False
        self.isRendering = False
        self._priority = 0

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "object": self.object = kwarg[key]
            elif key == "sensorbox": self.sensorbox = kwarg[key]
            elif key == "master": self.master = kwarg[key]
            elif key == "fadein": self.fadein = kwarg[key]
            elif key == "fadeout": self.fadeout = kwarg[key]
            elif key == "alpha": self.alpha = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            if self.image == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            if self.image == None:
                self.image = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2))
                self.image.fill(self.bordercolor)
                draw.rect(self.image,self.colour,(self.borderwidth,self.borderwidth,self.width,self.height))
                self.width,self.height = self.image.get_size()
            elif self.image != None:
                self.width,self.height = self.image.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth))
                self.image = tmpSurface
        except AttributeError:
            raise TypeError

        try:
            self.image.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        if self.object:
            try:
                self.sensorbox = Rect(self.object.pos,self.object.image.get_size())
            except:
                raise Exception("Object must be placed first.")

        _widgets.append(self)

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True

    def startHovering(self,pos):
        self.isHovering = True
        self.place((pos[0],pos[1]-self.image.get_height()))
        if self.fadein:
            for i in range(1,52):
                if self.isHovering:
                    mx,my = mouse.get_pos()
                    self.image.set_alpha(i*5)
                    self.move((mx,my-self.image.get_height()))
                    sleep(0.01)
        while self.isHovering:
            mx,my = mouse.get_pos()
            self.move((mx,my-self.image.get_height()))
        if self.fadeout:
            for i in range(1,52):
                if not self.isHovering:
                    mx,my = mouse.get_pos()
                    self.image.set_alpha(255-i*5)
                    self.move((mx,my-self.image.get_height()))
                    sleep(0.01)
        self.isRendering = False

    def stopHovering(self):
        self.isHovering = False

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)

    def blit(self,surface,pos):
        self.image.blit(surface,((self.borderwidth+pos[0],self.borderwidth+pos[1])))


class Entry:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.master = master
        self.bg = Color("white")
        self.width = 100
        self.height = 12
        self.image = None
        self.font = "Arial"
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("white")
        self.text = ""
        self.borderwidth = 2
        self.bordercolor = Color("Grey")
        self.numonly = False
        self.isRendering = False
        self.isFocused = False
        self._buffer = None # The shown words
        self._x = 0 # Keeps the position
        self._priority = 2

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "bg": self.bg = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "numonly": self.numonly = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            self._font = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
            testText = self._font.render("Testing",self.antialias,self.textcolor)
            tmpText = self._font.render(self.text,self.antialias,self.textcolor)
        except:
            print("Something went wrong with the Fonts.")

        if testText.get_height() > self.height:
            self.height = testText.get_height()

        try:
            if self.image == None:
                self.image = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2))
                self.image.fill(self.bordercolor)
                draw.rect(self.image,self.colour,(self.borderwidth,self.borderwidth,self.width,self.height))
            elif self.image != None:
                self.width,self.height = self.image.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth))
                self.image = tmpSurface
        except AttributeError:
            raise TypeError

        self._buffer = Surface((self.width,self.height),SRCALPHA)
        self._buffer.fill(self.bg)

        try:
            self._buffer.blit(tmpText,(self._x,0))
        except:
            pass

        _widgets.append(self)

    def write(self,button,mods):
        if button == "backspace":
            self.text = self.text[:-1]
        elif button == "space":
            button = " "
        elif button == "return":
            self.isFocused = False
        if self.numonly:
            if button.isalpha():
                button = ""

        if 0 < mods <= 3 or 4096 < mods <= 4099 or mods >= 8192:
            button = button.upper()
        if len(button) == 1:
            self.text += button
        if len(button) == 3:
            if button[0] == "[" and button[2] == "]":
                self.text += button[1]

        tmpText = self._font.render(self.text,self.antialias,self.textcolor)
        self._x = self.width - tmpText.get_width()
        if self._x > 0: self._x = 0
        self._buffer.fill(self.bg)
        self._buffer.blit(tmpText,(self._x,0))

    def get(self):
        return self.text

    def set(self,text):
        self.text = text
        tmpText = self._font.render(self.text,self.antialias,self.textcolor)
        self._x = self.width - tmpText.get_width()
        if self._x > 0: self._x = 0
        self._buffer.fill(self.bg)
        self._buffer.blit(tmpText,(self._x,0))

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                self.image.blit(self._buffer,(self.borderwidth,self.borderwidth))
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)


class FilmBar:

    def __init__(self,master=None,**kwarg):
        """Don't use vertical for now it's a little buggy

        This is the Filmbar Widget. It is used to scroll and showcase
        an image. It simply scrolls the image left and right. More
        functionality might be added in a later time.

        It takes the kwargs:

        width, dirty, height, length, orientation, arrowcolor,
        scrollspeed, image, film, colour, borderwidth,
        bordercolor
        """

        global _widgets

        self._pos = 0
        self._buffer = None

        self.master = master
        self.dirty = False
        self.width = 100
        self.height = 50
        self.length = 300
        self.image = None
        self.film = None
        self.arrowcolor = Color("Grey")
        self.orientation = HORIZONTAL
        self.scrollspeed = 5
        self.colour = Color("white")
        self.borderwidth = 2
        self.bordercolor = Color("Grey")
        self.isRendering = False
        self.isScrolling = False
        self._priority = 3
        self.isMaster = True

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "dirty": self.dirty = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "length": self.length = kwarg[key]
            elif key == "orientation": self.orientation = kwarg[key]
            elif key == "arrowcolor": self.arrowcolor = kwarg[key]
            elif key == "scrollspeed": self.scrollspeed = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "film": self.film = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        # Drawing the frame
        if self.image == None:
            self._border = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2),SRCALPHA)
            self._border.fill(self.bordercolor)
            draw.rect(self._border,(0,0,0,0),(self.borderwidth,self.borderwidth,self.width,self.height))

        # Drawing assemblying the rest
        try:
            if self.image == None:
                if self.orientation == HORIZONTAL:
                    self.image = Surface((self.borderwidth*2+self.width+56,self.borderwidth*2+self.height),SRCALPHA)
                    self.image.fill((0,0,0,0))
                    draw.polygon(self.image,self.arrowcolor,((0,self.image.get_height()//2),(25,0),(25,self.image.get_height())))
                    draw.polygon(self.image,self.arrowcolor,((self.image.get_width(),self.image.get_height()//2),(self.image.get_width()-25,0),(self.image.get_width()-25,self.image.get_height())))
                    self.image.blit(self._border,(28,0))
                    self._buffer = Surface((self.width,self.height),SRCALPHA)
                elif self.orientation == VERTICAL:
                    self.image = Surface((self.borderwidth*2+self.width,self.borderwidth*2+self.height+56),SRCALPHA)
                    self.image.fill((0,0,0,0))
                    draw.polygon(self.image,self.arrowcolor,((self.image.get_width()//2,0),(0,25),(self.image.get_width(),25)))
                    draw.polygon(self.image,self.arrowcolor,((self.image.get_width()//2,self.image.get_height()),(0,self.image.get_height()-25),(self.image.get_width(),self.image.get_height()-25)))
                    self.image.blit(self._border,(0,28))
                self._buffer = Surface((self.width,self.height),SRCALPHA)
            elif self.image != None:
                self.width,self.height = self.image.get_size()
                self._buffer = Surface((self.width-56,self.height-self.borderwidth*2),SRCALPHA)
        except AttributeError:
            raise TypeError

        if not self.film:
            if self.orientation == HORIZONTAL:
                self.film = Surface((self.length,self.height))
                self.film.fill((255,255,255))
            elif self.orientation == VERTICAL:
                self.film = Surface((self.width,self.length))
                self.film.fill((255,255,255))

        if self.orientation == HORIZONTAL:
            self._buffer.blit(self.film,(self._pos,0))
        elif self.orientation == VERTICAL:
            self._buffer.blit(self.film,(0,self._pos))

        _widgets.append(self)

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def startScroll(self,direction):

        self.isScrolling = True
        while self.isScrolling:

            if direction in (LEFT,UP):
                self._pos -= self.scrollspeed

            if direction in (RIGHT,DOWN):
                self._pos += self.scrollspeed

            if self.orientation == HORIZONTAL:
                if self.dirty:
                    self._buffer.blit(self.film,(self._pos,0))
                else:
                    self._buffer.fill((0,0,0,0))
                    self._buffer.blit(self.film,(self._pos,0))
            elif self.orientation == VERTICAL:
                if self.dirty:
                    self._buffer.blit(self.film,(0,self._pos))
                else:
                    self._buffer.fill((0,0,0,0))
                    self._buffer.blit(self.film,(0,self._pos))

            sleep(0.02)


    def stopScroll(self):
        self.isScrolling = False

    def render(self):
        try:
            if self.master and self.isRendering:
                if self.orientation == HORIZONTAL:
                    self.master.blit(self._buffer,(self.pos[0]+28+self.borderwidth,self.pos[1]+self.borderwidth))
                    self.master.blit(self.image,self.pos)
                else:
                    self.master.blit(self._buffer,(self.pos[0]+self.borderwidth,self.pos[1]+self.borderwidth+28))
                    self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)

    def blit(self,surface,pos):
        self.film.blit(surface,pos)
        if self.orientation == HORIZONTAL:
            self._buffer.blit(self.film,(self._pos,0))
        elif self.orientation == VERTICAL:
            self._buffer.blit(self.film,(0,self._pos))


class StaticFrame:

    def __init__(self,master=None,**kwarg):

        """
        This is the Static Frame Widget. It is similar to the
        frame object except that it is unmovable. So if you want
        it to hold items for display purposes use this rather than
        Frame.

        It takes the kwargs:
        header, htitle, htitlebold, htitleitalic, htitlefont,
        htitlesize, htitlecolor, width, height, image*, font,
        fontsize, bold, italic, textcolor, antialias
        colour, text, borderwidth, bordercolor

        * As of right now if you specify an image the width and
        height will be over ridden for the width and height of the
        image you have given"""

        global _widgets

        self.htitle = ""
        self.htitlebold = False
        self.htitleitalic = False
        self.htitlefont = "Arial"
        self.htitlesize = 12
        self.htitlecolor = Color("white")
        self.header = True
        self.master = master
        self.width = 50
        self.height = 50
        self.image = None
        self.font = "Arial"
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("white")
        self.text = ""
        self.borderwidth = 2
        self.bordercolor = Color("Grey")
        self.isRendering = False
        self.placed_obj = []
        self._priority = 4
        self.isMaster = True

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "htitle": self.htitle = kwarg[key]
            elif key == "htitlebold": self.htitlebold = kwarg[key]
            elif key == "htitleitalic": self.htitleitalic = kwarg[key]
            elif key == "htitlefont": self.htitlefont = kwarg[key]
            elif key == "htitlesize": self.htitlesize = kwarg[key]
            elif key == "htitlecolor": self.htitlecolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "header": self.header = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            if self.image == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
            if self.header:
                titleFont = font.SysFont(self.htitlefont,self.htitlesize,self.htitlebold,self.htitleitalic)
                titleText = titleFont.render(self.htitle,True,self.htitlecolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            if self.image == None:
                if self.header:
                    self.image = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2+titleText.get_height()+4))
                    self.image.fill(self.bordercolor)
                    self._headerHeight = titleText.get_height()+4
                    draw.rect(self.image,self.colour,(self.borderwidth,self.borderwidth+titleText.get_height()+4,self.width,self.height))
                    self.width,self.height = self.image.get_size()
                else:
                    self._headerHeight = 0
                    self.image = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2))
                    self.image.fill(self.bordercolor)
                    draw.rect(self.image,self.colour,(self.borderwidth,self.borderwidth,self.width,self.height))
                    self.width,self.height = self.image.get_size()
            elif self.image != None:
                self.width,self.height = self.image.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth))
                self.image = tmpSurface
        except AttributeError:
            raise TypeError

        try:
            self.image.blit(titleText,(2,2))
        except:
            pass

        try:
            self.image.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        _widgets.append(self)

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False
        for widget in self.placed_obj:
            widget.forget_place()

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True
        for widget in self.placed_obj:
            widget.remember_place()

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)
        for widget in self.placed_obj:
            widget.kill()

    def blit(self,surface,pos):
        self.image.blit(surface,((self.borderwidth+pos[0],self.borderwidth+self._headerHeight+pos[1])))


class TypableSurface(Surface):

    def __init__(self,array,flags=0,bg=Color("White"),depth=0,\
                 masks=None,text="",f="Arial",fontsize=12,alpha=(False,255),\
                 bold=False,italic=False,color=Color("Black"),alias=True):

        """
        A typeable surface is just a surface which has more support for
        fonts on it than a standard surface. It will take some special characters
        such as \n"""

        if not masks:
            super().__init__(array,flags)
        elif masks and depth:
            super().__init__(array,flags,depth,masks)
        self.text = text
        self.fill(bg)

        lines = text.split('\n')
        tmpFont = font.SysFont(f,fontsize,bold,italic)
        for i,line in enumerate(lines):
            surfaceText = tmpFont.render(line,alias,color)
            self.blit(surfaceText,(0,i*surfaceText.get_height()))


class Frame:

    def __init__(self,master=None,**kwarg):

        """
        This is the Frame Widget. It is used to hold objects
        just like tkinter. Unlike tkinter, the Frame in this module
        contains headers which are like tabs. Frames are also movable.
        If the frame has a header, you can drag it by the header. If it
        doesn't, you can drag it with anything.

        It takes the kwargs:
        header, htitle, htitlebold, htitleitalic, htitlefont,
        htitlesize, htitlecolor, width, height, image*, font,
        fontsize, bold, italic, textcolor, antialias
        colour, text, borderwidth, bordercolor

        * As of right now if you specify an image the width and
        height will be over ridden for the width and height of the
        image you have given"""

        global _widgets

        self.htitle = ""
        self.htitlebold = False
        self.htitleitalic = False
        self.htitlefont = "Arial"
        self.htitlesize = 12
        self.htitlecolor = Color("white")
        self.header = True
        self.master = master
        self.width = 50
        self.height = 50
        self.image = None
        self.font = "Arial"
        self.fontsize = 12
        self.alpha = 200
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("white")
        self.text = ""
        self.borderwidth = 2
        self.bordercolor = Color("Grey")
        self.isRendering = False
        self.isDragging = False
        self._priority = 3
        self.placed_obj = []
        self.isMaster = True

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "alpha": self.alpha = kwarg[key]
            elif key == "htitle": self.htitle = kwarg[key]
            elif key == "htitlebold": self.htitlebold = kwarg[key]
            elif key == "htitleitalic": self.htitleitalic = kwarg[key]
            elif key == "htitlefont": self.htitlefont = kwarg[key]
            elif key == "htitlesize": self.htitlesize = kwarg[key]
            elif key == "htitlecolor": self.htitlecolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "header": self.header = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            if self.image == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
            if self.header:
                titleFont = font.SysFont(self.htitlefont,self.htitlesize,self.htitlebold,self.htitleitalic)
                titleText = titleFont.render(self.htitle,True,self.htitlecolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            if self.image == None:
                if self.header:
                    self.image = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2+titleText.get_height()+4))
                    self.image.fill(self.bordercolor)
                    self._headerHeight = titleText.get_height()+4
                    draw.rect(self.image,self.colour,(self.borderwidth,self.borderwidth+titleText.get_height()+4,self.width,self.height))
                    self.width,self.height = self.image.get_size()
                else:
                    self._headerHeight = 0
                    self.image = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2))
                    self.image.fill(self.bordercolor)
                    draw.rect(self.image,self.colour,(self.borderwidth,self.borderwidth,self.width,self.height))
                    self.width,self.height = self.image.get_size()
            elif self.image != None:
                if self.header:
                    tmpSurface = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2+titleText.get_height()+4))
                    self.image.fill(self.bordercolor)
                    self._headerHeight = titleText.get_height()+4
                    self.width,self.height = self.image.get_size()
                    tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                    tmpSurface.fill(self.bordercolor)
                    tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth+self._headerHeight))
                    self.image = tmpSurface
                else:
                    self.width,self.height = self.image.get_size()
                    tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                    tmpSurface.fill(self.bordercolor)
                    tmpSurface.blit(self.image,(self.borderwidth,self.borderwidth))
                    self.image = tmpSurface
        except AttributeError:
            raise TypeError

        try:
            self.image.blit(titleText,(self.borderwidth,self.borderwidth))
        except:
            pass

        try:
            self.image.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        _widgets.append(self)

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False
        for widget in self.placed_obj:
            widget.forget_place()

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True
        for widget in self.placed_obj:
            widget.remember_place()

    def dragStart(self,mx,my):
        self.isDragging = True
        self.offsetx, self.offsety = mx-self.pos[0],my-self.pos[1]
        self.image.set_alpha(self.alpha)
        while self.isDragging:
            mx,my = mouse.get_pos()
            self.move((mx-self.offsetx,my-self.offsety))

    def dragStop(self):
        self.image.set_alpha(255)
        self.isDragging = False

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        for widget in self.placed_obj:
            widget.kill()
        _widgets.remove(self)

    def blit(self,surface,pos):
        self.image.blit(surface,((self.borderwidth+pos[0],self.borderwidth+self._headerHeight+pos[1])))


class Button:

    def __init__(self,master=None,**kwarg):
        """
        This is the Button Widget. When a button is pressed
        it will return the event WIDGETBUTTONPRESSED and will
        have an attribute called 'button' which returns the
        instance of the button that was pressed.

        It takes the kwargs:
        width, height, image**, font, fontsize, bold, italic,
        textcolor, antialias, target*, args*, depthx, depthy,
        colour, text, borderwidth, bordercolor, direction

        * Right now target and args must be formatted to use
        one list or tuple or else it will cause an error

        ** As of right now if you specify an image the width and
        height will be over ridden for the width and height of the
        image you have given"""

        global _widgets

        self.master = master
        self.width = 50
        self.height = 50
        self.upimage = None
        self.downimage = None
        self.font = "Arial"
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.target = None
        self.args = tuple()
        self.colour = Color("White")
        self.text = ""
        self.borderwidth = 3
        self.bordercolor = Color("Grey")
        self.isRendering = False
        self.isPressed = False
        self._priority = 4

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "upimage": self.upimage = kwarg[key]
            elif key == "downimage": self.downimage = kwarg[key]
            elif key == "target": self.target = kwarg[key]
            elif key == "args": self.args = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            if self.upimage == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            if self.upimage == None:
                self.upimage = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2))
                self.upimage.fill(self.bordercolor)
                draw.rect(self.upimage,self.colour,(self.borderwidth,self.borderwidth,self.width,self.height))
                draw.polygon(self.upimage,Color("Black"),[(0,self.upimage.get_height()),(self.borderwidth,self.height+self.borderwidth),\
                                                          (self.width+self.borderwidth,self.height+self.borderwidth),(self.width+self.borderwidth,self.borderwidth),\
                                                          (self.upimage.get_width(),0),self.upimage.get_size()])
            elif self.upimage != None:
                self.width,self.height = self.upimage.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.upimage,(self.borderwidth,self.borderwidth))
                draw.polygon(self.upimage,Color("Black"),[(0,self.upimage.get_height()),(self.borderwidth,self.height+self.borderwidth),\
                                                          (self.width+self.borderwidth,self.borderwidth),(self.width+self.borderwidth,self.borderwidth),\
                                                          (self.upimage.get_width(),0),self.upimage.get_size()])
                self.upimage = tmpSurface
        except AttributeError:
            raise TypeError

        try:
            if self.downimage == None:
                self.downimage = Surface((self.width+self.borderwidth*2,self.height+self.borderwidth*2))
                self.downimage.fill(self.bordercolor)
                draw.rect(self.downimage,self.colour,(self.borderwidth,self.borderwidth,self.width,self.height))
                draw.polygon(self.downimage,Color("Black"),[(0,0),(self.downimage.get_width(),0),(self.width+self.borderwidth,self.borderwidth),\
                                                          (self.borderwidth,self.borderwidth),(self.borderwidth,self.height+self.borderwidth),(0,self.downimage.get_height())])
            elif self.downimage != None:
                self.width,self.height = self.downimage.get_size()
                tmpSurface = Surface((self.height+self.borderwidth*2,self.width+self.borderwidth*2))
                tmpSurface.fill(self.bordercolor)
                tmpSurface.blit(self.downimage,(self.borderwidth,self.borderwidth))
                draw.polygon(self.downimage,Color("Black"),[(0,0),(self.downimage.get_width(),0),(self.width+self.borderwidth,self.borderwidth),\
                                                          (self.borderwidth,self.borderwidth),(self.borderwidth,self.height+self.borderwidth),(0,self.downimage.get_height())])
                self.downimage = tmpSurface
        except AttributeError:
            raise TypeError

        self.image = self.upimage

        try:
            self.upimage.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
            self.downimage.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        _widgets.append(self)

    def runTarget(self):
        try:
            if self.target:
                if self.args:
                    self.target(self.args)
                else:
                    self.target()
        except:
            traceback.print_exc()

    def buttonPressed(self):
        self.isPressed = True
        self.image = self.downimage
        event.post(event.Event(WIDGETBUTTONPRESSED,{"widget":self}))

    def buttonUp(self):
        self.isPressed = False
        self.image = self.upimage
        self.runTarget()
        event.post(event.Event(WIDGETBUTTONUP,{"widget":self}))

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                if self.isPressed:
                    self.master.blit(self.downimage,self.pos)
                else:
                    self.master.blit(self.upimage,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)

    def blit(self,surface,pos):
        self.image.blit(surface,(pos[0]+self.borderwidth,pos[1]+self.borderwidth))


class Label:

    def __init__(self,master=None,**kwarg):

        global _widgets

        self.master = master
        self.width = 100
        self.height = 100
        self.image = None
        self.font = "Arial"
        self.htitle = ""
        self.htitlebold = False
        self.htitleitalic = False
        self.htitlefont = "Arial"
        self.htitlesize = 12
        self.htitlecolor = Color("Dark Grey")
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.textcolor = Color("Black")
        self.antialias = True
        self.colour = Color("Dark Grey")
        self.alpha = 150
        self.text = ""

        self.placed_obj = []
        self._headerHeight = 0
        self.isMaster = True
        self.isRendering = False
        self._priority = 3
        self.header = True

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "htitle": self.htitle = kwarg[key]
            elif key == "htitlebold": self.htitlebold = kwarg[key]
            elif key == "htitleitalic": self.htitleitalic = kwarg[key]
            elif key == "htitlefont": self.htitlefont = kwarg[key]
            elif key == "htitlesize": self.htitlesize = kwarg[key]
            elif key == "htitlecolor": self.htitlecolor = kwarg[key]
            elif key == "font": self.font = kwarg[key]
            elif key == "fontsize": self.fontsize = kwarg[key]
            elif key == "bold": self.bold = kwarg[key]
            elif key == "italic": self.italic = kwarg[key]
            elif key == "textcolor": self.textcolor = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "alpha": self.alpha = kwarg[key]
            elif key == "antialias": self.antialias = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "text": self.text = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        try:
            if self.image == None and self.text:
                newFont = font.SysFont(self.font,self.fontsize,self.bold,self.italic)
                tmpText = newFont.render(self.text,self.antialias,self.textcolor)
        except:
            print("Something went wrong with the Fonts.")

        try:
            if self.image == None and self.htitle:
                titleFont = font.SysFont(self.htitlefont,self.htitlesize,self.htitlebold,self.htitleitalic)
                title = titleFont.render(self.htitle,1,self.htitlecolor)
                self._headerHeight = title.get_height()
        except:
            print("Something went wrong with the Fonts.")

        try:
            if self.image == None:
                self.image = Surface((self.width,self.height+int(self._headerHeight//2)),SRCALPHA)
                self.image.fill((0,0,0,0))
                draw.rect(self.image,(self.colour.r,self.colour.g,self.colour.b,self.alpha),(1,1+int(self._headerHeight//2),self.width-2,self.height-2),3)
                draw.rect(self.image,(0,0,0,150),(1,1+int(self._headerHeight//2),self.width-2,self.height-2),1)
        except:
            raise ValueError

        try:
            self.image.blit(tmpText,(int((self.width-tmpText.get_width())//2),int((self.height-tmpText.get_height())//2)))
        except:
            pass

        try:
            if self.htitle:
                draw.rect(self.image,(0,0,0,0),(6,0,title.get_width()+int(self._headerHeight//2),title.get_height()))
                self.image.blit(title,(8,0))
        except:
            pass

        _widgets.append(self)

    def place(self,pos):
        self.pos = pos
        self.isRendering = True
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self)
            self._priority = self.master._priority -1

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self.image,self.pos)
        except NameError:
            raise Exception("Position was not set.")

    def forget_place(self):
        """Stop this widget from rendering"""
        self.isRendering = False

    def remember_place(self):
        """Restarts this widget to begin rendering"""
        self.isRendering = True

    def move(self,pos):
        self.pos = pos

    def kill(self):
        global _widgets
        self.isRendering = False
        _widgets.remove(self)

    def blit(self,surface,pos):
        self.image.blit(surface,((4+pos[0],4+self._headerHeight+pos[1])))


#-------------------------- Handling Functions ----------------------#

def handle_widgets():
    global _front_obj, _focused
    _front_obj = get_front_obj()
    _widgets.sort(key=get_priority,reverse=True)
    events = event.get()
    mx,my = mouse.get_pos()
    # Active Widgets
    tmpL = list(_widgets)
    tmpL.reverse()

    for e in events:

        if e.type == MOUSEBUTTONDOWN:
            # Mouse down actions

            for widget in tmpL:

                tmpMaster = widget.master # Finding the actual position if has
                tmpPosX,tmpPosY = 0,0     # a master
                while hasattr(tmpMaster,"isMaster"):
                    if tmpMaster.isRendering:
                        if hasattr(tmpMaster,"header"):
                            tmpPosX += tmpMaster.pos[0]
                            tmpPosY += tmpMaster.pos[1] + tmpMaster._headerHeight
                        else:
                            tmpPosX += tmpMaster.pos[0]
                            tmpPosY += tmpMaster.pos[1]
                    if hasattr(tmpMaster,"master"):
                        tmpMaster = tmpMaster.master

                if type(widget) == Button: # Handles Buttons
                    if widget.isRendering and Rect(tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.image.get_width(),widget.image.get_height()).collidepoint((mx,my)):
                        widget.buttonPressed()
                        break

                elif type(widget) == Frame: # Handles Frame
                    if widget.isRendering:
                        if widget.header:
                            if Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget._headerHeight)).collidepoint((mx,my)):
                                tmpThread = Thread(target=widget.dragStart,args=(mx,my))
                                tmpThread.start()
                                widget._priority = 1
                                break
                            elif Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget.height)).collidepoint((mx,my)):
                                break

                        else:
                            if Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget.height)).collidepoint((mx,my)):
                                tmpThread = Thread(target=widget.dragStart,args=(mx,my))
                                tmpThread.start()
                                widget._priority = 1
                                break

                elif type(widget) == StaticFrame:
                    if Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget.height+widget._headerHeight)).collidepoint((mx,my)):
                        break

                elif type(widget) == XFrame: # Handles XFrames
                    if widget.isRendering and Rect(tmpPosX+widget.pos[0]+widget.image.get_width()-widget.borderwidth-15,tmpPosY+widget.pos[1]+widget.borderwidth,10,widget._header.get_height()-2).collidepoint((mx,my)):
                        widget.close()
                    elif widget.isRendering and not widget.static:
                        if Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget._headerHeight)).collidepoint((mx,my)):
                            tmpThread = Thread(target=widget.dragStart,args=(mx,my))
                            tmpThread.start()
                            widget._priority = 1
                            break
                        elif Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget.height)).collidepoint((mx,my)):
                            break

                elif type(widget) == DropFrame: # Handles Drop Frames
                    if widget.isRendering and Rect(tmpPosX+widget.pos[0]+widget.image.get_width()-widget.borderwidth-15,tmpPosY+widget.pos[1]+widget.borderwidth,10,widget.headermin.get_height()-2).collidepoint((mx,my)):
                        if widget.isClosed:
                            widget.open()
                            widget._priority = 1
                            break
                        else:
                            widget.close()
                            widget._priority = 1
                            break
                    elif widget.isRendering and not widget.static:
                        if Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget._headerHeight)).collidepoint((mx,my)):
                            tmpThread = Thread(target=widget.dragStart,args=(mx,my))
                            tmpThread.start()
                            widget._priority = 1
                            break
                        elif Rect((tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.width,widget.height)).collidepoint((mx,my)) and not widget.isClosed:
                            break

                elif type(widget) == FilmBar: # Handles Film Bars
                    if widget.isRendering:
                        if widget.orientation == HORIZONTAL:
                            if Rect(tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],25,widget.image.get_height()).collidepoint(mx,my):
                                tmpThread = Thread(target=widget.startScroll,args=(LEFT,))
                                tmpThread.start()
                                break
                            elif Rect((tmpPosX+widget.pos[0]+widget.image.get_width()-25,tmpPosY+widget.pos[1]),(25,widget.image.get_height())).collidepoint(mx,my):
                                tmpThread = Thread(target=widget.startScroll,args=(RIGHT,))
                                tmpThread.start()
                                break
                        elif widget.orientation == VERTICAL:
                            if Rect(tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.image.get_width(),25).collidepoint(mx,my):
                                tmpThread = Thread(target=widget.startScroll,args=(UP,))
                                tmpThread.start()
                                break
                            if Rect(tmpPosX+widget.pos[0],tmpPosY+widget.pos[1]+widget.image.get_height()-25,widget.image.get_width(),25).collidepoint(mx,my):
                                tmpThread = Thread(target=widget.startScroll,args=(DOWN,))
                                tmpThread.start()
                                break

                elif type(widget) == Entry: # Handles Entries
                    if widget.isRendering:
                        if Rect(tmpPosX+widget.pos[0],tmpPosY+widget.pos[1],widget.image.get_width(),widget.image.get_height()).collidepoint(mx,my):
                            try: _focused.isFocused = False
                            except: pass
                            _focused = widget
                            widget.isFocused = True
                            break
                        else:
                            widget.isFocused = False

        elif e.type == MOUSEBUTTONUP:
            # Clean up and mouse lift actions
            for widget in tmpL:

                tmpMaster = widget.master
                tmpPosX,tmpPosY = 0,0
                while hasattr(tmpMaster,"isMaster"):
                    if tmpMaster.isRendering:
                        if hasattr(tmpMaster,"header"):
                            tmpPosX += tmpMaster.pos[0]
                            tmpPosY += tmpMaster.pos[1] + tmpMaster._headerHeight
                        else:
                            tmpPosX += tmpMaster.pos[0]
                            tmpPosY += tmpMaster.pos[1]
                    if hasattr(tmpMaster,"master"):
                        tmpMaster = tmpMaster.master

                if type(widget) == Button:
                    if widget.isPressed:
                        widget.buttonUp()

                elif type(widget) == Frame:
                    if widget.isDragging:
                        widget._priority = 3
                        _widgets.sort(key=get_priority,reverse=True)
                        widget.dragStop()

                elif type(widget) == FilmBar:
                    if widget.isRendering:
                        widget.stopScroll()

                elif type(widget) == DropFrame:
                    if widget.isDragging:
                        widget._priority = 3
                        _widgets.sort(key=get_priority,reverse=True)
                        widget.dragStop()

                elif type(widget) == XFrame:
                    if widget.isDragging:
                        widget._priority = 3
                        _widgets.sort(key=get_priority,reverse=True)
                        widget.dragStop()

        elif e.type == KEYDOWN:
            for widget in _widgets:
                if type(widget) == Entry:
                    if widget.isRendering and widget.isFocused:
                        mods = key.get_mods()
                        widget.write(key.name(e.key),mods)

    # Passive Widgets
    for widget in tmpL:

        if type(widget) == HoverFrame:
            try:
                tmpPosX,tmpPosY = 0,0
                if hasattr(widget.object.master,"isMaster"):
                    tmpMaster = widget.object.master
                    while hasattr(tmpMaster,"isMaster"):
                        if tmpMaster.isRendering:
                            if hasattr(tmpMaster,"header"):
                                tmpPosX += tmpMaster.pos[0]
                                tmpPosY += tmpMaster.pos[1] + tmpMaster._headerHeight
                            else:
                                tmpPosX += tmpMaster.pos[0]
                                tmpPosY += tmpMaster.pos[1]
                        if hasattr(tmpMaster,"master"):
                            tmpMaster = tmpMaster.master
            except:
                pass
            if Rect(widget.sensorbox.x+tmpPosX,widget.sensorbox.y+tmpPosY,widget.sensorbox.w,widget.sensorbox.h).collidepoint((mx,my)) and not widget.isHovering:
                if hasattr(widget,"object"):
                    if widget.object:
                        if widget.object.isRendering:
                            tmpThread = Thread(target=widget.startHovering,args=((mx,my),))
                            tmpThread.start()
                    else:
                        tmpThread = Thread(target=widget.startHovering,args=((mx,my),))
                        tmpThread.start()
                else:
                    tmpThread = Thread(target=widget.startHovering,args=((mx,my),))
                    tmpThread.start()

        if type(widget) == HoverFrame and widget.isHovering:
            try:
                tmpPosX,tmpPosY = 0,0
                if hasattr(widget.object.master,"isMaster"):
                    tmpMaster = widget.object.master
                    while hasattr(tmpMaster,"isMaster"):
                        if tmpMaster.isRendering:
                            if hasattr(tmpMaster,"header"):
                                tmpPosX += tmpMaster.pos[0]
                                tmpPosY += tmpMaster.pos[1] + tmpMaster._headerHeight
                            else:
                                tmpPosX += tmpMaster.pos[0]
                                tmpPosY += tmpMaster.pos[1]
                        if hasattr(tmpMaster,"master"):
                            tmpMaster = tmpMaster.master
            except:
                pass
            if not Rect(widget.sensorbox.x+tmpPosX,widget.sensorbox.y+tmpPosY,widget.sensorbox.w,widget.sensorbox.h).collidepoint((mx,my)):
                widget.stopHovering()
    return events

def render_widgets(widgetlist=[]):
    if not widgetlist:
        global _widgets
        for widget in _widgets:
            widget.render()
    else:
        for widget in widgetlist:
            widget.render()

def get_priority(widget):
    global _front_obj
    if widget.master == _front_obj:
        return 1
    return widget._priority

def get_front_obj():
    for i in range(len(_widgets)):
        if type(_widgets[-1-i]) in (Frame,DropFrame,XFrame):
            return _widgets[-1-i]