import pygame
import sys
from pygame.locals import *
import random


pygame.init()

width = 400
height = 600
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("2048")

bgimg = pygame.image.load("images/bg.jpg").convert()

nums = {}
nums[2] = pygame.image.load("images/2.jpg").convert_alpha()
nums[4] = pygame.image.load("images/4.jpg").convert_alpha()
nums[8] = pygame.image.load("images/8.jpg").convert_alpha()
nums[16] = pygame.image.load("images/16.jpg").convert_alpha()
nums[32] = pygame.image.load("images/32.jpg").convert_alpha()
nums[64] = pygame.image.load("images/64.jpg").convert_alpha()
nums[128] = pygame.image.load("images/128.jpg").convert_alpha()
nums[256] = pygame.image.load("images/256.jpg").convert_alpha()
nums[512] = pygame.image.load("images/512.jpg").convert_alpha()
nums[1024] = pygame.image.load("images/1024.jpg").convert_alpha()
nums[2048] = pygame.image.load("images/2048.jpg").convert_alpha()
nums[4096] = pygame.image.load("images/4096.jpg").convert_alpha()
nums[8192] = pygame.image.load("images/8192.jpg").convert_alpha()

# button of reset
reset = pygame.image.load("images/reset.jpg").convert_alpha()
reset_rect = reset.get_rect()
reset_rect.left = 0
reset_rect.top = 100

# button of restart
restart = pygame.image.load("images/restart.jpg").convert_alpha()
restart_rect = restart.get_rect()
restart_rect.left = width - restart_rect.width
restart_rect.top = 100




class Board(object):
    def __init__(self, nums, p_sur):
        self.nums = nums
        self.p_sur = p_sur
        self.ps = []
        self.copy_ps = []
        self.base = 4
        self.len = self.base ** 2
        self.score = 0
        self.ps = [0 for x in range(self.base**2)]
        self.copy_ps = self.ps[:]
        self.moved = True


    def reset(self):
        self.ps = self.copy_ps[:]
        
    def copy(self):
        self.copy_ps = self.ps[:]
    
    def add(self):
        while self.moved:
            i = random.choice(range(self.base**2))
            if self.ps[i]:
                continue
            if i % 4:
                self.ps[i] = 2
            else:
                self.ps[i] = 4
            break

            
    def is_full(self):
        if 0 in self.ps:
            return False
        
        for i in range(self.len):
            if i % 4 != 3 and self.ps[i] == self.ps[i+1]:
                return False
            if i < 12 and self.ps[i] == self.ps[i+4]:
                return False
        return True             
            
        

    
    def move(self, direction):
        self.moved = False
        self.copy()
        
        def loop(x, next, limit):
            y = next(x)
            while limit(y):
                if self.ps[y]:
                    if self.ps[x] == 0:
                        self.ps[x] = self.ps[y]
                        self.ps[y] = 0
                        self.moved = True
                        continue
                    elif self.ps[y] == self.ps[x]:
                        self.ps[x] *= 2
                        self.score += self.ps[y]
                        self.ps[y] = 0
                        self.moved = True
                    break
                y = next(y)
        
        #up
        if direction == "UP":
            for i in range(self.len):
                loop(i, lambda x: x+4, lambda x: x < self.len)
                
        elif direction == "DOWN":
            for i in range(self.len-1, -1, -1):
                loop(i, lambda x: x - 4, lambda x: x >= 0)
                
        elif direction == "LEFT":
            for i in range(self.len):
                cont = i // 4 * 4 + 4
                loop(i, lambda x: x + 1, lambda x: x < cont)
                
        elif direction == "RIGHT":
            for i in range(self.len-1, -1, -1):
                cont = i // 4 * 4
                loop(i, lambda x: x - 1, lambda x: x >=cont)
                
                    
        
                    
    def blit(self):
        for p in range(self.len):
            
            if self.ps[p]:
                x = 5 + (p % 4) * 100
                y = 205 + (p // 4) * 100
                self.p_sur.blit(self.nums[self.ps[p]], (x, y))
        

#
board = Board(nums, screen)


font = pygame.font.SysFont("arial", 32)
font_height = font.get_linesize()

board.add()
fullen = False
while True:

    screen.blit(bgimg, (0,0))
    screen.blit(reset, (0, 100))
    screen.blit(restart, (restart_rect.left, 100 ))
    
    
    # reset and restart
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if reset_rect.left < pos[0] < reset_rect.left + 100 and \
           reset_rect.top < pos[1] < reset_rect.top + 100:
            board.reset()
            fullen = False

        if restart_rect.left < pos[0] < restart_rect.left + 100 and \
           restart_rect.top < pos[1] < restart_rect.top + 100:
            board = Board(nums, screen)
            board.add()
            fullen = False
            
    # fuilen? 
    if fullen:
        game_over = font.render("Game Over", True, (255,0,0))
        game_over_rect = game_over.get_rect()
        screen.blit(game_over, ((width  - game_over_rect.width) / 2, (height - game_over_rect.height) / 2))      
        board = Board(nums, screen)
        
    # user events
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and not fullen:
                if event.key == K_LEFT:
                    board.move("LEFT")
                if event.key == K_RIGHT:
                    board.move("RIGHT")
                if event.key == K_UP:
                    board.move("UP")
                if event.key == K_DOWN:
                    board.move("DOWN")
                
                board.add()
                fullen = board.is_full()

    
    board.blit()
    
    
    #blid score
    score_sur = font.render("Score: "+str(board.score), True, (255,0,0))
    screen.blit(score_sur, (width - score_sur.get_rect().width, 0))

    pygame.display.update()
    

