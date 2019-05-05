import pygame
import random

from pygame.locals import *

WINDOW_W = 800
WINDOW_H = 600
FPS = 40
speed = 16

#Colours
COL_WHITE = (255,255,255)
COL_BLACK = (0,0,0)
COL_GREEN = (0,255,0)
COL_RED = (255,0,0)

def main():
    global CLOCK, DISPLAY

    pygame.init()
    DISPLAY = pygame.display.set_mode( (800, 600) )
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Rect chasing")
    target_rect = generate_target_rect( True )
    print("Target rect: " + str( target_rect.tl ))
    current_rect = generate_dynamic_rect( target_rect, False )
    animation_running = True

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        DISPLAY.fill(COL_BLACK)
        pygame.draw.rect(DISPLAY, target_rect.col, [ target_rect.tl.x, target_rect.tl.y, target_rect.w, target_rect.h ] )
        pygame.draw.rect(DISPLAY, current_rect.col, [ current_rect.tl.x, current_rect.tl.y, current_rect.w, current_rect.h ] )
        
        
        if animation_running:
            if current_rect == target_rect:
                current_rect.col = COL_GREEN
                animation_running = False
            else:
                update_rects(current_rect)
        else:
            target_rect = generate_target_rect(True)
            current_rect.update_target( target_rect )
            animation_running = True
        current_rect.update()

        pygame.display.update()
        CLOCK.tick( FPS )

def generate_dynamic_rect( target, is_random ):
    if is_random:
        top_left = Coordinate(random.randrange(0, WINDOW_W, 10), random.randrange(0, WINDOW_H, 10), target.tl)
        top_right = Coordinate(random.randrange(top_left.x, WINDOW_W, 10), top_left.y, target.tr)
        bottom_right = Coordinate(top_right.x, random.randrange(top_right.y, WINDOW_H, 1), target.br)
        bottom_left = Coordinate(top_left.x, bottom_right.y, target.bl)
        return Rect( top_left, top_right, bottom_right, bottom_left)
    else:
        top_left = Coordinate(110, 110, target.tl, "top left")
        top_right = Coordinate(130, 110, target.tr, "top right")
        bottom_right = Coordinate(130, 140, target.br, "bottom right")
        bottom_left = Coordinate(110, 140, target.bl, "bottom left")
    return Rect( top_left, top_right, bottom_right, bottom_left, COL_RED )

def generate_target_rect( is_random ):
    if is_random:
        top_left = Coordinate(random.randrange(0, WINDOW_W, 10), random.randrange(0, WINDOW_H, 10))
        top_right = Coordinate(random.randrange(top_left.x, WINDOW_W, 10), top_left.y)
        bottom_right = Coordinate(top_right.x, random.randrange(top_right.y, WINDOW_H, 10))
        bottom_left = Coordinate(top_left.x, bottom_right.y)
    else:
        top_left = Coordinate(10, 140)
        top_right = Coordinate(30, 10)
        bottom_right = Coordinate(30, 40)
        bottom_left = Coordinate(10, 230)
    return Rect( top_left, top_right, bottom_right, bottom_left, COL_WHITE )

def update_rects(current):
    for coord in current.coordinates:
        coord.advance_step()

class Coordinate:

    def __init__( self, x, y, target=0, name=0 ):
        self.x = x
        self.y = y
        self.target = target
        self.name = name
        if self.target:
            self.step = Coordinate( (target.x - self.x)/speed, (target.y - self.y)/speed )
    
    def __eq__( self, other ):
        print("Checking coordinate equality: " + self.name)
        print("self.x: " + str( self.x ) + " other.x: " + str( other.x ))
        print("self.y: " + str( self.y ) + " other.y: " + str( other.y ))
        equal = (self.x == other.x and self.y == other.y)
        print( str( equal ))
        return equal
    
    def __add__( self, other ):
        self.x = self.x + other.x
        self.y = self.y + other.y

    def advance_step( self ):
        if self == self.target:
            print( "Coordinate reached" )
        else:
            print( self.step.x )
            print( self.step.y )
            self = self + self.step
    
    def update_target( self, new_target ):
        self.target = new_target
        self.step = Coordinate( (new_target.x - self.x)/speed, (new_target.y - self.y)/speed )
        


class Rect:

    def __init__( self, top_left, top_right, bottom_right, bottom_left, colour ):
        self.tl = top_left
        self.tr = top_right
        self.br = bottom_right
        self.bl = bottom_left
        self.col = colour
        self.coordinates = [self.tl, self.tr, self.br, self.bl]
        self.h = self.bl.y - self.tl.y
        self.w = self.tr.x - self.tl.x

    def update( self ):
        self.h = self.bl.y - self.tl.y
        self.w = self.tr.x - self.tl.x

    def __eq__(self, other):
        return (self.tl.x == other.tl.x and self.tl.y == other.tl.y and self.w == other.w and self.h == other.h)

    def update_target( self, target ):
        self.tl.update_target( target.tl )      
        self.tr.update_target( target.tr )       
        self.br.update_target( target.br )
        self.bl.update_target( target.bl )
        self.update()
        self.col = COL_RED

main()