import pygame
from random import choice, randint
from settings import *

class backGround(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
        
        bgImage = pygame.image.load('./assets/environment/background.png').convert()
        
        fullHeight = bgImage.get_height() * scaleFactor
        fullWidth = bgImage.get_width() * scaleFactor
        fullImage = pygame.transform.scale(bgImage,(fullWidth, fullHeight))
        
        self.image = pygame.Surface((fullWidth * 2,fullHeight))
        self.image.blit(fullImage, (0,0))
        self.image.blit(fullImage, (fullWidth,0))
        
        self.rect = self.image.get_rect(topleft = (0,0))    
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
    def update(self, dt):
        self.pos.x -= 300 * dt
        
        # if self.rect.right <= 0:
        #     self.pos.x = 0
        
        if self.rect.centerx <= 0:
            self.pos.x = 0
        
        self.rect.x = round(self.pos.x)
        
class ground(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor) :
        super().__init__(groups)
        self.sprite_type = 'ground'
        
        groundImage = pygame.image.load('./assets/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(groundImage, pygame.math.Vector2(groundImage.get_size()) * scaleFactor)
        
        self.rect = self.image.get_rect(bottomleft = (0, windowHeight))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.pos.x -= 350 * dt
        
        if self.rect.centerx <= 0:
            self.pos.x = 0
        
        self.rect.x = round(self.pos.x)
        
class plane(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
    
        self.getFrames(scaleFactor)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        
        self.rect = self.image.get_rect(midleft = (windowWidth / 25, windowHeight / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft) 
        
        self.gravity = 1000
        self.direction = 0
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.jumpSound = pygame.mixer.Sound('./assets/sounds/jump.wav')
        self.jumpSound.set_volume(0.15)
        
    def getFrames(self, scaleFactor):
        self.frames = []
        
        for img in range(3):
            currentPlaneImage = pygame.image.load(f'./assets/plane/plane{img}.png').convert_alpha()
            scaledPlanedImage = pygame.transform.scale(currentPlaneImage, pygame.math.Vector2(currentPlaneImage.get_size()) * scaleFactor)
            
            self.frames.append(scaledPlanedImage)
    
    def Applygravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
    
    def jump(self):
        self.jumpSound.play()
        self.direction = -400
    
    def animate(self, dt):
        self.frameIndex += 15 * dt
        if self.frameIndex >= len(self.frames): 
            self.frameIndex = 0
            
        self.image = self.frames[int(self.frameIndex)]
    
    def rotate(self):
        rotatedPlane = pygame.transform.rotozoom(self.image, -self.direction * 0.08 , 1)
        self.image = rotatedPlane
        
        self.mask = pygame.mask.from_surface(self.image)
      
    def update(self, dt):
        self.Applygravity(dt)
        self.animate(dt)
        self.rotate()
        
class obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'
        
        orientation = choice(('up', 'down'))
        ObstacleImage = pygame.image.load(f'./assets/obstacles/{choice((0, 1))}.png').convert_alpha()
        
        self.image = pygame.transform.scale(ObstacleImage, pygame.math.Vector2(ObstacleImage.get_size()) * scaleFactor) 
        
        if orientation == 'up':
            self.rect = self.image.get_rect(midbottom = (windowWidth + randint(40,100), windowHeight + randint(20,50)))
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (windowWidth + randint(40,100), randint(-50, -20)))
        
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        self.mask = pygame.mask.from_surface(self.image)
            
    def update(self, dt):
        self.pos.x -= 350 * dt
        self.rect.x = round(self.pos.x)
        
        if self.rect.right <= -50:
            self.kill()        