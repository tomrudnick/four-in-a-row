import pygame
from pygame import gfxdraw
from fourInARow import FourInARow
from colors import *
from ki import KI
from button import Button
from pygameHelper import render_text
import copy

WIDTH = 750
HEIGHT = 950

COLUMNS = 7
ROWS = 6

OFFSET_X = 0
OFFSET_Y = 250

DEPTH = 4
HUMAN_KI_DEPTH = 5

test_board = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [2, 0, 1, 1, 0, 0, 0],
              [2, 2, 1, 1, 2, 0, 0]]

def draw_board(screen, game):
    for row in range(1, ROWS + 1, 1):
        for column in range(1, COLUMNS + 1, 1):
            # calculate correct position of the game pieces
            circle_x_position = int((WIDTH - OFFSET_X) / COLUMNS * column) - 50 + OFFSET_X
            circle_y_position = int((HEIGHT - OFFSET_Y) / ROWS * row) - 50 + OFFSET_Y
            circle_color = game.playerColors[int(game.board[row - 1][column - 1])] # get the correct circle color (white, red, yellow)
            if not game.animation_finished and column == game.turn_history[-1][1] + 1 and row == game.turn_history[-1][0] + 1:

                animation_circle_y_position = OFFSET_Y + game.animation_offset_pos

                if animation_circle_y_position >= circle_y_position:
                    game.animation_finished = True

                    pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, circle_color)
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, circle_color)

                else:
                    game.animation_offset_pos += 20
                    pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, game.playerColors[0])
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, game.playerColors[0])

                    pygame.gfxdraw.aacircle(screen, circle_x_position, animation_circle_y_position, 40, circle_color)
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, animation_circle_y_position, 40, circle_color)
            #Calculated KI move to help the Human should blink
            elif game.help_human and column == game.help_move[1] + 1 and row == game.help_move[0] + 1:
                #allways draw the white circle
                pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, game.playerColors[0])
                pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, game.playerColors[0])
                # Should only blink two times
                if game.help_human_blink_counter >= 4:
                    game.help_human = False #deactivate help indicator
                    game.help_human_blink_counter = 0
                # blink in a frequece of 2 Hz
                if (t := pygame.time.get_ticks()) - game.help_human_blink_old_time > 500:
                    game.help_human_blink_old_time = t
                    game.help_human_blink_counter += 1
                    game.help_human_show_piece = not game.help_human_show_piece
                # show blinking piece
                if game.help_human_show_piece:
                    pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, game.playerColors[game.human])
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, game.playerColors[game.human])
            else:
                circle_color = game.playerColors[int(game.board[row - 1][column - 1])]
                pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, circle_color)
                pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, circle_color)

# calculate the column
def calculate_piece_position(position):
    x_pos = position[0]
    y_pos = position[1]
    if y_pos > OFFSET_Y:
        column = int((x_pos - OFFSET_X) / ((WIDTH - OFFSET_X) / COLUMNS) + 1)
        return column



def help_player(game, depth):
    print("HELP HUMAN MOVE")
    game_copy = copy.deepcopy(game)
    human_help_ki = KI(depth, game_copy, game.human)
    human_help_ki.calculate_move_multiple_processes()
    game.help_move = game_copy.turn_history[-1]
    game.help_human = True




def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS = pygame.time.Clock()


    running = True

    text_font = pygame.font.SysFont('Tahoma', 64, True, False)
    # Button text
    button_font = pygame.font.SysFont('Corbel', 35, True, False)
    button_text_quit = button_font.render('quit', True, color_white)
    button_text_reset = button_font.render('reset', True, color_white)
    button_text_back = button_font.render('undo', True, color_white)
    button_text_depth_plus = button_font.render('+', True, color_white)
    button_text_depth_minus = button_font.render('-', True, color_white)
    button_text_swap_colors = button_font.render('swap color', True, color_white)
    button_text_help = button_font.render('help', True, color_white)
    button_text_ki_toggle = button_font.render('KI Mode', True, color_white)
    button_text_human_ki_depth_plus = button_font.render('+', True, color_white)
    button_text_human_ki_depth_minus = button_font.render('-', False, color_white)
    # Game Buttons
    quitButton = Button((10, 10), (100, 50), button_text_quit, color_dark, color_light, screen, 10)
    resetButton = Button((120, 10), (100, 50), button_text_reset, color_dark, color_light, screen, 10)
    turn_back_button = Button((230, 10), (100, 50), button_text_back, color_dark, color_light, screen, 10)
    depth_minus_button = Button((340, 10), (50, 50), button_text_depth_minus, color_dark, color_light, screen, 10)
    depth_plus_button = Button((450, 10), (50, 50), button_text_depth_plus, color_dark, color_light, screen, 10)
    swap_colors_button = Button((525, 10), (170, 50), button_text_swap_colors, color_dark, color_light, screen, 10)
    help_button = Button((595, 80), (100, 50), button_text_help, color_dark, color_light, screen, 10)
    ki_toggle_button = Button((525, 150), (170, 50), button_text_ki_toggle, color_dark, color_light, screen, 10)
    human_ki_depth_minus_button = Button((525, 220), (50, 50), button_text_human_ki_depth_minus, color_dark, color_light, screen, 10)
    human_ki_depth_plus_button = Button((645, 220), (50, 50), button_text_human_ki_depth_plus, color_dark, color_light, screen, 10)
    game = FourInARow(COLUMNS, ROWS)
    game.currentPlayer = game.human
    game.lastPlayer = game.ki
    game_ended = False
    #game.board = test_board
    ki = KI(DEPTH, game, game.ki)
    ki_human = KI(HUMAN_KI_DEPTH, game, game.human)
    ki_overtake_mode = False



    while running:

        mouse_pos = pygame.mouse.get_pos()
        #if it's the turn of the KI it will make it's turn
        if game.currentPlayer == game.ki and not game_ended and game.animation_finished:
            print("KI MOVE")
            ki.calculate_move_multiple_processes()
        # if the KI "overtaken mode" is activated it will make a turn
        if game.currentPlayer == game.human and not game_ended and game.animation_finished and ki_overtake_mode:
            print("HUMAN KI MOVE")
            ki_human.calculate_move_multiple_processes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("CLOSE GAME")
                running = False
            # left mouse button clicked event
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                #Check if any button is clicked or a game piece should be placed

                #quit game
                if quitButton.pressed(mouse_pos):
                    print("Close")
                    running = False
                # resets the game
                elif resetButton.pressed(mouse_pos):
                    game.reset_game()
                    ki.game = game
                    game_ended = False

                # take back two moves
                elif turn_back_button.pressed(mouse_pos):
                    print("Undo")
                    if game_ended:
                        game_ended = False
                    game.undo()
                    game.undo()
                # lower ki depth by one
                elif depth_minus_button.pressed(mouse_pos):
                    if ki.depth > 1:
                        ki.depth -= 1
                # increase ki depth by one
                elif depth_plus_button.pressed(mouse_pos):
                    ki.depth += 1
                # swap the colors
                elif swap_colors_button.pressed(mouse_pos):
                    game.playerColors[1], game.playerColors[2] = game.playerColors[2], game.playerColors[1]
                # recieve a tip
                elif help_button.pressed(mouse_pos):
                    help_player(game, ki_human.depth)
                # activate the ki mode, the ki will play for you
                elif ki_toggle_button.pressed(mouse_pos):
                    ki_overtake_mode = not ki_overtake_mode
                # decrease human ki depth by one
                elif human_ki_depth_minus_button.pressed(mouse_pos):
                    if ki_human.depth > 1:
                        ki_human.depth -= 1
                # increase human ki depth by one
                elif human_ki_depth_plus_button.pressed(mouse_pos):
                    ki_human.depth += 1
                # place a piece
                elif not game_ended and game.currentPlayer == game.human and not ki_overtake_mode:
                    column = calculate_piece_position(mouse_pos)
                    if column is not None:
                        game.place_piece(column)

        screen.fill(BLUE)
        if game.check_win_player(game.human):
            game_ended = True
            render_text(screen, "You have beaten\nthe computer!", text_font, game.playerColors[game.human], [10, 80])
        elif game.check_win_player(game.ki):
            game_ended = True
            render_text(screen, "I am smarter\nthan you!", text_font, game.playerColors[game.ki], [10, 80])
        elif game.check_tie():
            game_ended = True
            render_text(screen, "It's a tie!", text_font, game.playerColors[game.human], [10, 80])

        elif game.currentPlayer == game.human:
            render_text(screen, "It's your turn", text_font, game.playerColors[game.human], [10, 80])
        elif game.currentPlayer == game.ki:
            render_text(screen, "I'm thinking...", text_font, game.playerColors[game.ki], [10, 80])



        draw_board(screen, game)

        quitButton.drawButton(mouse_pos)
        resetButton.drawButton(mouse_pos)
        turn_back_button.drawButton(mouse_pos)
        depth_plus_button.drawButton(mouse_pos)
        depth_minus_button.drawButton(mouse_pos)
        swap_colors_button.drawButton(mouse_pos)
        help_button.drawButton(mouse_pos)
        ki_toggle_button.drawButton(mouse_pos)
        human_ki_depth_minus_button.drawButton(mouse_pos)
        human_ki_depth_plus_button.drawButton(mouse_pos)
        render_text(screen, str(ki.depth), text_font, color_white, [400, 0])
        render_text(screen, str(ki_human.depth), text_font, color_white, [585, 205])
        pygame.display.update()
        FPS.tick(60) # Locks FPS to 60



if __name__ == "__main__":
    run_game()
