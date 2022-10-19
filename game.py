# PyGame template.
 
# Import standard modules.

import sys
import os
from matplotlib.pyplot import show
 
# Import non-standard modules.
import pygame
from pygame.locals import *
from button import Button
from enemy_spawner import EnemySpawner
from random import randrange
import time

pygame.init() 
pygame.display.set_caption("Welcome Day") #The window title

#Import images and define sizes
width, height = 720, 480 
WIZARD_WIDTH , WIZARD_HEIGHT = 78 , 103
LIFE_WIDTH , LIFE_HEIGHT = 21 , 22 
CARA_WIZARD_IMAGE =pygame.image.load(os.path.join('Assets','cara.png')) #character image

CARA_WIZARD=pygame.transform.scale(CARA_WIZARD_IMAGE,(WIZARD_WIDTH,WIZARD_HEIGHT)) #resize

BULLET_FIRE=pygame.image.load(os.path.join('Assets','fireball.png'))
BULLET_FIRE=pygame.transform.scale(BULLET_FIRE, (28,12))
screen = pygame.display.set_mode((width, height))
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
fireball_sfx = pygame.mixer.Sound(os.path.join('SFX','fireball.mp3'))
font = pygame.font.Font(os.path.join('Fonts', 'FreeSansBold.ttf'), 32)
textX = 10
textY = 10
score = 0


def show_score(x,y, screen):
  
  score_text = font.render("Score :" + str(score), True, (255, 255, 255))
  screen.blit(score_text,(x,y))
  pygame.display.update()



def update(wizard):
  # Go through events that are passed to the script by the window.
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type ==pygame.KEYDOWN:
          if event.key == pygame.K_SPACE  and len(bullets)<MAX_BULLET : # event to shot bullets
            bullet= pygame.Rect(wizard.x + wizard.width , wizard.y + wizard.height//2 , 10 , 5)
            bullets.append(bullet)
 
def draw(screen , wizard,bullets, enemy_spawner):
 
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
    for enemy in enemy_spawner.enemy_group:
      if bullet.colliderect(enemy):
        enemy.kill()
        score += 1
        pygame.mixer.Sound.play(fireball_sfx)
        bullets.remove(bullet)

def get_font(size): 
  return pygame.font.Font("Fonts/font.ttf", size)



def play():
  # Initialise PyGame.
  global score

  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  
  fpsClock = pygame.time.Clock()
  
  # Set up the window.

  
  enemy_spawner = EnemySpawner()

  #character
  wizard=pygame.Rect(20 ,100, WIZARD_WIDTH , WIZARD_HEIGHT )
  
  
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
      update(wizard)
        
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
            play()
      
    

def main():
  
  fps = 60.0
  fpsClock = pygame.time.Clock()
  dt = 1/fps 
  
  while True :
    fpsClock.tick(fps)
    MENU_TEXT = get_font(60).render("SAOI GAME", True, "#253B8E")
    MENU_RECT = MENU_TEXT.get_rect(center=(width/2, 180))
    screen.blit(MENU_TEXT, MENU_RECT)
    PLAY_MOUSE_POS=pygame.mouse.get_pos() # get mouse position
    PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), img_width= 220,img_height=80, pos=(width/2, height/2 + 80), 
                            text_input="START", font=get_font(30), base_color="#00b7eb", hovering_color="White")
    PLAY_BUTTON.changeColor(PLAY_MOUSE_POS)
    PLAY_BUTTON.update(screen)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit() # Opposite of pygame.init
        sys.exit() 
      if event.type == pygame.MOUSEBUTTONDOWN:
        if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
          play()
    pygame.display.update()
 


main()