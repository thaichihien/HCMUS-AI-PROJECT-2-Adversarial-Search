from ai_tictactoe import Cato,BoardMap
import interface as ui
import pygame
from sys import exit

WIDTH = 700
HEIGHT = 450

            
def print_result(winner):
    if winner > 0:
        avatar.send_message(screen,(65,270),4)
    elif winner < 0:
        avatar.send_message(screen,(65,270),3)
    elif winner == 0:
        avatar.send_message(screen,(65,270),5)

def click_play():
    global menu_play
    menu_play = True

def click_info():
    global menu_info
    menu_info = True

def click_back():
    global menu
    global menu_info
    menu = True
    menu_info = False

def click_prepare(size_game):
    global menu
    global menu_play
    global game_ui
    global board
    board = BoardMap(size=size_game)
    game_ui = ui.Board(size=board.size)
    menu = False
    menu_play = False
    timer.reset()

def display_info(info_list,pen):
    pygame.draw.rect(screen,'0xFFFFEB',pygame.Rect(310,25,360,360))
    pygame.draw.rect(screen,'0x7F7E8E',pygame.Rect(305,20,370,370),width=5)

    pen.render_line(info_list[0],(352,50),screen,size=12)
    pen.render_line(info_list[1],(424,88),screen,size=16)
    pen.render_line(info_list[2],(337,120),screen,size=22)
    pen.render_paragraph(info_list[3],(325,200),screen,spacing=5)
    pen.render_paragraph(info_list[4],(325,255),screen,spacing=1)
    #pen.render_paragraph(info_list[3],(320,220),screen,spacing=1)



#initilize game
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
icon = pygame.image.load('AI/Lab02-TicTacToe/data/cato_icon.png').convert_alpha()
pygame.display.set_icon(icon)
MAX_FRAME = pygame.time.Clock()
timer = ui.Timer()
bot = Cato()
board = None
game_ui = None 


#interface
menu = True
menu_play = False
menu_info= False
button_playagain = pygame.sprite.GroupSingle()
button_playagain.add(ui.Button('PLAY AGAIN',position=(50,406)))
button_back = pygame.sprite.GroupSingle()
button_back.add(ui.Button('BACK TO MENU',position=(238,406)))
button_play = pygame.sprite.GroupSingle()
button_play.add(ui.Button('PLAY',position=(432,160),font_size=30))
button_info = pygame.sprite.GroupSingle()
button_info.add(ui.Button('INFORMATION',position=(350,260),font_size=30))
button_3x3 = pygame.sprite.GroupSingle()
button_3x3.add(ui.Button('3x3',position=(430,155),font_size=33))
button_5x5 = pygame.sprite.GroupSingle()
button_5x5.add(ui.Button('5x5',position=(430,255),font_size=33))

avatar = ui.CatoAvatar((70,40),filename='AI/Lab02-TicTacToe/data/message_source.txt')
message_box = pygame.image.load('AI/Lab02-TicTacToe/data/message_box.png')
title_write = ui.Text(source='AI/Lab02-TicTacToe/data/DePixelHalbfett.ttf',size=45)
time_write = ui.Text(source='AI/Lab02-TicTacToe/data/DePixelHalbfett.ttf',size=15)
file = open('AI/Lab02-TicTacToe/data/info.txt')
info_list = file.readlines()
file.close()

#gameplay
IsFinished = False
played = 0     #for delay
time_played = 0
#playfirst = randint(0,1)


#main
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #exit game
            pygame.quit()
            exit()

    #inteface
    screen.fill("0x43434F")
    pygame.draw.rect(screen,'0xFFFFEB',pygame.Rect(55,30,190,190))
    pygame.draw.rect(screen,'0x7F7E8E',pygame.Rect(50,25,200,200),width=5)
    screen.blit(message_box,(50,240))
    

    if menu_info:
        avatar.play_animation(screen,MODE='Finished')
        avatar.send_message(screen,(65,265),7)
        display_info(info_list,time_write)

        button_back.draw(screen)
        button_back.update()
        if button_back.sprite.Event_Click():
            click_back()
    elif menu and not menu_play:
        #inteface
        avatar.play_animation(screen)
        avatar.send_message(screen,(65,265),0)
        title_write.render_line('TIC TAC TOE',(313,43),screen,color='0x7F7E8E')
        title_write.render_line('TIC TAC TOE',(310,40),screen,color='0x282735')

        button_play.draw(screen)
        button_play.update()
        if button_play.sprite.Event_Click():
            click_play()

        button_info.draw(screen)
        button_info.update()
        if button_info.sprite.Event_Click():
            click_info()
        

    elif menu and menu_play:
        #inteface
        avatar.play_animation(screen)
        avatar.send_message(screen,(65,265),6)
        title_write.render_line('TIC TAC TOE',(313,43),screen,color='0x7F7E8E')
        title_write.render_line('TIC TAC TOE',(310,40),screen,color='0x282735')

        if timer.wait(400):
            button_3x3.draw(screen)
            button_3x3.update()
            if button_3x3.sprite.Event_Click():
                click_prepare(3)

            button_5x5.draw(screen)
            button_5x5.update()
            if button_5x5.sprite.Event_Click():
                click_prepare(5)
    else:
        
        if not timer.wait(400):continue

        #inteface
        pygame.draw.rect(screen,'0xFFFFEB',pygame.Rect(465,404,190,30))
        pygame.draw.rect(screen,'0x7F7E8E',pygame.Rect(460,399,200,40),width=5)

        #if playfirst:
        #    bot.play(board)
        #    playfirst = False

        #game is finished
        if IsFinished:
            avatar.play_animation(screen,MODE='Finished')

            if winning_moves != None:           #case: there is a winner
                game_ui.winning(winning_moves)
            
            #restart game
            button_playagain.draw(screen)
            button_playagain.update()
            if button_playagain.sprite.Event_Click():
                board.clear()
                game_ui.reset()
                IsFinished = False
                played = 0
                time_played = 0

            #back to menu
            button_back.draw(screen)
            button_back.update()
            if button_back.sprite.Event_Click():
                played = 0
                board = None
                game_ui = None
                IsFinished = False
                click_back()
                timer.reset()
                time_played = 0
                continue

        else: avatar.play_animation(screen)

        #computer turn
        if played and not IsFinished:
            played += 1
            avatar.play_animation(screen,'Play')
            avatar.send_message(screen,(105,300),2)
            if played >= 5:
                time_played = pygame.time.get_ticks()
                bot.play(board)
                played = 0
                time_played = pygame.time.get_ticks() - time_played
        elif not IsFinished:
            if board.totalplay <= 0:
                avatar.play_animation(screen,'O')
            avatar.send_message(screen,(105,300),1)

        #time taken by computer to play a move
        time_write.render_line('time taken : {0} s'.format(int(time_played/1000)),(470,409),screen)

        #player turn and render board game
        if game_ui.update(screen,board) and played == 0:
            played = 1

        # check result
        result,winning_moves = bot.check_board_result(board)
        if result != 0 or not board.ismoveleft():
            IsFinished = True
            print_result(result)
    
    pygame.display.update()
    MAX_FRAME.tick(60)

    