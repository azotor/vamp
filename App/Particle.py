import pygame, random

class Particle:
    def __init__( self, x, y ):
        self.pos = pygame.Vector2( x, y )
        self.dir = pygame.Vector2( random.randint( -2, 2 ), random.randint( -2, 2 ) )
        self.opacity = 1
        
    def update( self ):
        self.pos += self.dir
        self.opacity -= random.randint( 2, 5 ) * .01
    
    def render( self ):
        surf = pygame.display.get_surface()
        pygame.draw.circle( surf, '#cccccc', self.pos, 2 )