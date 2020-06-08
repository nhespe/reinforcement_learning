import pygame 
import time 
import math
import random
import sys
import os
import argparse

import send_message as sm

background = pygame.Surface((640, 400))
background.fill((250, 250, 250))

WIDTH, HEIGHT = 500, 400
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

IMAGE_LOCATIONS = os.path.join("utils", "flappy_bird")

def parse_args() -> argparse.Namespace:
    """ Parses Command Line Args 
        In: None
        Out: Dict Like
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="Send message at ending"
    )
    return parser.parse_args()

class Ground():
    def __init__(self):
        self.image_1 = pygame.image.load(os.path.join(IMAGE_LOCATIONS, "ground.png"))

    def draw(self):
        screen.blit(self.image_1, (0,350))

GRAVITY = .25

class Birb():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_y = 0
        self.alive = True
        self.isJump = False
        self.jumpCount = 10
        self.image_1 = pygame.image.load(os.path.join(IMAGE_LOCATIONS,"flappy1.png"))
        self.image_2 = pygame.image.load(os.path.join(IMAGE_LOCATIONS,"flappy2.png"))

    def draw(self, falling=0):
        if self.isJump:
            screen.blit(self.image_2, (self.x, self.y))
        else:
            screen.blit(self.image_1, (self.x, self.y))
        # pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))

    def fall(self):
        self.speed_y += GRAVITY
        self.y += self.speed_y

    def jump(self):
        # Check if Player is jumping and then execute the
        # jumping code.
        if self.isJump:
            if self.jumpCount >= 0:
                neg = 1
                if self.jumpCount < 0:
                    neg = 1
                self.y -= self.jumpCount**2 * 0.20 * neg
                self.jumpCount -= 1
            else:
                self.speed_y = 0
                self.isJump = False
                self.jumpCount = 10

class PipePair():
    def __init__(self, offset=0):
        offset = offset * random.choice([-1, 1]) # UP/DOWN
        self.x = 500
        self.y = 250 + offset
        self.speed = 2
        self.offset = offset
        self.image_1 = pygame.image.load(os.path.join(IMAGE_LOCATIONS,"Pipeup.png"))
        self.image_2 = pygame.image.load(os.path.join(IMAGE_LOCATIONS,"pipedown.png"))

    def draw(self):
        self.x-=self.speed
        screen.blit(self.image_1, (self.x, self.y))
        screen.blit(self.image_2, (self.x, self.y - 310))
        
        # pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x+75, self.y))
        # pygame.draw.line(screen, (255, 0, 0), (self.x, self.y-120), (self.x+75, self.y-120))

    def colission(self, birb):
        if birb.y > 350 or birb.y < -20:
            return 1

        if self.x < birb.x < (self.x + 75): # 75 is the width of the pipe - not changed with offset 
            # (birb.y > self.y)
            if (birb.y > self.y) or (birb.y < self.y-120):
                return 1
        return 0

def main(args):
    birbs = [Birb(WIDTH/2, HEIGHT/2)]
    ground = Ground()
    pipes = []
    score = 0

    while True:
        score += 1

        # make the first pipe
        if not pipes:
            pipes.append(PipePair())

        if pipes and pipes[-1].x < 300:
            pipes.append(PipePair(random.randint(25, 50)))

        if pipes and pipes[0].x < -40:
            pipes.pop(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Start to jump by setting isJump to True.
                    for birb in birbs:
                        birb.isJump = True

        for birb in birbs:
            if not birb.isJump:
                birb.fall()
            birb.jump()

        clock.tick(FPS)
        # pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0,0))

        for pipe in pipes:
            for birb in birbs:
                if pipe.colission(birb):
                   birb.alive = False
            pipe.draw()
        
        ground.draw()
        for birb in birbs:
            if birb.alive:
                birb.draw()

        if not any([birb.alive for birb in birbs]):
            break
        pygame.display.flip()
    
    print("args", args)
    if args.verbose:
        sm.publish_message(f"Local Game Ended")

if __name__ == "__main__":
    args = parse_args()
    main(args)
    
   
