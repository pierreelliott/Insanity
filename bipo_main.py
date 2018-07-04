# -*- coding: Latin-1 -*-
#-------------------------------------------------------------------------------
# Name:        Bipo Maze
# Author:      Jimmy (WoofWoofDude)
# Created:     2012/04/06
# Python:      3.2.2 (default, Sep  4 2011, 09:51:08) [MSC v.1500 32 bit (Intel)]
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#-----------------------Libs import-----------------------#
from pygame import init, display, Color, key, quit, joystick, font
from pygame.locals import *
from sys import exit
# FIN
import time;
import pygame;

#-----------------------Local import-----------------------#
from tygame.main import StaticFrame, Button, Label, render_widgets, handle_widgets #But you can put in ..\Python\Lib\site-packages
from BipoClasse import *

# FIN

def main(difficulty):
    #---------------------Pygame init--------------------#

    myfont = font.SysFont("monospace", 15)
    #Création de la fenêtre
    WW, WH = 640, 480
    Window = display.set_mode((WW, WH))

    #icone = image.load("Bipo.png")
    #icone.set_colorkey(const.pink)
    #display.set_icon(icone)
    # FIN

    if difficulty == 0:
        time_limit = 40
    elif difficulty == 1:
        time_limit = 30
    elif difficulty == 2:
        time_limit = 20


    #---------------------Some variables--------------------#
    mylaby = laby(5, 5)
    mylaby.generate_laby()
    perso = Perso(mylaby)

    perso_time = 0
    display.flip()
    key.set_repeat(50, 55)
    # FIN

    first_time = time.time()




    while True:
        current_time = time.time()
        Window.fill(const.Porange)

        time_play = int(current_time - first_time)
        label = myfont.render(str(time_limit - time_play), 1, (0,0,0))
        Window.blit(label, (200, 0))


        if time_play >= time_limit:
            return -1

        for event in handle_widgets():
            if event.type == QUIT:
                quit()
                exit()

        pygame.time.wait(50)
        keys = key.get_pressed()
        if keys:
            if keys[K_UP]:
                if not perso.che_jaune:
                    perso.move(const.up)
            if keys[K_DOWN]:
                if not perso.che_jaune:
                    perso.move(const.down)
            if keys[K_LEFT]:
                if not perso.che_jaune:
                    perso.move(const.left)
            if keys[K_RIGHT]:
                if not perso.che_jaune:
                    perso.move(const.right)


        perso.show(Window)
        render_widgets()
        display.flip()

        if perso.x == perso.laby.w - 1 and perso.y == perso.laby.h - 1:
            return 0
