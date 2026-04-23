class Cooldown:
    def __init__( self, time ):
        self.time = time
        self.timer = time
        self.run = False
        
    def setTime( self, time ):
        self.time = time
    
    def update( self ):
        if self.run:
            self.timer += 60 / 1000
            if self.timer >= self.time:
                self.timer = self.time
                self.run = False
    
    def start( self ):
        self.run = True
        self.timer = 0