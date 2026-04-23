import pygame, math

class Bullet:
    def __init__( self, pos, dir, attack ):
        self.pos = pygame.Vector2( pos[ 0 ], pos[ 1 ] )
        self.speed = 200
        self.r = 2
        self.attack = attack
        self.dir = pygame.math.Vector2.from_polar( ( 1, math.degrees( dir ) ) ) * self.speed * ( 60 / 1000 )
    
    def update( self ):
        self.pos += self.dir
    
    def render( self ):
        surf = pygame.display.get_surface()
        pygame.draw.circle( surf, '#00ff00', self.pos, self.r )
        
    def outOfScreen( self ):
        surf = pygame.display.get_surface()
        return self.pos[ 0 ] - self.r < 0 or self.pos[ 0 ] + self.r > surf.get_width() or self.pos[ 1 ] - self.r < 0 or self.pos[ 1 ] + self.r > surf.get_height()