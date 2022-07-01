
from random import randrange
import pygame
from ai_tictactoe import PLAYER,COMPUTER,EMPTY

START_POS_BOARD = (300,30)


class Board:
    def __init__(self,size) -> None:

        self.board_size = size
        self.block_size = int(360/self.board_size)
        self.board_ui = []
        #self.board_ui = [[pygame.Rect(300,30,120,120),pygame.Rect(420,30,120,120),pygame.Rect(540,30,120,120)],
        #          [pygame.Rect(300,150,120,120),pygame.Rect(420,150,120,120),pygame.Rect(540,150,120,120)],
        #          [pygame.Rect(300,270,120,120),pygame.Rect(420,270,120,120),pygame.Rect(540,270,120,120)],]
        startpos = START_POS_BOARD
        for i in range(self.board_size):
            temp = []
            for j in range(self.board_size):
                block = pygame.Rect(startpos[0] + self.block_size*j,
                            startpos[1] + self.block_size*i,self.block_size,self.block_size)
                temp.append(block)
            self.board_ui.append(temp)
        
        self.IsFinished = False
        self.wining_moves = []
        

    def click_event(self,block):
        mousepos = pygame.mouse.get_pos()
        if block.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0]:
                #print(i)
                return True
        return False
       
    def update(self,screen,board_game):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.draw_block(self.board_ui[i][j],board_game.at(i,j),screen,pos=(i,j))
                if board_game.at(i,j) == EMPTY and not self.IsFinished:
                    if self.click_event(self.board_ui[i][j]):
                        board_game.place(i,j,PLAYER)
                        #board_game[i][j] = PLAYER
                        return True

        return False

    
    def draw_block(self,block_ui,block_game,screen,pos):
        pygame.draw.rect(screen,'0xFFFFEB',block_ui)
        if self.IsFinished:
            if pos in self.wining_moves:
                pygame.draw.rect(screen,'0x66FFE3',block_ui)
        pygame.draw.rect(screen,'0xC3C2D0',block_ui,width=3)
        
        
        if block_game == COMPUTER:
            self.draw_x(screen,'0xE36856',block_ui)
        elif block_game == PLAYER:
            self.draw_o(screen,'0xCFFE70',block_ui)

    def winning(self,move_list):
        self.IsFinished = True
        self.wining_moves = move_list

    def draw_x(self,screen,color,block,width=10):
        pygame.draw.line(screen,color,(block.x+20,block.y+10),(block.x+self.block_size-20,block.y+self.block_size-10),width=width)
        pygame.draw.line(screen,color,(block.x+self.block_size-20,block.y+10),(block.x+20,block.y+self.block_size-10),width=width)

    def draw_o(self,screen,color,block,width=10):
        pygame.draw.circle(screen, color, (block.x + int(self.block_size/2),block.y + int(self.block_size/2)), int(self.block_size/3),width=width)

    def reset(self):
        self.IsFinished = False
        self.wining_moves = []


class CatoAvatar():
    def __init__(self,pos,filename) -> None:
        super().__init__()
        self.frames = [pygame.image.load("AI/Lab02-TicTacToe/data/cato_idle_01.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_idle_02.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_play_01.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_play_02.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_play_03.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_play_04.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_play_05.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_finished.png").convert_alpha(),
                  pygame.image.load("AI/Lab02-TicTacToe/data/cato_o.png").convert_alpha()]
        
        frame_list = []
        for i in range(10):
            if i == 9:frame_list.append(self.frames[1])
            else: frame_list.append(self.frames[0])

        self.animation = Animation(frame_list,framre_rate=0.03)
        self.image = self.animation.current_animation()
        self.pos = pos
        self.index = randrange(2,7)
        self.__played = True
        self.MODE_list = {'Idle' : self.animation.play,
                          'Play' : self.frames[self.index],
                          'Finished': self.frames[7],
                          'O': self.frames[8]}
        #message
        file  = open(filename)
        self.message_list = file.readlines()
        file.close()

        self.speak = Text('AI/Lab02-TicTacToe/data/DePixelKlein.ttf',size=18)

    
    def play_animation(self,screen,MODE='Idle'):
        if MODE == 'Idle':
            self.image = self.MODE_list[MODE]()
            self.__played = True
        elif MODE =='Play':
            if self.__played:
                self.index += 1
                if self.index >=7:self.index = 2
                self.image = self.frames[self.index]
                self.__played = False
        else:self.image = self.MODE_list[MODE]
        screen.blit(self.image,self.pos)

    def send_message(self,screen,pos,index):
        self.speak.render_paragraph(self.message_list[index],pos,screen)

    



class Animation:
    def __init__(self,frames : list,framre_rate = 0.1) -> None:
        self.framerate = framre_rate
        self.animation_list = frames
        self.index = 0

        #if size != 1:
        #    for i in range(0,len(frames)):
        #        self.animation_list[i] = pygame.transform.rotozoom(self.animation_list[i],0,size)

    def play(self):
        self.index += self.framerate
        if self.index >= len(self.animation_list):self.index = 0
        return self.animation_list[int(self.index)]

    def current_animation(self):
        return self.animation_list[int(self.index)]

class Text:
    def __init__(self,source=None,size=20) -> None:
        if source == None:
            self.text_font = pygame.font.SysFont('timesnewroman',  size)
        else:
            self.text_font = pygame.font.Font(source,  size)
        self.font_size = size
        self.source = source

        
    def render_paragraph(self,message,pos,screen,size=None,color='Black',spacing=10):
        message = message.split(sep = '*')

        if size != None:
            self.text_font = pygame.font.Font(self.source,  size)

        for i,line in enumerate(message):
            print_line = self.text_font.render(line,'False',color)
            screen.blit(print_line,(pos[0],pos[1]+ i*(self.font_size*2-spacing)))
        self.text_font = pygame.font.Font(self.source,  self.font_size)
    
    def render_line(self,message,pos,screen,color='Black',size=None):
        if size != None:
            self.text_font = pygame.font.Font(self.source,  size)
        print_line = self.text_font.render(message,'False',color)
        screen.blit(print_line,pos)
        self.text_font = pygame.font.Font(self.source,  self.font_size)


class Button(pygame.sprite.Sprite):
    def __init__(self,text : str,color = 'Black',position = (0,0),font_size=20) -> None:
        super().__init__()
        self.text_font = pygame.font.Font('AI/Lab02-TicTacToe/data/DePixelHalbfett.ttf', font_size)
        self.text = text
        self.color = color
        self.image = self.text_font.render(self.text,False,color)
        self.rect = self.image.get_rect(topleft = position)
        #self.click_sound = pygame.mixer.Sound('data/Sound/click.wav')
        #self.click_sound.set_volume(0.2)


    def update(self):
        self.Event_Click()
        self.Event_Hover()


    def Event_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                #self.click_sound.play()
                return True
            
        return False

    def Event_Hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.text_font.render(self.text,False,'0xFFFFEB')
        else:
             self.image = self.text_font.render(self.text,False,self.color)


class Timer:
    def __init__(self) -> None:
        self.wait_time = 0
        self.timer = pygame.time.get_ticks()
        self.setup = False
        self.finish = False

    def wait(self,time):
        if not self.setup:
            self.timer = pygame.time.get_ticks()
            self.setup = True
        now = pygame.time.get_ticks()
        if now - self.timer >= time:
            return True
        else:return False

    def reset(self):
        self.setup = False




