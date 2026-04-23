import pygame
import App, Entity

class Game:
    def __init__( self ):
        self.window = pygame.display.set_mode( ( 800, 600 ) )
        pygame.display.set_caption( 'Vampirek' )
        self.cooldownClick = App.Cooldown( .1 )
        self.player = Entity.Player()
        self.clock = pygame.time.Clock()
        self.cross = Entity.Cross()
        self.hud = App.Hud()
        self.enemies = []
        self.particles = []
        self.drop = []
        self.enemyTimeToUpdate = 60
        self.enemyTimeToUpdateTimer = 0
        self.enemySpawnTime = 5
        self.enemyLvl = 1
        self.enemySpawn = App.Cooldown( self.enemySpawnTime )
        self.state = 'menu'
        self.font = pygame.font.SysFont( 'Arial', 32, True )
        self.fontSmall = pygame.font.SysFont( 'Arial', 16, True )
        
        self.labels = {
            'vampirek' : App.Label( self.font, 'Vampirek', self.window.get_width() / 2, 60 ),
            'sklep' : App.Label( self.font, 'Sklep', self.window.get_width() / 2, 60 ),
            'koniec' : App.Label( self.font, 'Koniec gry', self.window.get_width() / 2, 60 ),
            'czas' : App.Label( self.fontSmall, 'Twój czas', self.window.get_width() / 2, 100 ),
            'punktyExp' : App.Label( self.fontSmall, f'Punkty doświadczenia: { self.hud.exp }', self.window.get_width() / 2, 100 ),
            'heal' : App.Label( self.fontSmall, f'Leczenie:', self.window.get_width() / 2 - 100, 200 ),
            'cooldownLvl' : App.Label( self.fontSmall, f'Sybkostrzelność: { App.updates.cooldownLvl[ 0 ] }', self.window.get_width() / 2 - 100, 250 ),
            'maxHp' : App.Label( self.fontSmall, f'Maksymalne życie: { App.updates.maxHp[ 0 ] }', self.window.get_width() / 2 - 100, 300 ),
            'attackLvl' : App.Label( self.fontSmall, f'Siła ataku: { App.updates.attackLvl[ 0 ] }', self.window.get_width() / 2 - 100, 350 ),
            'magnetSpeed' : App.Label( self.fontSmall, f'Siła przyciągania EXPA: { App.updates.magnetSpeed[ 0 ] }', self.window.get_width() / 2 - 100, 400 ),
            'magnetRadius' : App.Label( self.fontSmall, f'Zasięg przyciągania EXPA: { App.updates.magnetRadius[ 0 ] }', self.window.get_width() / 2 - 120, 450 )
        }
                
        self.buttons = {
            'start' : App.Button( self.font, 'Start', self.window.get_width() / 2 - 100, self.window.get_height() / 2 - 50, 200, 100 ),
            'retry' : App.Button( self.font, 'Spróbuj ponownie', self.window.get_width() / 2 - 200, self.window.get_height() / 2 - 50, 400, 100 ),
            'back' : App.Button( self.font, 'Wróć', self.window.get_width() / 2 - 100, self.window.get_height() - 60, 200, 50 ),
            'heal' : App.Button( self.fontSmall, f'Ulecz ( koszt: { App.updates.heal[ 1 ] } )', self.window.get_width() / 2 + 10, 175, 150, 50 ),
            'cooldownLvl' : App.Button( self.fontSmall, f'Ulepsz ( koszt: { App.updates.cooldownLvl[ 1 ] } )', self.window.get_width() / 2 + 10, 225, 150, 50 ),
            'maxHp' : App.Button( self.fontSmall, f'Ulepsz ( koszt: { App.updates.maxHp[ 1 ] } )', self.window.get_width() / 2 + 10, 275, 150, 50 ),
            'attackLvl' : App.Button( self.fontSmall, f'Ulepsz ( koszt: { App.updates.attackLvl[ 1 ] } )', self.window.get_width() / 2 + 10, 325, 150, 50 ),
            'magnetSpeed' : App.Button( self.fontSmall, f'Ulepsz ( koszt: { App.updates.magnetSpeed[ 1 ] } )', self.window.get_width() / 2 + 10, 375, 150, 50 ),
            'magnetRadius' : App.Button( self.fontSmall, f'Ulepsz ( koszt: { App.updates.magnetRadius[ 1 ] } )', self.window.get_width() / 2 + 10, 425, 150, 50 )
        }
        
        self.loop()
        
    def loop( self ):
        while App.eventsloop.running:
            App.eventsloop.update()
            self.window.fill( '#222222' )
            self.update()
            self.render()
            self.clock.tick( 60 )
            pygame.display.update()
    
    def update( self ):
        
        self.cross.update()
        self.cooldownClick.update()
        
        match self.state:
            case 'menu':
                if self.buttons[ 'start' ].hitTest() and App.mouse.DOWN:
                    self.state = 'play'
                    self.player.cooldown.start()
            case 'play':
                self.enemyTimeToUpdateTimer += 1 / 60
                if self.enemyTimeToUpdateTimer >= self.enemyTimeToUpdate:
                    self.enemyTimeToUpdateTimer = 0
                    self.enemySpawnTime -= .05
                    self.enemyLvl += 1
                    self.enemySpawn.setTime( self.enemySpawnTime )
                self.hud.update()
                self.enemySpawn.update()
                if not self.enemySpawn.run:
                    self.enemySpawn.start()
                    self.enemies.append( Entity.Enemy( self.enemyLvl ) )
                self.player.update()
                
                if len( self.enemies ):
                    for enemy in self.enemies:
                        self.player.hit( enemy )
                        enemy.update( self.player.pos )
                        if len( self.player.bullets ):
                            for bullet in self.player.bullets:
                                if enemy.hit( bullet ):
                                    self.player.bullets.remove( bullet )
                                    if enemy.hp <= 0:
                                        self.particles.append( App.Particles( enemy.pos[ 0 ], enemy.pos[ 1 ] ) )
                                        self.drop.append( Entity.Exp( enemy.pos[ 0 ], enemy.pos[ 1 ] ) )
                                        self.enemies.remove( enemy )
                                        self.hud.score += 1
                
                if len( self.particles ):
                    for particles in self.particles:
                        particles.update()
                        if not len( particles.particles ):
                            self.particles.remove( particles )
                
                if len( self.drop ):
                    for drop in self.drop:
                        drop.update( self.player )
                        if drop.collide( self.player ):
                            self.drop.remove( drop )
                            self.hud.exp += 1
                            
                if self.player.hp <= 0:
                    self.state = 'gameover'
                    
                if App.keys.E:
                    self.state = 'shop'
                    
            case 'shop':
                if not self.cooldownClick.run and App.mouse.DOWN:
                    if self.buttons[ 'cooldownLvl' ].hitTest():
                        if App.updates.cooldownLvl[ 0 ] <= App.updates.cooldownLvl[ 2 ] and self.hud.exp >= App.updates.cooldownLvl[ 1 ]:
                            self.hud.exp -= App.updates.cooldownLvl[ 1 ]
                            App.updates.cooldownLvl[ 0 ] += 1
                            App.updates.cooldownLvl[ 1 ] = int( App.updates.cooldownLvl[ 1 ] * 1.5 )
                            self.player.cooldownLvl /= 2
                            self.player.cooldown.setTime( self.player.cooldownLvl )
                    if self.buttons[ 'heal' ].hitTest():
                        if self.hud.exp >= App.updates.heal[ 1 ]:
                            self.hud.exp -= App.updates.heal[ 1 ]
                            App.updates.heal[ 0 ] += 1
                            App.updates.heal[ 1 ] += 5
                            self.player.hp = self.player.maxHp
                    if self.buttons[ 'maxHp' ].hitTest():
                        if self.hud.exp >= App.updates.maxHp[ 1 ]:
                            self.hud.exp -= App.updates.maxHp[ 1 ]
                            App.updates.maxHp[ 0 ] += 1
                            App.updates.maxHp[ 1 ] *= 2
                            self.player.maxHp += 50
                            self.player.hp = self.player.maxHp
                    if self.buttons[ 'attackLvl' ].hitTest():
                        if self.hud.exp >= App.updates.attackLvl[ 1 ]:
                            self.hud.exp -= App.updates.attackLvl[ 1 ]
                            App.updates.attackLvl[ 0 ] += 1
                            App.updates.attackLvl[ 1 ] *= 3
                            self.player.attack *= 2
                    if self.buttons[ 'magnetSpeed' ].hitTest():
                        if App.updates.magnetSpeed[ 0 ] <= App.updates.magnetSpeed[ 2 ] and self.hud.exp >= App.updates.magnetSpeed[ 1 ]:
                            self.hud.exp -= App.updates.magnetSpeed[ 1 ]
                            App.updates.magnetSpeed[ 0 ] += 1
                            App.updates.magnetSpeed[ 1 ] *= 3
                    if self.buttons[ 'magnetRadius' ].hitTest():
                        if App.updates.magnetRadius[ 0 ] <= App.updates.magnetRadius[ 2 ] and self.hud.exp >= App.updates.magnetRadius[ 1 ]:
                            self.hud.exp -= App.updates.magnetRadius[ 1 ]
                            App.updates.magnetRadius[ 0 ] += 1
                            App.updates.magnetRadius[ 1 ] *= 3
                        
                    if self.buttons[ 'back' ].hitTest():
                        self.player.cooldown.start()
                        self.state = 'play'
                
            case 'gameover':
                if self.buttons[ 'retry' ].hitTest() and not self.cooldownClick.run and App.mouse.DOWN:
                    self.reset()
                    self.state = 'play'
                    
        if not self.cooldownClick.run and App.mouse.DOWN:
            self.cooldownClick.start()
              
    def reset( self ):
        self.player.cooldown.start()
        self.player.hitCooldown.start()
        self.hud.exp = 0
        self.hud.score = 0
        self.enemies = []
        self.particles = []
        self.drop = []
        self.player.bullets = []
        self.player.maxHp = 100
        self.player.hp = 100
        self.player.pos = pygame.Vector2( self.window.get_width() / 2, self.window.get_height() / 2 )
        self.enemyTimeToUpdate = 60
        self.enemyTimeToUpdateTimer = 0
        self.enemySpawnTime = 5
        self.enemyLvl = 1
        self.enemySpawn.setTime( self.enemySpawnTime )
        App.updates.cooldownLvl[ 0 ] = 1
        App.updates.cooldownLvl[ 1 ] = 10
        self.player.cooldownLvl = 2
        self.player.cooldown.setTime( self.player.cooldownLvl )
        App.updates.heal[ 0 ] = 1
        App.updates.heal[ 1 ] = 5
        App.updates.maxHp[ 0 ] = 1
        App.updates.maxHp[ 1 ] = 20
        App.updates.attackLvl[ 0 ] = 1
        App.updates.attackLvl[ 1 ] = 10
        self.player.attack = 2
        self.hud.timer = 0
        App.updates.magnetSpeed[ 0 ] = 1
        App.updates.magnetSpeed[ 1 ] = 5
        App.updates.magnetRadius[ 0 ] = 1
        App.updates.magnetRadius[ 1 ] = 5
              
    def render( self ):
        match self.state:
            case 'menu':
                self.labels[ 'vampirek' ].render()
                self.buttons[ 'start' ].render()
            case 'play':
                self.player.render()
                
                if len( self.enemies ):
                    for enemy in self.enemies:
                        enemy.render()
                        
                if len( self.particles ):
                    for particles in self.particles:
                        particles.render()
                        
                if len( self.drop ):
                    for drop in self.drop:
                        drop.render()
                self.hud.render( self.player )
                
            case 'shop':
                self.labels[ 'sklep' ].render()
                
                self.labels[ 'punktyExp' ].setLabel( f'Punkty doświadczenia: { self.hud.exp }' )
                self.labels[ 'punktyExp' ].render()
                
                self.labels[ 'cooldownLvl' ].setLabel( f'Sybkostrzelność: { App.updates.cooldownLvl[ 0 ] }' )
                self.labels[ 'cooldownLvl' ].render()
                
                self.buttons[ 'cooldownLvl' ].setLabel( f'Ulepsz ( koszt: { App.updates.cooldownLvl[ 1 ] } )' )
                if App.updates.cooldownLvl[ 0 ] < App.updates.cooldownLvl[ 2 ]:
                    self.buttons[ 'cooldownLvl' ].render()
                
                self.labels[ 'heal' ].render()
                
                self.buttons[ 'heal' ].setLabel( f'Ulecz ( koszt: { App.updates.heal[ 1 ] } )' )
                self.buttons[ 'heal' ].render()
                
                self.labels[ 'maxHp' ].setLabel( f'Maksymalne życie: { App.updates.maxHp[ 0 ] }' )
                self.labels[ 'maxHp' ].render()
                
                self.buttons[ 'maxHp' ].setLabel( f'Ulepsz ( koszt: { App.updates.maxHp[ 1 ] } )' )
                self.buttons[ 'maxHp' ].render()
                
                self.labels[ 'attackLvl' ].setLabel( f'Siła ataku: { App.updates.attackLvl[ 0 ] }' )
                self.labels[ 'attackLvl' ].render()
                
                self.buttons[ 'attackLvl' ].setLabel( f'Ulepsz ( koszt: { App.updates.attackLvl[ 1 ] } )' )
                self.buttons[ 'attackLvl' ].render()
                
                self.labels[ 'magnetSpeed' ].setLabel( f'Siła przyciągania EXPA: { App.updates.magnetSpeed[ 0 ] }' )
                self.labels[ 'magnetSpeed' ].render()
                
                self.buttons[ 'magnetSpeed' ].setLabel( f'Ulepsz ( koszt: { App.updates.magnetSpeed[ 1 ] } )' )
                if App.updates.magnetSpeed[ 0 ] < App.updates.magnetSpeed[ 2 ]:
                    self.buttons[ 'magnetSpeed' ].render()
                
                self.labels[ 'magnetRadius' ].setLabel( f'Promień przyciągania EXPA: { App.updates.magnetRadius[ 0 ] }' )
                self.labels[ 'magnetRadius' ].render()
                
                self.buttons[ 'magnetRadius' ].setLabel( f'Ulepsz ( koszt: { App.updates.magnetRadius[ 1 ] } )' )
                if App.updates.magnetRadius[ 0 ] < App.updates.magnetRadius[ 2 ]:
                    self.buttons[ 'magnetRadius' ].render()
                
                self.buttons[ 'back' ].render()
            case 'gameover':
                self.labels[ 'koniec' ].render()
                
                self.labels[ 'czas' ].setLabel( f'Twój czas: { int( self.hud.timer ) }' )
                self.labels[ 'czas' ].render()
                
                self.buttons[ 'retry' ].render()
                
        self.cross.render()