import App

class Particles:
    def __init__( self, x, y ):
        self.particles = [ App.Particle( x, y ) for i in range( 10 ) ]
    
    def update( self ):
        for particle in self.particles:
            particle.update()
            if particle.opacity <= 0:
                self.particles.remove( particle )
    
    def render( self ):
        for particle in self.particles:
            particle.render()
