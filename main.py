import pygame
from pygame import gfxdraw
from fourInARow import FourInARow
from colors import *
from ki import KI
from button import Button
from pygameHelper import render_text

WIDTH = 750
HEIGHT = 950

COLUMNS = 7
ROWS = 6

OFFSET_X = 0
OFFSET_Y = 250

DEPTH = 5

test_board = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [2, 0, 1, 1, 0, 0, 0],
              [2, 2, 1, 1, 2, 0, 0]]

def draw_board(screen, game, offset_x=0, offset_y=0):
    for row in range(1, ROWS + 1, 1):
        for column in range(1, COLUMNS + 1, 1):
            circle_x_position = int((WIDTH - offset_x) / COLUMNS * column) - 50 + offset_x
            circle_y_position = int((HEIGHT - offset_y) / ROWS * row) - 50 + offset_y
            if not game.animation_finished and column == game.turn_history[-1][1] + 1 and row == game.turn_history[-1][0] + 1:
                animation_circle_y_position = offset_y + game.animation_offset_pos
                if animation_circle_y_position >= circle_y_position:
                    game.animation_finished = True
                    circle_color = game.playerColors[int(game.board[row - 1][column - 1])]
                    # pygame.draw.circle(screen, circle_color, (circle_x_position, circle_y_position), 40, 0)
                    pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, circle_color)
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, circle_color)

                else:
                    game.animation_offset_pos += 6
                    pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, game.playerColors[0])
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, game.playerColors[0])
                    circle_color = game.playerColors[int(game.board[row - 1][column - 1])]
                    pygame.gfxdraw.aacircle(screen, circle_x_position, animation_circle_y_position, 40, circle_color)
                    pygame.gfxdraw.filled_circle(screen, circle_x_position, animation_circle_y_position, 40, circle_color)

            else:
                circle_color = game.playerColors[int(game.board[row - 1][column - 1])]
                #pygame.draw.circle(screen, circle_color, (circle_x_position, circle_y_position), 40, 0)
                pygame.gfxdraw.aacircle(screen, circle_x_position, circle_y_position, 40, circle_color)
                pygame.gfxdraw.filled_circle(screen, circle_x_position, circle_y_position, 40, circle_color)

def get_piece_position(position, game, offset_x=0, offset_y=0):
    x_pos = position[0]
    y_pos = position[1]
    if y_pos > offset_y:
        column = int((x_pos - offset_x) / ((WIDTH - offset_x) / COLUMNS) + 1)
        return game.place_piece(column)
    else:
        return False


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS = pygame.time.Clock()
    FPS.tick(60)

    running = True
    text_font = pygame.font.SysFont('Tahoma', 64, True, False)
    button_font = pygame.font.SysFont('Corbel', 35, True, False)
    button_text_quit = button_font.render('quit', True, color_white)
    button_text_reset = button_font.render('reset', True, color_white)
    button_text_back = button_font.render('undo', True, color_white)
    button_text_depth_plus = button_font.render('+', True, color_white)
    button_text_depth_minus = button_font.render('-', True, color_white)
    button_text_swap_colors = button_font.render('swap color', True, color_white)
    game = FourInARow(COLUMNS, ROWS)
    game.currentPlayer = game.human
    game.lastPlayer = game.ki
    game_ended = False
    #game.board = test_board
    ki = KI(DEPTH, game)
    quitButton = Button((10, 10), (100, 50), button_text_quit, color_dark, color_light, screen, 10)
    resetButton = Button((120, 10), (100, 50), button_text_reset, color_dark, color_light, screen, 10)
    turn_back_button = Button((230, 10), (100, 50), button_text_back, color_dark, color_light, screen, 10)
    depth_minus_button = Button((340, 10), (50, 50), button_text_depth_minus, color_dark, color_light, screen, 10)
    depth_plus_button = Button((450, 10), (50, 50), button_text_depth_plus, color_dark, color_light, screen, 10)
    swap_colors_button = Button((525, 10), (170,50), button_text_swap_colors, color_dark, color_light, screen, 10)


    allow_ki_move = False

    while running:

        mouse_pos = pygame.mouse.get_pos()
        if game.currentPlayer == game.ki and not game_ended and game.animation_finished:
            print("KI move?")
            ki.calculate_move_multiple_processes()
            allow_ki_move = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("CLOSE GAME")
                running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if quitButton.pressed(mouse_pos):
                    print("Close")
                    running = False
                elif resetButton.pressed(mouse_pos):
                    game.reset_game()
                    ki.game = game
                    game_ended = False
                elif turn_back_button.pressed(mouse_pos):
                    print("Undo")
                    if game_ended:
                        game_ended = False
                    game.undo()
                    game.undo()
                elif depth_minus_button.pressed(mouse_pos):
                    if ki.depth > 1:
                        ki.depth -= 1
                elif depth_plus_button.pressed(mouse_pos):
                    ki.depth += 1
                elif swap_colors_button.pressed(mouse_pos):
                    game.playerColors[1], game.playerColors[2] = game.playerColors[2], game.playerColors[1]
                elif not game_ended and game.currentPlayer == game.human:
                    get_piece_position(mouse_pos, game, OFFSET_X, OFFSET_Y)
                    game.check_win_fast()
                # print(game.board)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("RESET GAME")
                    game_ended = False
                    game.reset_game()
                    ki.depth = DEPTH
                    ki.game = game

        screen.fill(BLUE)
        if game.animation_finished:
            if game.check_win_player(game.human):
                game_ended = True
                render_text(screen, "You have beaten\nthe computer!", text_font, game.playerColors[game.human], [10, 80])
            elif game.check_win_player(game.ki):
                game_ended = True
                render_text(screen, "I am smarter\nthan you!", text_font, game.playerColors[game.ki], [10, 80])
            elif game.check_tie():
                game_ended = True
                render_text(screen, "It's a tie!", text_font, game.playerColors[game.human], [10, 80])


        if game.currentPlayer == game.human:
            render_text(screen, "It's your turn", text_font, game.playerColors[game.human], [10, 80])
        if game.currentPlayer == game.ki:
            render_text(screen, "I'm thinking...", text_font, game.playerColors[game.ki], [10, 80])



        draw_board(screen, game, OFFSET_X, OFFSET_Y)
        quitButton.drawButton(mouse_pos)
        resetButton.drawButton(mouse_pos)
        turn_back_button.drawButton(mouse_pos)
        depth_plus_button.drawButton(mouse_pos)
        depth_minus_button.drawButton(mouse_pos)
        swap_colors_button.drawButton(mouse_pos)
        render_text(screen, str(ki.depth), text_font, color_white, [400, 0])
        pygame.display.update()


if __name__ == "__main__":
    run_game()
