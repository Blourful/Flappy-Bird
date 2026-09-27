import pygame
import random
import os
from constants import *
#constants


# Traceback (most recent call last):
# File "game.py", line 458, in <module>
# File "game.py", line 63, in main
# File "game.py", line 345, in score
# IndexError: list index out of range


import sys
pygame.init()
SCREEN = pygame.display.set_mode((288 , 512))
pygame.display.set_caption("flipper bird")
clock = pygame.time.Clock()







##bird class


        



def main():
    best = 0
    out_score = None
    
    while True:
        #initial settings change randomly every play
        if out_score == None:
            pass
        else: 
            best = out_score
        # print(f"best{best}")
        
        AUDIOS["start"].play()
        IMAGES["bg_pic"] = IMAGES[random.choice(["day","night"])]
        color = random.choice(["red","blue","yellow"])
        pose = ["down","mid","up"]
        IMAGES["birds"] = []

        for i in pose:
            IMAGES["birds"].append(IMAGES[color + "-" + i])


        pipe = random.choice(["red-pipe","green-pipe"])
        IMAGES["pipe"] = [IMAGES[pipe],pygame.transform.flip(IMAGES[pipe],False,True)]
        


        start(IMAGES)
        result = game(IMAGES)
        if result["score"] is not None:
            if result["score"]> best:
                best = result["score"]
            # print(f"best:{best}, result{result["score"]}")
        end(IMAGES,result)
        out_score = score(IMAGES,result,best)
        

def start(images):
    pygame.mixer.music.load("assets/audio/713.mp3")
    pygame.mixer.music.play(-1)
    bird_x = W*0.2
    bird_y = (H - images["red-mid"].get_height())/2
    floor_movex = 0
    
    vel_y = 1
    bird_range = [bird_y-8,bird_y+8]
    
    repeat = 5
    frame = [1] * repeat + [0] * repeat + [2] * repeat + [1] * repeat
    bird = Bird(bird_x,bird_y,images)
    


    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
                return  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dx = images["floor"].get_width() - W
        floor_movex -= 2
        if floor_movex <= -dx:
            floor_movex = 0
        
        

        
        
        bird.update_wings()
        bird.update_motion_up_down()
        SCREEN.blit(images["bg_pic"],(0,0))
        SCREEN.blit(images["guide"],(guide_x,guide_y))
        SCREEN.blit(images["floor"],(floor_movex,floor_y))
        SCREEN.blit(bird.image, bird.rect)
        
        pygame.display.update()
        clock.tick(FPS)
    pass

def game(images):
    
    AUDIOS["flap"].play()
    bird2 = Bird(W*0.2,H*0.4,images)
    pipe1 = Pipe(W, H * 0.5,images)
    floor_movex = 0
    list_pipes = []
    list_pipes_trans = []
    distance = random.uniform(140, 300)
    n = 3
    score = 0
    for i in range(n):
        pipe_lefttop_y = H * random.uniform(0.2,0.8)
        list_pipes.append(Pipe(W + i * distance , pipe_lefttop_y ,images))
        list_pipes_trans.append(Pipe(W + i * distance , pipe_lefttop_y - 100 - 320 ,images,True))
    while True:
        flap = False
        dx = images["floor"].get_width() - W
        floor_movex -= 2
        if floor_movex <= -dx:
            floor_movex = 0
        if list_pipes[0].rect.right in(87,90 ):
            score +=1
            AUDIOS["score"].play()

        score_digits = [(digit) for digit in str(score)]
        n = len(score_digits)
        image_ls = []
        image_rect = []
        for i in range(n):
            image_ls.append(images[score_digits[i]])
            image_rect.append(image_ls[i].get_rect())
        
        
        long = (image_ls[0].get_width())* 1.5
        start_ = (W - long * n)/2
        for i in range(n):
            image_rect[i].x = start_ + long * i
            image_rect[i].y = H*0.15
        
        
        

            
        
        

        for event in pygame.event.get():
            
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flap = True
                AUDIOS["flap"].play()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        
        
        new_topleft = H * random.uniform(0.3, 0.7)
        for pipe in list_pipes:
            pipe.moving()
            if pipe.rect.right <0:
                list_pipes.remove(pipe)
                list_pipes.append(Pipe(list_pipes[-1].rect.x + 52 + distance, new_topleft,images))
        
        for pipe in list_pipes_trans:
            pipe.moving()   
            if pipe.rect.right <0:
                list_pipes_trans.remove(pipe)
                list_pipes_trans.append(Pipe(list_pipes_trans[-1].rect.x + 52 + distance, new_topleft - 320 - 100 ,images,True))

        
        results = {"bird":bird2,"pipes": (list_pipes,list_pipes_trans), "image_ls" : image_ls, "image_rect": image_rect, "score": score }    
        if bird2.rect.bottom >= floor_y-11  :
            AUDIOS["hit"].play()
            AUDIOS["die"].play()
            pygame.mixer.music.stop()
            return results
        
        for i in range(len(list_pipes)-1):
            if bird2.rect.colliderect(list_pipes[i].rect) or bird2.rect.colliderect(list_pipes_trans[i].rect):
                AUDIOS["hit"].play()
                AUDIOS["die"].play()
                pygame.mixer.music.stop()
                return results
        bird2.update_wings(flap)
        bird2.update_drop(flap)
        
        
        SCREEN.blit(images["bg_pic"],(0,0)) #background
        for pipe in list_pipes:

            SCREEN.blit(pipe.image, pipe.rect) #pipes
        
        for pipe in list_pipes_trans:

            SCREEN.blit(pipe.image, pipe.rect)
        SCREEN.blit(images["floor"],(floor_movex,floor_y)) # floor

        for i in range(len(score_digits)):
            SCREEN.blit(image_ls[i], image_rect[i])

        SCREEN.blit(bird2.image,bird2.rect) #birds
        
        pygame.display.update()
        clock.tick(FPS)

    pass

def end(images,results):
    while True:
              

        continue_image = images["continue"]
        continue_width = continue_image.get_width()
        left_x = (W - continue_width)/2
        continue_rect = continue_image.get_rect()
        continue_rect.x = left_x
        continue_rect.y = 300
        
        SCREEN.blit(images["bg_pic"],(0,0))

        for i in range(len(results["pipes"][0]) - 1):
            SCREEN.blit(results["pipes"][0][i].image,results["pipes"][0][i].rect)
            SCREEN.blit(results["pipes"][1][i].image,results["pipes"][1][i].rect)

        SCREEN.blit(images["floor"],(0,floor_y))
        SCREEN.blit(images["gameover"],(over_x,over_y))

        for i in range(len(results["image_ls"])):
            SCREEN.blit(results["image_ls"][i], results["image_rect"][i])

        SCREEN.blit(results["bird"].image,results["bird"].rect)
        results["bird"].go_die()   
        SCREEN.blit(continue_image,(left_x,300))
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 1:  # 左键点击
                    if continue_rect.collidepoint(event.pos):
                        return results 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return results 
    pass
##
def score(images, result,bestin):
    # print(f"best in score{bestin}")
    new = False  # Assuming new is initially False
    bronze = False
    silver = False
    if result["score"] == bestin:
        AUDIOS["jinse"].play()
    elif 0 <= bestin -result["score"] <= 5:
        AUDIOS["celebration"].play()
    elif bestin - result["score"] > 5:
        AUDIOS["celebration"].play()
    while True:
        score_panel_image = images["score_panel"]
        score_panel_rect = score_panel_image.get_rect()
        score_panel_rect.x = ((W - score_panel_image.get_width()) / 2)
        score_panel_rect.y = 100
        button_rect = images["button_play"].get_rect()
        button_rect.topleft = ((W - images["button_play"].get_width()) / 2, 300)

        if result["score"] == bestin:
            
            
            new = True
        elif 0 <= bestin -result["score"] <= 5:
            silver = True
        elif bestin - result["score"] > 5:
            bronze = True

        SCREEN.blit(images["bg_pic"], (0, 0))
        SCREEN.blit(score_panel_image, score_panel_rect)
        SCREEN.blit(images["button_play"], button_rect.topleft)

        if new:
            SCREEN.blit(images["medals_1"], (55, 145))
            SCREEN.blit(images["new"], (165,160))
            
        if silver:
            SCREEN.blit(images["medals_2"], (55, 145))
        if bronze:
            SCREEN.blit(images["medals_3"], (55, 145))
            
        ## outscore
        out_score_digits = [(digit) for digit in str(result["score"])]
        # print(f"out_score_digits in score{out_score_digits}")
        n = len(out_score_digits)
        image_ls = []
        image_rect = []
        for i in range(n):
            image_ls.append(pygame.transform.scale(images[out_score_digits[i]], (int(images[out_score_digits[i]].get_width() * 0.5), int(images[out_score_digits[i]].get_height() * 0.5))))

            image_rect.append(image_ls[i].get_rect())
        
        
        long = (image_ls[0].get_width())* 1.5
        start_ = ((W - 165) - long * n)/2 + 165
        for i in range(n):
            image_rect[i].x = start_ + long*i
            image_rect[i].y = 135
            SCREEN.blit(image_ls[i],image_rect[i])
        

        
        if new:
            best_digits = [(digit) for digit in str(bestin)]
            # print(f"best_digits:{best_digits}")
        else:
            best_digits = [(digit) for digit in str(bestin)]
            # print(f"best_digits:{best_digits}")
        n_best = len(best_digits)
        image_ls_best = []
        image_rect_best = []
        for i in range(n):
            image_ls_best.append(pygame.transform.scale(images[best_digits[i]], (int(images[out_score_digits[i]].get_width() * 0.5), int(images[out_score_digits[i]].get_height() * 0.5))))
            image_rect_best.append(image_ls[i].get_rect())
        
        
        long_best = (image_ls_best[0].get_width())* 1.5
        start_best = ((W - 165) - long_best * n)/2 + 165
        for i in range(n_best):
            image_rect_best[i].x = start_best + long*i
            image_rect_best[i].y = 175
            SCREEN.blit(image_ls_best[i],image_rect_best[i])
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                AUDIOS["jinse"].stop()
                AUDIOS["celebration"].stop()
                
                return bestin
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    AUDIOS["jinse"].stop()
                    AUDIOS["celebration"].stop()
                    return bestin

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    if new:
        best = result["score"]

        
        

class Bird:
    def __init__(self,x,y,input_image):
        self.index = 0
        self.repeat = 7
        self.frame = [1] * self.repeat + [0] * self.repeat + [2] * self.repeat + [1] * self.repeat
        self.IMAGES_inclass = input_image 
        self.image = self.IMAGES_inclass["birds"][self.frame[self.index]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 0.51
        self.game_vely = -6    
        self.gravity = 0.4
        self.rotate = 35
        self.ro_vel = -2.5
    
    def update_wings(self,flap = False):
        if flap:
            self.image = self.IMAGES_inclass["birds"][0]
        else:
            self.index +=1
            self.index %= len(self.frame)
            self.image = self.IMAGES_inclass["birds"][self.frame[self.index]]
        
        
        pass

    def update_motion_up_down(self):
        max = 244+8
        min = 244-8
        self.rect.y += self.vel
        if self.rect.y > max or self.rect.y < min:
            self.vel *= -1
    
    def update_drop(self,flap = False):
        if flap:
            self.rotate = 35
            self.game_vely = -6
        else:
            maxvel = 10
            maxrotate = -90

            self.game_vely = min((self.game_vely + self.gravity),maxvel)
            self.rect.y += self.game_vely

            self.rotate = max(maxrotate,self.ro_vel + self.rotate)
            
            self.image = pygame.transform.rotate(self.image,self.rotate) 

    def go_die(self):
        if self.rect.bottom < floor_y - 11:
            self.rotate = -90
            self.game_vely = 10
            self.rect.y += self.game_vely
            self.image = pygame.transform.rotate(self.image,self.rotate) 



class Pipe():
    def __init__(self,x,y,images,flip = False) -> None:
        if flip:
            self.image = images["pipe"][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.x_vel = -2
            
        else:
            self.image = images["pipe"][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.x_vel = -2

    def moving(self):
        self.rect.x += self.x_vel
        
        
        





if __name__ == "__main__":
    main()




