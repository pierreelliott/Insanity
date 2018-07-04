# -*- coding: Latin-1 -*-
#-------------------------------------------------------------------------------
# Name:        Bipo Maze
# Author:      Jimmy (WoofWoofDude)
# Created:     2012/04/06
# Python:      3.2.2 (default, Sep  4 2011, 09:51:08) [MSC v.1500 32 bit (Intel)]
#-------------------------------------------------------------------------------


from pygame import image, Rect, draw, Surface
from pygame.locals import *
from random import randint, choice


"""
Tous les Class utilisées:
"""
class def_const(object):
    def __getattr__(self, attr):
        return const.__dict__[attr]

    def __setattr__ (self, attr, value):
        if attr in self.__dict__.keys():
            raise Exception("Impossible de redefinir une constante")
        else:
            self.__dict__[attr] = value

    def __str__(self):
        return self.__dict__.__str__()


const = def_const ()
""" definitions des constantes """

# Couleurs
const.white  = (255 , 255 , 255)
const.pink   = (255 , 0 , 255)
const.black  = (0 , 0 , 0)
const.yellow = (255 , 255 , 0)
const.red = (255 , 0 , 0)
const.green = (0, 255, 0)

const.Pgreen = (192, 234, 68)
const.Porange = (255, 201, 14)
const.Pblue = (18, 204, 214)

#directions
const.right = 0
const.left = 1
const.up = 2
const.down = 3

# autres

const.wc = 16 # width d'un seul carreau du laby
const.hc = 16 # height d'un seul carreau du laby

const.time_perso_poll = 75

""" fin definitions des constantes"""

class Point(object):
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]


class Case(object):
    """
    Case est une case du laby.
    """

    def __init__(self):
        self.state = False
        self.gate = [True, True, True, True] # D, G, H, B


class CaseCouleur(object):
    """
    Case de départ et de fin
    """
    def __init__(self, Pos, couleur):
        self.pos = Pos

        self.surf = Surface((const.wc, const.hc))
        self.surf.fill(couleur)


class Perso(object):
    """
    Le Personage
    """
    def __init__(self, laby):
        self.x = 0
        self.y = 0

        self.chemain = None
        self.che_jaune = []
        self.reverse = 0

        self.laby = laby

        self.img = image.load("assets/Bipo.png").convert()
        self.img.set_colorkey(const.pink)
        self.rect_img = self.img.get_rect()
        self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)

        self.dep = CaseCouleur((0, 0), const.green)
        self.fin = CaseCouleur(((self.laby.w * const.wc - const.wc), (self.laby.h * const.hc - const.hc)), const.red)


    def show(self, screen):

        caseL = []

        if self.che_jaune:

            if self.reverse == 0:
                self.che_jaune.reverse()
                self.reverse = 1


            for id, c in enumerate(self.che_jaune):
                    caseL.append(CaseCouleur(((c.x * const.wc), (c.y * const.hc)), const.yellow))



        caseL.reverse()
        for c in caseL:
            screen.blit(c.surf, c.pos)

        screen.blit(self.dep.surf, self.dep.pos)
        screen.blit(self.fin.surf, self.fin.pos)
        screen.blit(self.img, self.rect_img)


        self.laby.show(screen)

    def move(self, dir):
        if not self.laby.get_cell(self.x, self.y).gate[dir]:

            if dir == const.right and self.x + 1 < self.laby.w:
                self.x += 1
            if dir == const.left and self.x - 1 >= 0:
                self.x -= 1
            if dir == const.up and self.y - 1 >= 0:
                self.y -= 1
            if dir == const.down and self.y + 1 < self.laby.h:
                self.y += 1

            self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)



class laby(object):
    def __init__(self, w = 25, h = 30, sx = 0, sy = 0):
        self.w = w
        self.h = h

        self.cases = []
        self.wc = const.wc
        self.hc = const.hc

        self.sx = sx
        self.sy = sy

        for v in range(self.w * self.h):
            a = Case()
            a.x = v % self.w
            a.y = int(v / self.w)
            self.cases.append(a)

    def get_cell(self, x, y):
        return self.cases[(y*self.w) + x]

    def notdir(self, dir):
        if dir == const.right:
            return const.left
        if dir == const.left:
            return const.right
        if dir == const.up:
            return const.down
        if dir == const.down:
            return const.up

    def generate_laby(self, x = -1, y = -1):
        if x == -1:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)

        cell_act = self.get_cell(x, y)

        if not cell_act.state:
            cell_act.state = True

            tab = []

            if x + 1 < self.w and not self.get_cell(x + 1, y).state:
                tab.append((x + 1, y, const.right))
            if x - 1 >= 0 and not self.get_cell(x - 1, y).state:
                tab.append((x - 1, y, const.left))
            if y + 1 < self.h and not self.get_cell(x, y + 1).state:
                tab.append((x, y + 1, const.down))
            if y - 1 >= 0 and not self.get_cell(x, y - 1).state:
                tab.append((x, y - 1, const.up))


            if tab:
                while tab:
                    C = choice(tab)

                    if not self.get_cell(C[0], C[1]).state:

                        cell = self.get_cell(C[0], C[1])
                        cell_act.gate[C[2]] = False
                        cell.gate[self.notdir(C[2])] = False
                        self.generate_laby(C[0], C[1])

                    else:
                        tab.remove(C)

    def show(self, screen):
        W, H = self.wc, self.hc
        sx , sy = self.sx, self.sy

        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)

                if c.gate[const.right]:
                    draw.line(screen, const.black, (sx + ((x + 1) * W), (sy + (y * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)
                if c.gate[const.down]:
                    draw.line(screen, const.black, ((sx + (x * W)), (sy + ((y+1) * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)

        x = self.w - 1

        for y in range(self.h - 1):
            c = self.get_cell(x, y)

            if c.gate[const.down]:
                draw.line(screen, const.black, ((sx + (x * W)), (sy + ((y+1) * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)

        y = self.h - 1

        for x in range(self.w - 1):
            c = self.get_cell(x, y)

            if c.gate[const.right]:
                draw.line(screen, const.black, (sx + ((x + 1) * W), (sy + (y * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)



        draw.rect(screen, const.black, (sx, sy, W * self.w, H * self.h), 2)
