# PyGame template.
 
# Import standard modules.

import sys
import os
from matplotlib.pyplot import show
 
# Import non-standard modules.
import pygame
from pygame.locals import *
from enemy_spawner import EnemySpawner
from random import randrange
import time

pygame.display.set_caption("Welcome Day") #The window title

#Import images and define sizes
WIZARD_WIDTH , WIZARD_HEIGHT = 78 , 103
LIFE_WIDTH , LIFE_HEIGHT = 21 , 22 
CARA_WIZARD_IMAGE =pygame.image.load(os.path.join('Assets','cara.png')) #character image

CARA_WIZARD=pygame.transform.scale(CARA_WIZARD_IMAGE,(WIZARD_WIDTH,WIZARD_HEIGHT)) #resize

BULLET_FIRE=pygame.image.load(os.path.join('Assets','fireball.png'))
BULLET_FIRE=pygame.transform.scale(BULLET_FIRE, (28,12))
BULLET_VEL= 7
vel=5
width, height = 720, 480 
MAX_BULLET = 3
bullets=[]
background=pygame.image.load(os.path.join('Assets','sky.jpg')) #background image
background=pygame.transform.scale(background, (width,height))
gameover=pygame.image.load(os.path.join('Assets','gameover.jpg'))
gameover=pygame.transform.scale(gameover, (width, height))
pygame.font.init()
pygame.mixer.init()
fireball_sfx = pygame.mixer.music.load(os.path.join('SFX','fireball.mp3'))
font = pygame.font.Font(os.path.join('Fonts', 'FreeSansBold.ttf'), 32)
textX = 10
textY = 10
score = 0
def show_score(x,y, screen):
  
  score_text = font.render("Score :" + str(score), True, (255, 255, 255))
  screen.blit(score_text,(x,y))
  pygame.display.update()
def update(dt):
  """
  Update game. Called once per frame.
  dt is the amount of time passed since last frame.
  If you want to have constant apparent movement no matter your framerate,
  what you can do is something like
  
  x += v * dt
  
  and this will scale your velocity based on time. Extend as necessary."""
  
  # Go through events that are passed to the script by the window.
  for event in pygame.event.get():
    # We need to handle these events. Initially the only one you'll want to care
    # about is the QUIT event, because if you don't handle it, your game will crash
    # whenever someone tries to exit.
    if event.type == QUIT:
      pygame.quit() # Opposite of pygame.init
      sys.exit() # Not including this line crashes the script on Windows. Possibly
      # on other operating systems too, but I don't know for sure.
    # Handle other events as you wish.  
 
def draw(screen , wizard,bullets, enemy_spawner):
  """
  Draw things to the window. Called once per frame.
  """
  screen.fill((0, 0, 0)) # Fill the screen with black.
  screen.blit(background,(0,0))
  # Redraw screen here.
  screen.blit(CARA_WIZARD , (wizard.x , wizard.y)) # display character

  enemy_spawner.enemy_group.draw(screen)
  for bullet in bullets :
    screen.blit(BULLET_FIRE, bullet ) #display bullets 
  
  # Flip the display so that the things we drew actually show up.
  pygame.display.flip()

# function to handle the character mouvements (Up,Down)
def handle_movement(keys_pressed, wizard):
  if keys_pressed[pygame.K_UP] and wizard.y - vel > 0: #UP
    wizard.y-=vel
  if keys_pressed[pygame.K_DOWN] and wizard.y + vel + wizard.height < height : #DOWN
    wizard.y+=vel

#function to handle the bullet mouvement
def handle_bullet(bullets, wizard, enemy_spawner):
  
  for bullet in bullets:
    bullet.x += BULLET_VEL
    if wizard.colliderect(bullet):
      

      bullets.remove(bullet)
    elif bullet.x> width :
      bullets.remove(bullet)
      global score 
      score += 1
      print(score)
    for enemy in enemy_spawner.enemy_group:
      if bullet.colliderect(enemy):
        enemy.kill()
        score += 1
        pygame.mixer.Sound.play(fireball_sfx)
        bullets.remove(bullet)




def runPyGame():
  # Initialise PyGame.
  pygame.init()
  global score

  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  
  fpsClock = pygame.time.Clock()
  
  # Set up the window.
  screen = pygame.display.set_mode((width, height))
  
  enemy_spawner = EnemySpawner()

  #character
  wizard=pygame.Rect(20 ,100, WIZARD_WIDTH , WIZARD_HEIGHT )
  
  # screen is the surface representing the window.
  # PyGame surfaces can be thought of as screen sections that you can draw onto.
  # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
  
  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  run=True
  game_over = False
  while run: # Loop forever!

    fpsClock.tick(fps) # You can update/draw here, I've just moved the code for neatness.
    
    if game_over == False:
      draw(screen , wizard , bullets, enemy_spawner)
      
      
      enemy_spawner.update()
      
      #handeling some events
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type ==pygame.KEYDOWN:
          if event.key == pygame.K_SPACE  and len(bullets)<MAX_BULLET : # event to shot bullets
            bullet= pygame.Rect(wizard.x + wizard.width , wizard.y + wizard.height//2 , 10 , 5)
            bullets.append(bullet)
        
      for enemy in enemy_spawner.enemy_group:
        if wizard.colliderect(enemy):
          
          game_over = True

      
      
      keys_pressed = pygame.key.get_pressed()
      show_score(560,40, screen)
      handle_movement(keys_pressed, wizard)
      handle_bullet(bullets,wizard, enemy_spawner)
    else:
      screen.blit(gameover,(0,0))
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            score=0
            runPyGame()
      
    


 


runPyGame()