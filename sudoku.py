import pygame
import time

pygame.font.init()

class Grid:
    beginner = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    easy = [
        [0, 0, 0, 1, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 3, 7, 0, 1, 5],
        [0, 0, 0, 0, 5, 4, 0, 0, 8],
        [0, 0, 3, 0, 2, 0, 7, 0, 0],
        [0, 0, 2, 5, 0, 9, 0, 0, 0],
        [1, 0, 6, 0, 0, 8, 2, 0, 4],
        [0, 0, 0, 0, 4, 0, 6, 9, 0],
        [0, 7, 9, 0, 0, 6, 0, 8, 0],
        [0, 0, 8, 0, 0, 3, 1, 4, 2]
    ]
    medium = [
        [0, 1, 4, 2, 0, 0, 0, 0, 0],
        [0, 0, 3, 4, 9, 1, 0, 0, 0],
        [0, 0, 0, 7, 8, 0, 0, 5, 0],
        [3, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 1, 0, 6, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 7],
        [0, 0, 0, 6, 2, 0, 0, 3, 0],
        [6, 0, 1, 5, 0, 0, 0, 2, 0],
        [2, 0, 0, 0, 0, 7, 0, 0, 8]
    ]
    hard = [
        [0, 0, 0, 0, 0, 0, 8, 0, 4],
        [0, 0, 9, 0, 6, 3, 0, 0, 7],
        [2, 1, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 2, 0, 0, 1, 0],
        [0, 4, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 6, 5, 3, 0, 0, 0, 0],
        [0, 8, 0, 7, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 4, 0, 2, 9, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    def __init__(self, rows, cols, width, height, win, difficulty="easy"):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.win = win

        if difficulty == "beginner":
            self.board = self.beginner
        if difficulty == "easy":
            self.board = self.easy
        if difficulty == "medium":
            self.board = self.medium
        if difficulty == "hard":
            self.board = self.hard
        
        # Creation of 2D array
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)] 
        self.update_model()

    def update_model(self): # Updates cells
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def place(self, val): # Assessment of whether number can be placed using valid and solve function 
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self): # Finds empty cell and checks if number(1-9) is valid. Onve valid number checks ig can solve and if not puts back to 0. If no number(1-9) works then returns False
        find = find_empty(self.model) 
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0 # Backtrack part

        return False

    def solve_gui(self): # Visual of solving process
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100) # Pauses briefly to allow user to see changes

                if self.solve_gui():
                    return True

                self.model[row][col] = 0 # Backtrack part
                self.cubes[row][col].set(0) 
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100) # Pauses briefly to allow user to see changes

        return False
    
    def reset(self): # Clears temp values and resets board
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].set_temp(0)
                self.cubes[i][j].set(self.board[i][j])
        
        self.selected = None
        
        self.update_model()

class Cube: # Each individual cell
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0: # Style if there is a temp but no permanent value
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not(self.value == 0): # Style if permanent value
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected: # Style when cube is selected
            pygame.draw.rect(win, (255,0,0), (x, y, gap, gap), 3)
        

    def draw_change(self, win, g = True): # Colour changes of cubes when solver running
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val): # Setting confirmed value
        self.value = val

    def set_temp(self, val): # Setting temp. value
        self.temp = val


def draw_button(win, text, x, y, width, height, color):
    pygame.draw.rect(win, color, (x, y, width, height))
    
    font = pygame.font.SysFont("comicsans", 35)
    text_render = font.render(text, True, (0, 0, 0))
    win.blit(text_render, (x + (width - text_render.get_width()) // 2, y + (height - text_render.get_height()) // 2))

def select_board(win):
    running = True
    while running: 
        win.fill((255, 255, 255))
        
        # Draw buttons
        draw_button(win, "Beginner", 100, 100, 200, 50, (200, 200, 200))
        draw_button(win, "Easy", 100, 200, 200, 50, (200, 200, 200))       
        draw_button(win, "Medium", 100, 300, 200, 50, (200, 200, 200))     
        draw_button(win, "Hard", 100, 400, 200, 50, (200, 200, 200))       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 100 <= mouse_x <= 300 and 100 <= mouse_y <= 150:
                    return 'beginner'
                if 100 <= mouse_x <= 300 and 200 <= mouse_y <= 250:
                    return 'easy'
                if 100 <= mouse_x <= 300 and 300 <= mouse_y <= 350:
                    return 'medium'
                if 100 <= mouse_x <= 300 and 400 <= mouse_y <= 450:
                    return 'hard'

        pygame.display.update()

    return None



def find_empty(bo): # Find next empty cell
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

def valid(bo, num, pos): # Finds number that isn't already in row, col., or box
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))

    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560)) # Determining where on window to draw timer
    
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560)) # Determining where on window to draw strikes
    
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((800, 800)) # Size of window
    pygame.display.set_caption("Sudoku")

    # Call board selector function
    selected_difficulty = select_board(win)
    if selected_difficulty is None:
        return
    
    board = Grid(9, 9, 540, 540, win, selected_difficulty)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        # Button controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if board.selected:
                    i, j = board.selected

                    if board.cubes[i][j].value == 0:

                        if event.key == pygame.K_1:
                            if board.cubes[i][j].temp != 1:
                                key = 1
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_2:
                            if board.cubes[i][j].temp != 2:
                                key = 2
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_3:
                            if board.cubes[i][j].temp != 3:
                                key = 3
                            else:
                                strikes = confirm_num(strikes, board, i, j)                    
                        if event.key == pygame.K_4:
                            if board.cubes[i][j].temp != 4:
                                key = 4
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_5:
                            if board.cubes[i][j].temp != 5:
                                key = 5
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_6:
                            if board.cubes[i][j].temp != 6:
                                key = 6
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_7:
                            if board.cubes[i][j].temp != 7:
                                key = 7
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_8:
                            if board.cubes[i][j].temp != 8:
                                key = 8
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_9:
                            if board.cubes[i][j].temp != 9:
                                key = 9
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP1:
                            if board.cubes[i][j].temp != 1:
                                key = 1
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP2:
                            if board.cubes[i][j].temp != 2:
                                key = 2
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP3:
                            if board.cubes[i][j].temp != 3:
                                key = 3
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP4:
                            if board.cubes[i][j].temp != 4:
                                key = 4
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP5:
                            if board.cubes[i][j].temp != 5:
                                key = 5
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP6:
                            if board.cubes[i][j].temp != 6:
                                key = 6
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP7:
                            if board.cubes[i][j].temp != 7:
                                key = 7
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP8:
                            if board.cubes[i][j].temp != 8:
                                key = 8
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        if event.key == pygame.K_KP9:
                            if board.cubes[i][j].temp != 9:
                                key = 9
                            else:
                                strikes = confirm_num(strikes, board, i, j)
                        
                    # Manoeuvre grid with arrowpad
                    if event.key == pygame.K_UP:
                        if i > 0:
                            board.select(i - 1, j)
                            key = None
                    if event.key == pygame.K_DOWN:
                        if i < 8:
                            board.select(i + 1, j)
                            key = None
                    if event.key == pygame.K_LEFT:
                        if j > 0:
                            board.select(i, j - 1)
                            key = None
                    if event.key == pygame.K_RIGHT:
                        if j < 8:
                            board.select(i, j + 1)
                            key = None

                # Clear cell 
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None


                # Reset board with r
                if event.key == pygame.K_r:
                    board.reset()
                    start = time.time()
                    strikes = 0

                # Confirm number entry with return
                if event.key == pygame.K_RETURN:
                    strikes = confirm_num(strikes, board, i , j)
                
                # Run solver with spacebar
                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                redraw_window(win, board, play_time, strikes)
                pygame.display.update()

            # Use of mouse to manoeuvre board
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        
        if board.selected and key != None:
            board.sketch(key)
        
        # Function to confirm number in cell. Can be run through Enter or pressing number again to confirm entry
        def confirm_num(strikes, board, i, j):
            if board.place(board.cubes[i][j].temp) == False:
                strikes += 1

            return strikes

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()