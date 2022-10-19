import pygame
import os
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(os.path.join('Assets','enemy.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (52,52))
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = random.randrange(5,420)
        self.speed_x = random.randrange(18,24)
        self.speed_y = 0

    def update(self):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y

    def get_hit(self):
        self.kill()