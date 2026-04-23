import pygame

class Label:
    def __init__( self, font, label, x, y ):
        self.font = font
        self.label = label
        self.x = x
        self.y = y
    
    def setLabel( self, label ):
        self.label = label
    
    def render( self ):
        surf = pygame.display.get_surface()
        text = self.font.render( self.label, True, '#ffffff' )
        text_rect = text.get_rect()
        text_rect.center = ( self.x, self.y )
        surf.blit( text, text_rect )