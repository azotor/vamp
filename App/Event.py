import pygame

class EventsLoop:
    def __init__( self ):
        self.running = True
        pygame.mouse.set_visible( False )
    
    def update( self ):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        pressed = pygame.key.get_pressed()
        
        keys.UP = pressed[ pygame.K_UP ] or pressed[ pygame.K_w ]
        keys.RIGHT = pressed[ pygame.K_RIGHT ] or pressed[ pygame.K_d ]
        keys.DOWN = pressed[ pygame.K_DOWN ] or pressed[ pygame.K_s ]
        keys.LEFT = pressed[ pygame.K_LEFT ] or pressed[ pygame.K_a ]
        keys.E = pressed[ pygame.K_e ]
        
        pos = pygame.mouse.get_pos()
        mouse.X = pos[ 0 ]
        mouse.Y = pos[ 1 ]
        
        pressed = pygame.mouse.get_pressed()
        mouse.DOWN = pressed[ 0 ]
                
class Keys:
    UP = False
    RIGHT = False
    DOWN = False
    LEFT = False
    E = False

class Mouse:
    X = 0
    Y = 0
    DOWN = False
                    
keys = Keys()
mouse = Mouse()
eventsloop = EventsLoop()