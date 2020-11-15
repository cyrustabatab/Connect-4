import pygame
import random


def rabin_karp(s1,s2):
    assert len(s1) >= len(s2)

    current_hash = target_hash = 0
    same = True
    x = 53

    for i in range(len(s2)):
        if same and s1[i] != s2[i]:
            same = False

        current_hash = current_hash * x + ord(s1[i])
        target_hash = target_hash * x + ord(s2[i])

    if same:
        return 0



    
pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 700,800
BOARD_WIDTH,BOARD_HEIGHT = 700,600

FPS = 30
SQUARE_LENGTH = 100
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

rows,cols = 6,7
board = [[None for _ in range(cols)] for _ in range(rows)]


clock = pygame.time.Clock()

def draw_board(x=None,y=None):
    
    offset = 100
    

    for row in range(rows):
        for col in range(cols):
            
            pygame.draw.rect(screen,(0,0,255),(col * SQUARE_LENGTH,offset + row * SQUARE_LENGTH,SQUARE_LENGTH,SQUARE_LENGTH))


            if board[row][col] is None:
                pygame.draw.circle(screen,(255,255,255),(col * SQUARE_LENGTH + SQUARE_LENGTH//2, offset + row * SQUARE_LENGTH + SQUARE_LENGTH//2),SQUARE_LENGTH//2)
            elif board[row][col] == 'R':
                pygame.draw.circle(screen,(255,0,0),(col * SQUARE_LENGTH + SQUARE_LENGTH//2, offset + row * SQUARE_LENGTH + SQUARE_LENGTH//2),SQUARE_LENGTH//2)
            else:
                pygame.draw.circle(screen,(255,255,0),(col * SQUARE_LENGTH + SQUARE_LENGTH//2, offset + row * SQUARE_LENGTH + SQUARE_LENGTH//2),SQUARE_LENGTH//2)




    if x is not None:
        pygame.draw.circle(screen,color[turn],(x,y),SQUARE_LENGTH//2)

    
    






def falling_animation(col,row_to_fall_into):

    center_x = col * SQUARE_LENGTH + SQUARE_LENGTH//2
    center_y = SQUARE_LENGTH//2

    center_y_to_fall_to = 100 + row_to_fall_into * SQUARE_LENGTH + SQUARE_LENGTH // 2

    while center_y != center_y_to_fall_to:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        center_y += 10
        
        
    
        screen.fill((255,255,255))


        draw_board(center_x,center_y)
        #pygame.draw.circle(screen,color[turn],(center_x,center_y),SQUARE_LENGTH//2)

        pygame.display.update()

        clock.tick(60)

    
    pygame.time.wait(500)
    






        






pygame.display.set_caption("Connect 4")



color = {'R': (255,0,0),'Y': (255,255,0)}

done = False
turn = random.choice(('R','Y'))


def check_game_over(row_placed,col_placed):

    
    count = 1
    current_row= row_placed + 1

    while current_row < rows and count != 4 and board[current_row][col_placed] == turn:
        count += 1
        current_row += 1


    if count == 4:
        return True


    left_count = 1
    current_col = col_placed - 1

    while current_col > 0 and left_count != 4 and board[row_placed][current_col] == turn:
        left_count += 1
        current_col -= 1


    if left_count == 4:
        return True

    

    right_count = 1
    current_col = col_placed + 1

    while current_col < cols and right_count != 4 and board[row_placed][current_col] == turn:
        right_count += 1
        current_col += 1



    if right_count + left_count - 1 >= 4:
        return True

    
    
    up_left_count = 1
    current_row,current_col =row_placed - 1,col_placed - 1

    while current_row > 0 and current_col > 0 and up_left_count != 4 and board[current_row][current_col] == turn:
        up_left_count += 1
        current_row -= 1
        current_col -= 1


    if up_left_count == 4:
        return True


    down_right_count = 1
    current_row,current_col = row_placed + 1,col_placed + 1

    while current_row < rows and current_col < cols and down_right_count != 4 and board[current_row][current_col] == turn:
        down_right_count += 1
        current_row += 1
        current_col += 1

    if down_right_count + up_left_count - 1 >= 4:
        return True


    up_right_count = 1
    current_row,current_col = row_placed - 1,col_placed + 1

    while current_row > 0 and current_col < cols and up_right_count != 4 and board[current_row][current_col] == turn:
        up_right_count += 1
        current_row -= 1
        current_col += 1


    if up_right_count == 4:
        return True



    down_left_count = 1
    current_row,current_col = row_placed + 1,col_placed - 1

    while current_row < rows and current_col > 0 and down_left_count != 4 and board[current_row][current_col] == turn:
        down_left_count += 1
        current_row += 1
        current_col -= 1
    
    if up_right_count + down_left_count - 1 >= 4:
        return True


    return False


game_over = False

font = pygame.font.SysFont("comicsansms",42)

text_mapping = {'R': 'RED','Y': 'YELLOW'}
turn_text = font.render(f"{text_mapping[turn]}'s TURN",True,color[turn])

enter_text = font.render("Hit ENTER to play again!",True,(0,0,0))
offset = 100
turns = 0
while not done:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                x,_ = pygame.mouse.get_pos()

                col = x // SQUARE_LENGTH

                if board[0][col] == None:


                    first_empty_row_from_bottom = rows - 1

                    while board[first_empty_row_from_bottom][col] != None:
                        first_empty_row_from_bottom -= 1


                    falling_animation(col,first_empty_row_from_bottom)
                    board[first_empty_row_from_bottom][col] = turn
                    turns += 1
                    winner = check_game_over(first_empty_row_from_bottom,col)
                    
                    if winner:
                        game_over = True
                        turn_text = font.render(f"{text_mapping[turn]} WINS!",True,color[turn])
                    elif turns == rows * cols:
                        game_over = True
                        turn_text = font.render("DRAW!",True,color[turn])
                    else:
                        if turn == 'R':
                            turn = 'Y'
                        else:
                            turn = 'R'

                        turn_text = font.render(f"{text_mapping[turn]}'S TURN",True,color[turn])
            elif event.key == pygame.K_RETURN:

                board = [[None for _ in range(cols)] for _ in range(rows)]
                game_over = False
                turns = 0
                turn = random.choice(('R','Y'))
                turn_text = font.render(f"{text_mapping[turn]}'S TURN",True,color[turn])











    




    screen.fill((255,255,255))
    x,y = pygame.mouse.get_pos()
    
    if not game_over:
        col = x // SQUARE_LENGTH
        pygame.draw.circle(screen,color[turn],(col * SQUARE_LENGTH + SQUARE_LENGTH//2,SQUARE_LENGTH//2),SQUARE_LENGTH//2)
    screen.blit(turn_text,(SCREEN_WIDTH//2 - turn_text.get_width()//2,BOARD_HEIGHT + offset + (SCREEN_HEIGHT -  BOARD_HEIGHT)//4 - turn_text.get_height()//2))
    if game_over:

        screen.blit(enter_text,(SCREEN_WIDTH//2 - enter_text.get_width()//2,offset//2 -enter_text.get_height()//2))
    draw_board()
    pygame.display.update()
    clock.tick(FPS)






