import pygame, math
import App, Entity

class Player:
    def __init__( self ):
        surf = pygame.display.get_surface()
        self.pos = pygame.Vector2( surf.get_width() / 2, surf.get_height() / 2 )
        self.dir = pygame.Vector2()
        self.speed = 200
        self.r = 10
        self.maxHp = 100
        self.hp = 100
        self.cooldownLvl = 2
        self.cooldown = App.Cooldown( self.cooldownLvl )
        self.hitCooldown = App.Cooldown( 1 )
        self.force = 50
        self.attack = 2
        self.bullets = []
    
    def update( self ):
        
        if App.keys.LEFT:
            self.dir[ 0 ] = -1
        elif App.keys.RIGHT:
            self.dir[ 0 ] = 1
        else:
            self.dir[ 0 ] = 0
            
        if App.keys.UP:
            self.dir[ 1 ] = -1
        elif App.keys.DOWN:
            self.dir[ 1 ] = 1
        else:
            self.dir[ 1 ] = 0
            
        if self.dir[ 0 ] != 0 or self.dir[ 1 ] != 0:
            self.dir = self.dir.normalize()
        
        self.pos += self.dir * ( self.speed / 60 )
        
        if not self.cooldown.run and App.mouse.DOWN:
            self.cooldown.start()
            dir = math.atan2( App.mouse.Y - self.pos[ 1 ], App.mouse.X - self.pos[ 0 ] )
            self.bullets.append( Entity.Bullet( self.pos, dir, self.attack ) )
        
        self.cooldown.update()
        if len( self.bullets ):
            for bullet in self.bullets:
                bullet.update()
                if bullet.outOfScreen():
                    self.bullets.remove( bullet )
                    
        self.hitCooldown.update()
    
    def hit( self, enemy ):
        if not self.hitCooldown.run and math.sqrt( math.pow( self.pos[ 0 ] - enemy.pos[ 0 ], 2 ) + math.pow( self.pos[ 1 ] - enemy.pos[ 1 ], 2 ) ) <= self.r + enemy.r:
            self.hp -= enemy.attack
            self.hitCooldown.start()
    
    def render( self ):
        surf = pygame.display.get_surface()
        pygame.draw.circle( surf, '#ffffff' if not self.hitCooldown.run else '#ff0000', self.pos, self.r )
        if len( self.bullets ):
            for bullet in self.bullets:
                bullet.render()