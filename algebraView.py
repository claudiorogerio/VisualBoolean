"""! @brief Visualizacao de Assembler & Algebra Boole"""

# @file main.py
#
# @brief Arquivo principal de edição para Assembler e Algebra Boolean
#
# @section Description
#   O objetivo desse ambiente é de escrever algebras de Boole ou ainda códigos
#   em Assembler. A diversos atalhos que facilitam a escrita dos codigos
#
# @author Claudio Rogerio 26.11.2021
#
# @subsection TODO
#   tamanho da fonte
#   export png, pdf equacoes
#   acoes de botoes conforme dimensao da janela
#   potencia

# @subsection MAKED
#   botoes de operadores xnor, xor
#   operador tilde
#   operadores exclusivos
#   indicativo de linhas
#   botões de ações
#   DEBUG funciotions
#   Cursor direcional
#   redimensão da area de trabalho
#   acoes em Assembler
#   deletar ações em cada linha
#   controles de ações
#   linhas
#   limpar tela
#   adicionar espaco
#   barra dupla de complemento
#   pos horizontal do cursor
#   deletar a primeira linha
#   deletar a partir da 2 linha
#   deletar a ultima linha
#   deletar a partir da penultima linha
#   guardar posicoes das barras
#   barra de complemento individual ok
#   barra de complemento grupos - guarda inicio e fim da posicao e desenha ok
#   acoes barradas com '=,+,-,(,)'


## biblioteca responsavel por renderizar o jogo
import pygame
## biblioteca responsavel para gerenciar acoes externas ao cenario de jogo
import sys
import operator
import numpy as np
from buttons import *

DEBUG = False    # personal parts
DEBUG_2 = True   # print all keyboard

## Inicializacao do jogo
pygame.init()
## titulo da janela
pygame.display.set_caption( 'Assembler & Boolean View' )
icon = pygame.image.load( 'img/bt_xplus_on.png' )
pygame.display.set_icon( icon )
## variavel de controle de FPS
clock = pygame.time.Clock()

## dimensoes da janela do cenario
display = (1350,740)
# criacao do cenario
cenario = pygame.display.set_mode( display, pygame.RESIZABLE )

## fonte utilizada para informar a pontuacao
size = 40
#font = pygame.font.Font('font/monospace.medium.ttf', size)
font = pygame.font.Font('font/DejaVuSansMono.ttf', size)
font1 = pygame.font.Font('font/DejaVuSansMono.ttf', 20)     # line2 - potencia
font2 = pygame.font.Font('font/DejaVuSansMono.ttf', 12)     # help
font3 = pygame.font.Font('font/joystix monospace.ttf', 15)  # linhas fontes
color_font = (0, 0, 0)
color_font2 = (130, 130, 130)    # help
color_font3 = (150, 150, 150)    # cursor
color_font4 = (180, 180, 180)    # lines border

delete_line = False
letter = False
letter2 = False
words = []
words.append([])
words2 = []
words2.append([])
line  = ''
line2 = ''
shift = False
shift_right = False
barr_1 = False    # ativa complemento 1
barr_2 = False  # ativa complemento 2
barr_3 = False  # ativa complemento 3
barr_one = ''
barr_one_line = []
barr_one_line.append([])
barr_two = ''
barr_two_line = []
barr_two_line.append([])
barr_thr = ''
barr_thr_line = []
barr_thr_line.append([])

pot_space = ''
pot_space_off = ' '
potencia = ''
potencia_line = []
potencia_line.append([])


next_line = 55      # prox linha
pos_potencia_y = 5
pos_potencia_x = 5
pos_barr_one = 40
pos_barr_two = 45
pos_barr_thr = 50

help_on = True

def help_view():
    global display
    text  = "<H>   -> Help view ON/OFF \n"
    text += "<S>   -> Buttons view ON/OFF \n"
    text += "<K>   -> Cursor view ON/OFF \n"
    text += "<F1>   -> ON/OFF 1st complement \n"
    text += "<F2>   -> ON/OFF 2nd complement \n"
    text += "<F3>   -> ON/OFF 3th complement \n"
    text += "<F4> <F5> <F6> <F7> -> X operators \n"
    text += "<SHIFT> + < 9 >     ->  Write ( \n"
    text += "<SHIFT> + < 8 >     ->  Write * \n"
    text += "<SHIFT> + < 0 >     ->  Write ) \n"
    text += "<SHIFT> + < = >     ->  Write + \n"
    text += "< . >               ->  Write . \n"
    text += "<BACKSPACE>   ->  Delete last caract\n"
    text += "<DEL>  -> Delete all edition \n"
    text += "<HOME> -> Delete from 2th line to down \n"
    text += "<END>  -> Delete from -2th line to up \n"
    text += "<PGUP> -> Delete from 1st line to down \n"
    text += "<PGUP> -> Delete from -1st line to up \n"
    text = text.split('\n')

    pos_y_help = display[1]-300
    pos_x_help = display[0]-290
    pygame.draw.rect( cenario, (190,190,190), (pos_x_help-6, pos_y_help-4, 278, 294 ), 1)

    for t in range(len(text)):
        # para cada linha print uma posicao
        text_help = font2.render( text[t], True, color_font2 )
        cenario.blit( text_help, ( pos_x_help, pos_y_help ) )
        pos_y_help += 16


def get_barr_on_off( act_barr ):
    if act_barr: return '_'
    else: return ' '

def get_pot_on_off( potencia_on, letter, on_space, off_space ):
#    print( potencia_on )
    if potencia_on: return letter.lower()+on_space.lower()
    else: return off_space

def get_cursor_ini():
    return (40, 20)
cursor = get_cursor_ini()

def lines_view():
    aux_x, aux_y = get_cursor_ini()
    for n in range( 0, lines ):
        text_line = font3.render( str(n+1), True, color_font4 )
        cenario.blit( text_line, ( aux_x-34, aux_y+20 ) )
        aux_y += next_line
lines = 1   #total de linhas
active_lines = True
active_cursor = True
view_cursor = True      # aspecto para o cursor alternar em ligado, desligado
cursor_pos = cursor
cursor_word = ''

def cursor_view():
    global view_cursor, cursor_pos, cursor_word
    if view_cursor == True:
        cursor_word = ''
        for l in range( len(line) ):
            cursor_word += ' '
        cursor_word += '|'
        text_cursor = font.render( cursor_word, True, (210,210,210) )
    else:
        text_cursor = font.render( cursor_word, True, (255,255,255) )
    cenario.blit( text_cursor, ( cursor_pos[0]-12, cursor_pos[1]-7 ) )  # posicao de inicio da fonte
    view_cursor = ~view_cursor

idx_xor = idx_xnr = idx_and = idx_pls = idx_min = idx_pnt = idx_igu = idx_opn = idx_cls = idx_1 = idx_2 = idx_3 = 0

## start scene
while( True ):

    ## eventos do teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
        if event.type == pygame.VIDEORESIZE:
            display = event.size    #nova dimensao da janela

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit();

        pos = pygame.mouse.get_pos()        # get mouse position which change button view color
        #print( pos )
        if pos[0] > 465 and pos[0] < 530 and pos[1] > 600 and pos[1] < 660: idx_1 = 1
        else:
            if barr_1 == False: idx_1 = 0 # manter a tecla pressionada

        if pos[0] > 540 and pos[0] < 600 and pos[1] > 600 and pos[1] < 660: idx_2 = 1
        else:
            if barr_2 == False: idx_2 = 0 # manter a tecla pressionada

        if pos[0] > 610 and pos[0] < 670 and pos[1] > 600 and pos[1] < 660: idx_3 = 1
        else:
            if barr_3 == False: idx_3 = 0 # manter a tecla pressionada

        if pos[0] > 680 and pos[0] < 740 and pos[1] > 600 and pos[1] < 660: idx_and = 1
        else: idx_and = 0

        if pos[0] > 750 and pos[0] < 810 and pos[1] > 600 and pos[1] < 660: idx_pnt = 1
        else: idx_pnt = 0

        if pos[0] > 820 and pos[0] < 880 and pos[1] > 600 and pos[1] < 660: idx_xnr = 1
        else: idx_xnr = 0

        # baixo
        if pos[0] > 465 and pos[0] < 530 and pos[1] > 665 and pos[1] < 720: idx_opn = 1
        else: idx_opn = 0

        if pos[0] > 540 and pos[0] < 600 and pos[1] > 665 and pos[1] < 720: idx_cls = 1
        else: idx_cls = 0

        if pos[0] > 610 and pos[0] < 670 and pos[1] > 665 and pos[1] < 720: idx_igu = 1
        else: idx_igu = 0

        if pos[0] > 680 and pos[0] < 740 and pos[1] > 665 and pos[1] < 720: idx_pls = 1
        else: idx_pls = 0

        if pos[0] > 750 and pos[0] < 810 and pos[1] > 665 and pos[1] < 720: idx_min = 1
        else: idx_min = 0

        if pos[0] > 820 and pos[0] < 880 and pos[1] > 665 and pos[1] < 720: idx_xor = 1
        else: idx_xor = 0

        ## mouse event
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #print( 'Mouse pos:', pos )
            if active_buttons == True:
                if pos[0] > 465 and pos[0] < 530 and pos[1] > 600 and pos[1] < 660:
                    barr_1 = operator.not_( barr_1 )
                    idx_1 = int( barr_1 )
                    if DEBUG: print('Barr 1 ON')

                if pos[0] > 540 and pos[0] < 600 and pos[1] > 600 and pos[1] < 660:
                    barr_2 = operator.not_( barr_2 )
                    idx_2 = int( barr_2 )
                    if DEBUG: print('Barr 2 ON')

                if pos[0] > 610 and pos[0] < 670 and pos[1] > 600 and pos[1] < 660:
                    barr_3 = operator.not_( barr_3 )
                    idx_3 = int( barr_3 )
                    if DEBUG: print( 'Barr 3 ON' )

                if idx_xor == 1:
                    letter = '\u2295'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_xnr == 1:
                    letter = '\u2299'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_and == 1:
                    letter = '&'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_pnt == 1:
                    letter = '.'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_pls == 1:
                    letter = '+'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_igu == 1:
                    letter = '='
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_min == 1:
                    letter = '-'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

                if idx_opn == 1:
                    letter = '('
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False
                if idx_cls == 1:
                    letter = ')'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )
                    shift = False

        ## acoes do teclado
        if event.type ==pygame.KEYUP:
            #if event.key == pygame.K_DOWN:
            #    if DEBUG: print('Levanta-se!')

            if event.key == pygame.K_RSHIFT:
                if DEBUG: print( 'shift right' )
                shift_right = True
                letter = ''

            if event.key == pygame.K_LSHIFT:
                if DEBUG: print( 'shift' )
                shift = True
                letter = ''

            if event.key == pygame.K_QUOTE:
                if shift == True:
                    barr_2 = operator.not_(barr_2)
                    idx_2 = int( barr_2 )
                    shift = False
                else:
                    barr_1 = operator.not_(barr_1)
                    idx_1 = int( barr_1 )
                if DEBUG: print( '1', barr_1, idx_1, '  2', barr_2, idx_2 )

            if event.unicode == '~':
                if shift:
                    letter = '^'
                    shift = False
                else:
                    letter = '~'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_F1:
                if DEBUG: print( 'Barra one' )
                barr_1 = operator.not_(barr_1)
                idx_1 = int( barr_1 )

            if event.key == pygame.K_F2:
                if DEBUG: print( 'Barra two' )
                barr_2 = operator.not_(barr_2)
                idx_2 = int( barr_2 )

            if event.key == pygame.K_F3:
                if DEBUG: print( 'Barra three' )
                barr_3 = operator.not_( barr_3 )
                idx_3 = int( barr_3 )

            if event.key == pygame.K_F4:
                letter = '\u2295'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_F5:
                letter = '\u2299'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_F6:
                letter = '\u2296'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_F7:
                letter = '\u2297'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_BACKSLASH:
                if shift:
                    letter = '|'
                    shift = False
                else:
                    letter = '\\'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_k:     # ativa/desativa cursor
                active_cursor = ~active_cursor

            if event.key == pygame.K_s:     # ativa/desativa botoes
                active_buttons = ~active_buttons

            if event.key == pygame.K_h:     # imprime help desk
                help_on = ~help_on
            if event.key == pygame.K_l:     # ativa/desativa lines border
                active_lines = ~active_lines

            if event.key == pygame.K_a:
                letter = 'A'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
                potencia += get_pot_on_off( shift_right, letter, pot_space, pot_space_off )
                if shift_right: letter = False
                shift_right = False
#                if shift_right == True:
 #                   letter2 = letter.lower()
  #                  print( letter2 , 'kkk')
#                    pos



            if event.key == pygame.K_b:
                letter = 'B'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
                potencia += get_pot_on_off( shift_right, letter, pot_space, pot_space_off )
                shift_right = False

            if event.key == pygame.K_c:
                letter = 'C'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_d:
                letter = 'D'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_e:
                if shift:
                    letter = '∈' #∉
                    shift = False
                else:
                    letter = 'E'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_f:
                letter = 'F'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_x:
                if shift:
                    letter = 'X'
                    shift = False
                else:
                    letter = 'x' #\u2681
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_n:
                if shift:
                    letter = 'ℕ'
                    shift = False
                else:
                    letter = 'n'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_p:
                if shift:
                    letter = 'ℙ'
                    shift = False
                else:
                    letter = 'p'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_o:
                if shift:
                    letter = 'O'
                    shift = False
                else:
                    letter = 'o'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_z:
                if shift:
                    letter = 'ℤ'
                    shift = False
                else:
                    letter = 'z'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_q:
                if shift:
                    letter = 'ℚ'
                    shift = False
                else:
                    letter = 'q'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_i:
                if shift:
                    letter = 'I'
                    shift = False
                else:
                    letter = 'i'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
                potencia += get_pot_on_off( shift_right, letter, pot_space, pot_space_off )
                shift_right = False

            if event.key == pygame.K_r:
                if shift:
                    letter = 'ℝ'
                    shift = False
                else:
                    letter = 'r'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
            if event.key == pygame.K_u:
                if shift:
                    letter = '\u2229'
                    shift = False
                else:
                    letter = '\u222A'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_COMMA:
                if shift:
                    letter = '<'
                    shift = False
                else:
                    letter = ','
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False


            if event.key == pygame.K_SPACE:
                if DEBUG: print( 'espacos' )
                letter = ' '
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False
                potencia += get_pot_on_off( shift_right, letter, pot_space, pot_space_off )
                shift_right = False

            if event.key == pygame.K_9:
                if shift:
                    letter = '('
                    shift = False
                else:
                    letter = '9'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_0:
                if shift:
                    letter = ')'
                    shift = False
                else: letter = '0'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_1:
                if shift == True :
                    letter = '!'
                    shift = False
                else:
                    letter = '1'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_2:
                if shift == True :
                    letter = '@'
                    shift = False
                else:
                    letter = '2'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_3:
                if shift == True :
                    letter = '#'
                    shift = False
                else:
                    letter = '3'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_4:
                if shift == True :
                    letter = '$'
                    shift = False
                else:
                    letter = '4'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_5:
                letter = '5'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_6:
                if shift == True:
                    barr_3 = operator.not_( barr_3 )
                    idx_3 = int( barr_3 )
                    shift = False
                else:
                    letter = '6'
                    barr_one += get_barr_on_off( barr_1 )
                    barr_two += get_barr_on_off( barr_2 )
                    barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_7:
                if shift == True :
                    letter = '&'
                    shift = False
                else:
                    letter = '7'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_8:
                if shift == True :
                    letter = '*'
                    shift = False
                else: letter = '8'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_LEFTBRACKET:
                if shift == True :
                    letter = '{'
                    shift = False
                else: letter = '['
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_RIGHTBRACKET:
                if shift == True :
                    letter = '}'
                    shift = False
                else: letter = ']'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_EQUALS:
                if shift == True :
                    letter = '+'
                    shift = False
                else:
                    letter = '='
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_MINUS:
                if shift == True :
                    letter = '_'
                    shift = False
                else:
                    letter = '-'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )

            if event.key == pygame.K_PERIOD:
                if shift:
                    letter = '>'
                    shift = False
                else:
                    letter = '.'
                barr_one += get_barr_on_off( barr_1 )
                barr_two += get_barr_on_off( barr_2 )
                barr_thr += get_barr_on_off( barr_3 )
                shift = False

            if event.key == pygame.K_DELETE:
                lines = 1
                cursor = get_cursor_ini()
                line = ''
                words = []
                words.append([])
                barr_one = ''
                barr_one_line = []
                barr_one_line.append([])
                barr_two = ''
                barr_two_line = []
                barr_two_line.append([])
                barr_thr = ''
                barr_thr_line = []
                barr_thr_line.append([])
                shift = False

            # deleta ultima edicao
            if event.key == pygame.K_BACKSPACE:
                #barr_1= True # so isso
                line = line[:-1]
                barr_one = barr_one[:-1]
                barr_two = barr_two[:-1]
                barr_thr = barr_thr[:-1]

            if event.key == pygame.K_PAGEUP:
                if DEBUG: print( 'delete linhas superiores' )
                delete_line = 'up'
                lines -= 1
                if lines <= 0 : lines = 1

            if event.key == pygame.K_PAGEDOWN:
                if DEBUG: print( 'delete linhas inferiores' )
                delete_line = 'down'
                lines -= 1
                if lines <= 0 : lines = 1

            if event.key == pygame.K_HOME:
                if DEBUG: print( 'delete linhas inferiores menos a primeira' )
                delete_line = 'home'
                lines -= 1
                if lines <= 0 : lines = 1

            if event.key == pygame.K_END:
                if DEBUG: print( 'delete linhas inferiores menos a primeira' )
                delete_line = 'end'
                lines -= 1
                if lines <= 0 : lines = 1

            if event.key == pygame.K_RETURN:
                cursor = ( cursor[0], cursor[1]+ next_line )
                cursor_pos = cursor
                if DEBUG: print( 'enter', line, cursor[0], cursor[1] )
                letter = ''
                words[-1].append( line )
                words.append([]) # prox linha ativa
                line = ''
#                letter2 = ''
 #               words2[-1].append( line2 )
  #              words2.append([]) # prox linha ativa
   #             line2 = ''
                potencia_line[-1].append( potencia )
                potencia_line.append([])
                potencia = ''
                barr_one_line[-1].append( barr_one )
                barr_one_line.append([])
                barr_one = ''
                barr_two_line[-1].append( barr_two )
                barr_two_line.append([])
                barr_two = ''
                barr_thr_line[-1].append( barr_thr )
                barr_thr_line.append([])
                barr_thr = ''
                lines += 1

            ## visualizar teclas pressionadas
            if DEBUG_2: print(pygame.key.name(event.key), event.unicode)

    # cor de fundo
    cenario.fill( (255,255,255) )

    if letter != False :
        line += letter
        letter = False

    if letter2 != False :
        line2 += letter2
        letter2 = False


    if delete_line == 'up':
        words = words[1:-1]
        words.append([])
        letter = ''
        barr_one_line = barr_one_line[1:-1]
        barr_one_line.append([])
        barr_one = ''
        barr_two_line = barr_two_line[1:-1]
        barr_two_line.append([])
        barr_two = ''
        barr_thr_line = barr_thr_line[1:-1]
        barr_thr_line.append([])
        barr_thr = ''
        cursor = ( cursor[0], cursor[1]-next_line )

        delete_line = False

    if delete_line == 'down':
        words = words[:-2]
        words.append([])
        letter = ''
        barr_one_line = barr_one_line[:-2]
        barr_one_line.append([])
        barr_one = ''
        barr_two_line = barr_two_line[:-2]
        barr_two_line.append([])
        barr_two = ''
        barr_thr_line = barr_thr_line[:-2]
        barr_thr_line.append([])
        barr_thr = ''
        cursor = ( cursor[0], cursor[1]-next_line )
        delete_line = False

    if delete_line == 'home':
        words = words[:1] + words[2:-1]
        words.append([])
        letter = ''
        barr_one_line = barr_one_line[:1] + barr_one_line[2:-1]
        barr_one_line.append([])
        barr_one = ''
        barr_two_line = barr_two_line[:1] + barr_two_line[2:-1]
        barr_two_line.append([])
        barr_two = ''
        barr_thr_line = barr_thr_line[:-2]
        barr_thr_line.append([])
        barr_thr = ''
        cursor = ( cursor[0], cursor[1]-next_line )
        delete_line = False

    if delete_line == 'end':
        words = words[:-1]
        words = words[:-2] + words[-1:]
        words.append([])
        letter = ''
        barr_one_line = barr_one_line[:-1]
        barr_one_line = barr_one_line[:-2] + barr_one_line[-1:]
        barr_one_line.append([])
        barr_one = ''
        barr_two_line = barr_two_line[:-1]
        barr_two_line = barr_two_line[:-2] + barr_two_line[-1:]
        barr_two_line.append( [] )
        barr_two = ''
        barr_thr_line = barr_thr_line[:-1]
        barr_thr_line = barr_thr_line[:-2] + barr_thr_line[-1:]
        barr_thr_line.append([])
        barr_thr = ''
        cursor = ( cursor[0], cursor[1]-next_line )
        delete_line = False

    pos_y = get_cursor_ini()[1] # pos_y inicial escrita do algoritmo
    for p in words:
        if DEBUG: print( 'Palavra', p, len(words) )
        pp = ''
        for aux in p: pp += aux

        text = font.render( pp, True, color_font )
        cenario.blit( text, ( cursor[0], pos_y ) )
        pos_y += next_line

    text = font.render( line, True, color_font )
    cenario.blit( text, cursor )
    if DEBUG: print( 'Nova', line )

    pos_y = get_cursor_ini()[1]     # pos_y inicial complemento 1
    for bl in barr_one_line:
        if DEBUG: print( 'Barra 1', bl, len(barr_one_line) )
        barra = ''
        for aux in bl: barra += aux
        if DEBUG: print( 'Imprime:', barra )
        text = font.render( barra, True, color_font )
        cenario.blit( text, ( cursor[0], pos_y - pos_barr_one ) )
        pos_y += next_line

    text_1 = font.render( barr_one, True, color_font )
    cenario.blit( text_1, ( cursor[0], cursor[1] - pos_barr_one) )

    pos_y = get_cursor_ini()[1]     # pos_y inicial
    for bl in barr_two_line:
        if DEBUG: print( 'Barra 2', bl, len(barr_two_line) )
        barra = ''
        for aux in bl: barra += aux
        if DEBUG: print( 'Imprime_2:', barra )

        text = font.render( barra, True, color_font )
        cenario.blit( text, ( cursor[0], pos_y - pos_barr_two ) )
        pos_y += next_line

    text_2 = font.render( barr_two, True, color_font )
    cenario.blit( text_2, ( cursor[0], cursor[1] - pos_barr_two ) )

    pos_y = get_cursor_ini()[1]     # pos_y inicial
    for bl in barr_thr_line:
        if DEBUG: print( 'Barra 3', bl, len(barr_thr_line) )
        barra = ''
        for aux in bl: barra += aux
        if DEBUG: print( 'Imprime_3:', barra )

        text = font.render( barra, True, color_font )
        cenario.blit( text, ( cursor[0], pos_y - pos_barr_thr ) )
        pos_y += next_line

    text_3 = font.render( barr_thr, True, color_font )
    cenario.blit( text_3, ( cursor[0], cursor[1] - pos_barr_thr ) )

    text_4 = font1.render( potencia, True, color_font )
    cenario.blit( text_4, ( cursor[0] + pos_potencia_x, cursor[1] - pos_potencia_y ) )
    print( 'potencia', potencia )

    # help
    if help_on == True :
        help_view()

    if active_cursor == True:
        cursor_pos = cursor
        cursor_view()

    if active_buttons == True:
        #buttons_view( cenario, display, idx_and, idx_plus, idx_2, idx_1_up, idx_1_down )
        buttons_view( cenario, display, idx_xor, idx_xnr, idx_and, idx_pls, idx_min, idx_pnt, idx_igu, idx_opn, idx_cls, idx_1, idx_2, idx_3 )

    if active_lines == True:
        lines_view()

    pygame.display.update()
    clock.tick( 10 )
