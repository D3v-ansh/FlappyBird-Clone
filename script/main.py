import pygame, sys, time
from settings import *
from sprites import backGround, ground, plane, obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.windowSize = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption('Flappy Plane')
        self.clock = pygame.time.Clock()
        self.isRunning = True
        
        self.allSprites = pygame.sprite.Group()
        self.collisionSprites = pygame.sprite.Group()
        
        bgHeight = pygame.image.load('./assets/environment/background.png').convert().get_height()
        self.scaleFactor = windowHeight / bgHeight
        
        backGround(self.allSprites, self.scaleFactor)
        ground([self.allSprites, self.collisionSprites], self.scaleFactor)
        self.plane = plane(self.allSprites, self.scaleFactor / 2)
        
        self.obstacleTimer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacleTimer, 800)
        
        self.font = pygame.font.Font('./assets/fonts/BD_Cartoon_Shout.ttf', 50)
        self.score = 0
        
        self.startTime = 0
        
        self.menu = pygame.image.load('./assets/menu/menu.png').convert_alpha()
        self.menuRect = self.menu.get_rect(center = (windowWidth / 2, windowHeight / 2))
        
        self.backgroundMusic = pygame.mixer.Sound('./assets/sounds/music.wav')
        self.backgroundMusic.set_volume(0.2)
        self.backgroundMusic.play(loops = -1)
        
        
    def displayScore(self):
        if self.isRunning:
            self.score = (pygame.time.get_ticks() - self.startTime) // 1000
            scoreDisplayHeight = windowHeight / 10
        else:
            scoreDisplayHeight = windowHeight / 2 + (self.menuRect.height / 1.2)
        
        scoreSurface = self.font.render(str(self.score), True, (255, 154, 3))
        scoreRect = scoreSurface.get_rect(midtop = (windowWidth / 2, scoreDisplayHeight))
        
        self.windowSize.blit(scoreSurface, scoreRect)
    
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collisionSprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            for sprite in self.collisionSprites:
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.isRunning = False
            self.plane.kill()
    
    def run(self):
        lastTime = time.time()
        
        while True:
            dt = time.time() - lastTime
            lastTime = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isRunning:
                        self.plane.jump()
                    else:
                        self.isRunning = True
                        self.plane = plane(self.allSprites, self.scaleFactor / 2)
                        self.startTime = pygame.time.get_ticks()
                    
                if event.type == self.obstacleTimer and self.isRunning:
                    obstacle([self.allSprites, self.collisionSprites], self.scaleFactor)
                
            self.allSprites.update(dt)
            self.allSprites.draw(self.windowSize)
            
            self.displayScore()
            
            if self.isRunning:
                self.collisions()
            else:
                self.windowSize.blit(self.menu, self.menuRect)
                
            pygame.display.update()
            self.clock.tick(frameRate)
            
if __name__ == '__main__':
    game = Game()
    game.run() 