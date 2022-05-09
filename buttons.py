"""! @brief Imagens dos botoes"""

# @file buttons.py
#
# @brief Arquivo de importacao dos botoes para o cenario principal
#
# @section Descrição
# O arquivo é responsável pela importacao das imagens utilizadas como botoes
#
# @author Claudio Rogerio 30.11.2021
#
# @subsection TODO
#   -
#
# @subsection MAKED
#   -

import pygame

# funcao que importa com redimensionamento
# import_img( './img/bt_3_', 0.25, 'ONOFF' )
def import_img( file, percent, type ):
    if type == 'ONOFF':   # on off
        aux_f = file+'on.png'
        print( 'Load', aux_f )
        img_on = pygame.image.load( aux_f )
        img_on = pygame.transform.rotozoom( img_on, 0, percent )

        aux_f = file+'off.png'
        img_of = pygame.image.load( aux_f )
        img_of = pygame.transform.rotozoom( img_of, 0, percent )
        return [img_of, img_on]
    else: return 0

porc = 0.15
bt_and = import_img( './img/bt_and_', porc, 'ONOFF' )
bt_pls = import_img( './img/bt_plus_', porc, 'ONOFF' )
bt_min = import_img( './img/bt_min_', porc, 'ONOFF' )
bt_pnt = import_img( './img/bt_point_', porc, 'ONOFF' )
bt_igu = import_img( './img/bt_igu_', porc, 'ONOFF' )
bt_opn = import_img( './img/bt_open_', porc, 'ONOFF' )
bt_cls = import_img( './img/bt_close_', porc, 'ONOFF' )
bt_xor = import_img( './img/bt_xplus_', porc, 'ONOFF' )  #xor
bt_xnr = import_img( './img/bt_xpoint_', porc, 'ONOFF' ) #xnor
bt_1 = import_img( './img/bt_1_', porc, 'ONOFF' )
bt_2 = import_img( './img/bt_2_', porc, 'ONOFF' )
bt_3 = import_img( './img/bt_3_', porc, 'ONOFF' )


active_buttons = True
def buttons_view( cenario, display, idx_xor, idx_xnr, idx_and, idx_pls, idx_min, idx_pnt, idx_igu, idx_opn, idx_cls, idx_1, idx_2, idx_3 ):
    pos_x = int(display[0]/2) - 205
    pos_y = display[1]-140
    incrm = 70
    cenario.blit( bt_1[ idx_1 ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_2[ idx_2 ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_3[ idx_3 ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_and[ idx_and ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_pnt[ idx_pnt ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_xnr[ idx_xnr ], ( (pos_x, pos_y) ) )

    pos_x = int(display[0]/2) - 205
    pos_y += 65
    cenario.blit( bt_opn[ idx_opn ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_cls[ idx_cls ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_igu[ idx_igu ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_pls[ idx_pls ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_min[ idx_min ], ( (pos_x, pos_y) ) )
    pos_x += incrm
    cenario.blit( bt_xor[ idx_xor ], ( (pos_x, pos_y) ) )
