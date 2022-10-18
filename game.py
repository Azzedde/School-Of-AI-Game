# PyGame template.
 
# Import standard modules.
import sys
import os
 
# Import non-standard modules.
import pygame
from pygame.locals import *

pygame.display.set_caption("Welcome Day") #The window title

#Import images and define sizes
WIZARD_WIDTH , WIZARD_HEIGHT = 78 , 103
LIFE_WIDTH , LIFE_HEIGHT = 21 , 22 
CARA_WIZARD_IMAGE =pygame.image.load(os.path.join('Assets','cara.png')) #character image
LIFE_HEART_IMAGE=pygame.image.load(os.path.join('Assets','heart.png')) #life heart image
CARA_WIZARD=pygame.transform.scale(CARA_WIZARD_IMAGE,(WIZARD_WIDTH,WIZARD_HEIGHT)) #resize
LIFE_HEART=pygame.transform.scale(LIFE_HEART_IMAGE,(LIFE_WIDTH , LIFE_HEIGHT))

BULLET_VEL= 7
vel=5
width, height = 640, 480
MAX_BULLET = 3
bullets=[]

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
 
def draw(screen , wizard,bullets):
  """
  Draw things to the window. Called once per frame.
  """
  screen.fill((0, 0, 0)) # Fill the screen with black.
  
  # Redraw screen here.
  screen.blit(CARA_WIZARD , (wizard.x , wizard.y)) # display character
  screen.blit(LIFE_HEART, (width -120  , 20)) # display life hearts
  screen.blit(LIFE_HEART, (width -90  , 20))
  screen.blit(LIFE_HEART, (width -60  , 20))
  for bullet in bullets :
    pygame.draw.rect(screen,(255,0,0),bullet) #display bullets 
  # Flip the display so that the things we drew actually show up.
  pygame.display.flip()

# function to handle the character mouvements (Up,Down)
def handle_movement(keys_pressed, wizard):
  if keys_pressed[pygame.K_UP] and wizard.y - vel > 0: #UP
    wizard.y-=vel
  if keys_pressed[pygame.K_DOWN] and wizard.y + vel + wizard.height < height : #DOWN
    wizard.y+=vel

#function to handle the bullet mouvement
def handle_bullet(bullets, wizard):
  for bullet in bullets:
    bullet.x += BULLET_VEL
    if wizard.colliderect(bullet):
      #colidation code here 

      bullets.remove(bullet)
    elif bullet.x> width :
      bullets.remove(bullet)

#function who reduce the opacity on an image ( to add an invisibility effect)
def power_up(image):
  alpha = 120
  image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

def runPyGame():
  # Initialise PyGame.
  pygame.init()


  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  
  fpsClock = pygame.time.Clock()
  
  # Set up the window.
  screen = pygame.display.set_mode((width, height))

  #character
  wizard=pygame.Rect(20 ,100, WIZARD_WIDTH , WIZARD_HEIGHT )
  
  # screen is the surface representing the window.
  # PyGame surfaces can be thought of as screen sections that you can draw onto.
  # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
  
  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  run=True
  while run: # Loop forever!
    fpsClock.tick(fps) # You can update/draw here, I've just moved the code for neatness.
    draw(screen , wizard , bullets)

    #handeling some events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run=False
      if event.type ==pygame.KEYDOWN:
        if event.key == pygame.K_SPACE  and len(bullets)<MAX_BULLET : # event to shot bullets
          bullet= pygame.Rect(wizard.x + wizard.width , wizard.y + wizard.height//2 , 10 , 5)
          bullets.append(bullet)
          
    keys_pressed = pygame.key.get_pressed()
    handle_movement(keys_pressed, wizard)
    handle_bullet(bullets,wizard)
    


 


runPyGame()