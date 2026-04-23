import pygame

class Hud:
    def __init__( self ):
        self.score = 0
        self.exp = 0
        self.font = pygame.font.SysFont( 'Arial', 12, True )
        self.timer = 0
    
    def update( self ):
        self.timer += 1 / 60
    
    def render( self, player ):
        surf = pygame.display.get_surface()
        text = self.font.render( f'Punktacja: { self.score }', True, '#ffffff' )
        surf.blit( text, ( 10, 10 ) )
        text = self.font.render( f'Życie: { player.hp }', True, '#ffffff' )
        surf.blit( text, ( 200, 10 ) )
        text = self.font.render( f'Doświadczenie: { self.exp }', True, '#ffffff' )
        surf.blit( text, ( 400, 10 ) )
        text = self.font.render( f'Czas gry: { int( self.timer ) }', True, '#ffffff' )
        surf.blit( text, ( 550, 10 ) )
        text = self.font.render( f'Sklep - ( E )', True, '#ffffff' )
        surf.blit( text, ( 700, 10 ) )