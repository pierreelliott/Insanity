from tygame.main import Entry,_widgets,StaticFrame,get_priority,Frame,Label,DropFrame,TypableSurface,Button,XFrame
from tygame.constants import *
from pygame import Surface,Color,event,font,draw,Rect,mouse,key
from pygame.locals import *

class Table:

    def __init__(self,master=None,**kwarg):

        self.master = master
        self.x = 1
        self.y = 1
        self.width = 100
        self.height = 100
        self.borderwidth = 2
        self.bordercolor = Color("Grey")
        self.framewidth = 50
        self.frameheight = 16
        self.framefont = "Arial"
        self.frameborderwidth = 1
        self.framefontsize = 12
        self.framebold = False
        self.frameitatic = False
        self.framealias = True
        self.colour = Color("White")
        self.image = None

        self.isRendering = False
        self._priority = 3

        for key in kwarg.keys():
            if key == "x": self.x = kwarg[key]
            elif key == "y": self.y = kwarg[key]
            elif key == "width": self.width = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            elif key == "framewidth": self.framewidth = kwarg[key]
            elif key == "frameheight": self.frameheight = kwarg[key]
            elif key == "framefont": self.framefont = kwarg[key]
            elif key == "framefontsize": self.framefontsize = kwarg[key]
            elif key == "framebold": self.framebold = kwarg[key]
            elif key == "frameitatic": self.frameitatic = kwarg[key]
            elif key == "framealias": self.framealias = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        if (self.framewidth+self.frameborderwidth*2)*self.x > self.width:
            self.width = (self.framewidth+self.frameborderwidth*2)*self.x

        if (self.frameheight+self.frameborderwidth*2)*self.y > self.height:
            self.height = (self.frameheight+self.frameborderwidth*2)*self.y

        self._frame = StaticFrame(self.master,width=self.width,height=self.height,\
                            borderwidth=self.borderwidth,bordercolor=self.bordercolor,\
                            header=0)

        self._entries = [Entry(self._frame,width=self.framewidth,height=self.frameheight,\
                               font=self.framefont,fontsize=self.framefontsize,bold=self.framebold,\
                               italic=self.frameitatic,antialias=self.framealias,borderwidth=self.frameborderwidth)\
                               for i in range(self.x*self.y)]

        for i,entry in enumerate(self._entries):
            entry.place((i%self.x*entry.image.get_width(),i//self.x*entry.image.get_height()))

        _widgets.append(self)

    def get(self,x,y):
        return self._entries[x+y*self.x].get()

    def set(self,value,x,y):
        self._entries[x+y*self.x].set(value)

    def place(self,pos):
        self.pos = pos
        self._frame.pos = pos
        self.isRendering = True
        _widgets.sort(key=get_priority,reverse=True)
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self._frame)

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self._frame.image,self.pos)
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


class Counter:

    def __init__(self,master,**kwarg):

        self.master = master
        self.width = 50
        self.height = 20
        self.borderwidth = 1
        self.bordercolor = Color("Grey")
        self.framefont = "Arial"
        self.frameborderwidth = 2
        self.framefontsize = 12
        self.framebold = False
        self.frameitatic = False
        self.framealias = True
        self.colour = Color("White")
        self.image = None
        self.value = 0
        self.step = 1

        self.isRendering = False
        self._priority = 3

        for key in kwarg.keys():
            if key == "width": self.width = kwarg[key]
            elif key == "height": self.height = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "image": self.image = kwarg[key]
            elif key == "colour": self.colour = kwarg[key]
            elif key == "borderwidth": self.borderwidth = kwarg[key]
            elif key == "bordercolor": self.bordercolor = kwarg[key]
            elif key == "framefont": self.framefont = kwarg[key]
            elif key == "framefontsize": self.framefontsize = kwarg[key]
            elif key == "framebold": self.framebold = kwarg[key]
            elif key == "frameitatic": self.frameitatic = kwarg[key]
            elif key == "framealias": self.framealias = kwarg[key]
            elif key == "value": self.value = kwarg[key]
            elif key == "step": self.step = kwarg[key]
            else: raise ValueError("Invalid Arguement")

        self._frame = StaticFrame(self.master,width=self.width+self.borderwidth*4,height=self.height+self.borderwidth*4,\
                            borderwidth=0,bordercolor=self.bordercolor,\
                            header=0)

        self._entry = Entry(self._frame,width=self.width//2,height=self.height,\
                               font=self.framefont,fontsize=self.framefontsize,bold=self.framebold,\
                               italic=self.frameitatic,antialias=self.framealias,borderwidth=self.frameborderwidth)

        self._up = Button(self._frame,width=self.width//2,height=self.height//2-self.borderwidth*2,target=self.stepUp,\
                               font=self.framefont,fontsize=self.framefontsize//2,bold=self.framebold,text="+",\
                               italic=self.frameitatic,antialias=self.framealias,borderwidth=self.frameborderwidth)

        self._down = Button(self._frame,width=self.width//2,height=self.height//2-self.borderwidth*2,target=self.stepDown,\
                               font=self.framefont,fontsize=self.framefontsize//2,bold=self.framebold,text="-",\
                               italic=self.frameitatic,antialias=self.framealias,borderwidth=self.frameborderwidth)

        self._entry.place((0,0))
        self._entry.set(str(self.value))
        self._up.place((self.width//2,0))
        self._down.place((self.width//2,self._entry.height//2+self.borderwidth*2))

        _widgets.append(self)

    def get(self,x,y):
        return int(self._entry.get())

    def set(self,value,x,y):
        self._entry.set(value)

    def stepUp(self):
        self._entry.set(str(int(self._entry.get())+self.step))
        self.value = int(self._entry.get())+self.step

    def stepDown(self):
        self._entry.set(str(int(self._entry.get())-self.step))
        self.value = int(self._entry.get())-self.step

    def place(self,pos):
        self.pos = pos
        self._frame.pos = pos
        self.isRendering = True
        _widgets.sort(key=get_priority,reverse=True)
        if type(self.master) in (DropFrame,Frame,StaticFrame,Label,XFrame):
            self.master.placed_obj.append(self._frame)

    def render(self):
        try:
            if self.master and self.isRendering:
                self.master.blit(self._frame.image,self.pos)
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

class MessageVariable:

    def __init__(self):
        self.text = ""
        self.isClosed = False

    def set(self,s):
        self.text = s

    def get(self):
        return self.text

def createMessageBox(screen,message):

    def close():
        nonlocal tmpFrame
        tmpFrame.kill()

    tmpFrame = Frame(screen,htitle="Message",width=300,height=100)
    t = TypableSurface((190,90),text=message)
    tmpButton = Button(tmpFrame,width=50,height=20,text="Close",target=close)
    tmpFrame.blit(t,(10,10))
    tmpButton.place((122,74))
    tmpFrame.place((screen.get_width()//2-150,screen.get_height()//2-50))

    return tmpFrame

def createWarning(screen,message):

    def close():
        nonlocal tmpFrame
        tmpFrame.kill()

    # Creation
    tmpFont = font.SysFont("Arial",34)
    tmpText = tmpFont.render("!",1,(0,0,0))
    tmpFrame = Frame(screen,htitle="Warning",width=300,height=100)
    t = TypableSurface((160,90),text=message)
    tmpSurface = Surface((42,36))
    tmpButton = Button(tmpFrame,width=50,height=20,text="Ok",target=close)
    # Assembly
    tmpSurface.fill((255,255,255))
    draw.polygon(tmpSurface,(255,255,0),[(20,0),(0,35),(40,35)])
    draw.polygon(tmpSurface,(0,0,0),[(20,0),(0,35),(40,35)],3)
    tmpSurface.blit(tmpText,(16,0))
    tmpFrame.blit(tmpSurface,(2,10))
    tmpFrame.blit(t,(50,10))
    tmpButton.place((122,74))
    tmpFrame.place((screen.get_width()//2-150,screen.get_height()//2-50))

    return tmpFrame

def createInputBox(screen,message):

    def close():
        nonlocal tmpFrame,tmpEntry
        nonlocal var
        var.set(tmpEntry.get())
        var.isClosed = True
        tmpFrame.kill()

    tmpFrame = Frame(screen,htitle="Message",width=300,height=100)
    t = TypableSurface((190,90),text=message)
    tmpEntry = Entry(tmpFrame,width=234,height=20)
    tmpButton = Button(tmpFrame,width=50,height=18,text="Enter",target=close)
    var = MessageVariable()
    tmpFrame.blit(t,(10,10))
    tmpEntry.place((2,72))
    tmpButton.place((242,72))
    tmpFrame.place((screen.get_width()//2-150,screen.get_height()//2-50))

    return tmpFrame,var