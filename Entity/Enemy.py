import pygame, math, random, copy
import App

class Enemy:
    def __init__( self, lvl ):
        surf = pygame.display.get_surface()
        x = 0
        y = 0
        self.lvl = copy.copy( lvl )
        self.dir = pygame.Vector2()
        self.attack = 5 * self.lvl
        self.speed = 20 + self.lvl / 10
        self.r = 5 + self.lvl / 10
        self.hp = 10 + self.lvl / 3
        self.cooldown = App.Cooldown( 2 )
        self.bullets = []
        
        match random.randint( 0, 3 ):
            case 0 :
                x = -self.r
                y = random.randint( 0, surf.get_height() )
            case 1 :
                x = surf.get_width()
                y = random.randint( 0, surf.get_height() )
            case 2 :
                x = random.randint( 0, surf.get_width() )
                y = -self.r
            case 3 :
                x = random.randint( 0, surf.get_width() )
                y = surf.get_height()
        
        self.pos = pygame.Vector2( x, y )
        
    def update( self, player ):
        dir = math.atan2( player[ 1 ] - self.pos[ 1 ], player[ 0 ] - self.pos[ 0 ] )
        self.dir = pygame.math.Vector2.from_polar( ( 1, math.degrees( dir ) ) ) * self.speed * ( 60 / 1000 )
        self.pos += self.dir
    
    def render( self ):
        surf = pygame.display.get_surface()
        pygame.draw.circle( surf, ( 255, self.lvl * 10 % 360, 0, 0 ), self.pos, self.r )
        
    def hit( self, bullet ):
        if math.sqrt( math.pow( self.pos[ 0 ] - bullet.pos[ 0 ], 2 ) + math.pow( self.pos[ 1 ] - bullet.pos[ 1 ], 2 ) ) <= self.r + bullet.r:
            self.hp -= bullet.attack
            return True
        return False