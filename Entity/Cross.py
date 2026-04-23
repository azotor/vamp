import pygame
import App

class Cross:
    def __init__( self ):
        self.pos = pygame.Vector2()
    
    def update( self ):
        self.pos = pygame.Vector2( App.mouse.X, App.mouse.Y )
    
    def render( self ):
        surf = pygame.display.get_surface()
        color = '#ff0000' if App.mouse.DOWN else '#aaaaaa'
        pygame.draw.rect( surf, color, ( self.pos[ 0 ] - 2, self.pos[ 1 ] - 2, 5, 5 ), 1 )
        pygame.draw.line( surf, color, ( self.pos[ 0 ], self.pos[ 1 ] - 10 ), ( self.pos[ 0 ], self.pos[ 1 ] - 5 ) )
        pygame.draw.line( surf, color, ( self.pos[ 0 ], self.pos[ 1 ] + 10 ), ( self.pos[ 0 ], self.pos[ 1 ] + 5 ) )
        pygame.draw.line( surf, color, ( self.pos[ 0 ] - 10, self.pos[ 1 ] ), ( self.pos[ 0 ] - 5, self.pos[ 1 ] ) )
        pygame.draw.line( surf, color, ( self.pos[ 0 ] + 10, self.pos[ 1 ] ), ( self.pos[ 0 ] + 5, self.pos[ 1 ] ) )