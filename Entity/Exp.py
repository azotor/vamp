import pygame, math, random
import App

class Exp:
    def __init__( self, x, y ):
        self.pos = pygame.Vector2( x, y )
        self.dir = pygame.Vector2( random.randint( -2, 2 ), random.randint( -2, 2 ) )
        self.move = random.randint( 5, 10 )
        self.speed = 20
        
    def update( self, target ):
        if math.sqrt( math.pow( self.pos[ 0 ] - target.pos[ 0 ], 2 ) + math.pow( self.pos[ 1 ] - target.pos[ 1 ], 2 ) ) <= target.r + target.force * App.updates.magnetRadius[ 0 ]:
            self.move = 0
            dir = math.atan2( target.pos[ 1 ] - self.pos[ 1 ], target.pos[ 0 ] - self.pos[ 0 ] )
            self.dir = pygame.math.Vector2.from_polar( ( 1, math.degrees( dir ) ) ) * self.speed * App.updates.magnetSpeed[ 0 ] * ( 60 / 1000 )
            self.pos += self.dir
            
        if self.move > 0:
            self.move -= 1
            self.pos += self.dir
    
    def render( self ):
        surf = pygame.display.get_surface()
        pygame.draw.circle( surf, '#ffff55', self.pos, 2 )
        
    def collide( self, target ):
        return math.sqrt( math.pow( self.pos[ 0 ] - target.pos[ 0 ], 2 ) + math.pow( self.pos[ 1 ] - target.pos[ 1 ], 2 ) ) <= target.r + 4