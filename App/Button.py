import pygame
import App

class Button:
    def __init__( self, font, label, x, y, width, height ):
        self.font = font
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def setLabel( self, label ):
        self.label = label
    
    def render( self ):
        surf = pygame.display.get_surface()
        if App.mouse.X >= self.x and App.mouse.X <= self.x + self.width and App.mouse.Y >= self.y and App.mouse.Y <= self.y + self.height:
                    pygame.draw.rect( surf, '#333333', ( self.x, self.y, self.width, self.height ) )
        pygame.draw.rect( surf, '#ffffff', ( self.x, self.y, self.width, self.height ), 1 )
        text = self.font.render( self.label, True, '#ffffff' )
        text_rect = text.get_rect()
        text_rect.center = ( self.x + self.width / 2, self.y + self.height / 2 )
        surf.blit( text, text_rect )
        
    def hitTest( self ):
        return App.mouse.X >= self.x and App.mouse.X <= self.x + self.width and App.mouse.Y >= self.y and App.mouse.Y <= self.y + self.height