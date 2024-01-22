import pygame
import sys
import random
import numpy as np

import start_game
import game_over_menu
import end_game_snake

import datetime
import viewing_database_snake
import multiprocessing



class Level3:
    def __init__(self, clr_snake, clr_apple):
        def apple_check():
            self.apple_pos = [random.randrange(1, self.matrix_size - 1) for _ in range(2)]
            if self.matrix[self.apple_pos[0]][self.apple_pos[1]] == 0:
                self.matrix[self.apple_pos[0]][self.apple_pos[1]] = 2  # Отметить позицию яблока на матрице
                print(self.matrix)
            else:
                apple_check()

        pygame.init()
        pygame.display.set_caption('Змейка: Уровень 3')

        self.win_size = 800
        self.win = pygame.display.set_mode((1280, self.win_size))

        self.snake_size = 40
        self.snake_pos = [[0, 0]]  # Позиция змейки

        self.color_snake, self.color_apple = clr_snake, clr_apple

        self.matrix_size = 20
        self.matrix = self.generate_matrix()  # Игровая матрица

        self.direction = 'RIGHT'  # Направление движения змейки

        apple_check()
        self.mark = 0  # Очки

        self.btn_again_pos = [800, 50, 100, 50]  # Позиция кнопки "Заново"
        self.btn_point_pos = [800, 0, 100, 50]  # Позиция кнопки с отображением очков

        self.btn_point_pos = [800, 0, 100, 50]  # Позиция кнопки с отображением очков
        self.btn_main_pos = [800, 50, 100, 50]  # Позиция кнопки "Главная"
        self.btn_history_pos = [800, 100, 100, 50]  # Позиция кнопки "История"
        self.btn_again_pos = [800, 150, 100, 50]  # Позиция кнопки "Заново"

        self.blue = (165, 166, 246)
        self.yellow = (255, 218, 68)
        self.green = (16, 207, 117)
        self.red = (235, 87, 87)
        self.gray = (35, 62, 84)

        self.dark = (0, 0, 0)
        self.dark_yellow = (94, 80, 23)
        self.dark_red = (158, 27, 36)
        self.dark_blue = (79, 79, 117)
        self.dark_green = (8, 105, 59)

    def generate_matrix(self):
        matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=int)

        # Установить начальную позицию змейки на матрице
        matrix[self.snake_pos[0][0]][self.snake_pos[0][1]] = 1

        def is_valid_wall(matrix, row, col, length, is_horizontal):
            if is_horizontal:
                if col + length > self.matrix_size - 1 or col == 0:
                    return False
                if np.any(matrix[row, max(0, col - 1):min(self.matrix_size, col + length + 1)] != 0):
                    return False
            else:
                if row + length > self.matrix_size - 1 or row == 0:
                    return False
                if np.any(matrix[max(0, row - 1):min(self.matrix_size, row + length + 1), col] != 0):
                    return False
            return True

        def place_wall(matrix, row, col, length, is_horizontal):
            if is_horizontal:
                matrix[row, col:col + length] = 3
            else:
                matrix[row:row + length, col] = 3

        wall_orientations = [True, False, True, False, random.choice([True, False])]
        random.shuffle(wall_orientations)

        # Разместить преграды на матрице
        for is_horizontal in wall_orientations:
            wall_placed = False
            while not wall_placed:
                length = random.randint(4, 7)
                row, col = random.randint(1, self.matrix_size - 2), random.randint(1, self.matrix_size - 2)
                if is_valid_wall(matrix, row, col, length, is_horizontal):
                    place_wall(matrix, row, col, length, is_horizontal)
                    wall_placed = True

        return matrix

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.win, ac, (x, y, w, h), border_radius=10)
        else:
            pygame.draw.rect(self.win, ic, (x, y, w, h), border_radius=10)

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.win.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.direction = 'RIGHT'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Обработка нажатия кнопки "Заново"
                    if (self.btn_again_pos[0] < mouse_pos[0] < self.btn_again_pos[0] + self.btn_again_pos[2] and
                            self.btn_again_pos[1] < mouse_pos[1] < self.btn_again_pos[1] + self.btn_again_pos[3]):
                        qt_process = (
                            multiprocessing.Process
                            (target=viewing_database_snake.tb_app('level3', self.mark, datetime.date.today())))
                        qt_process.start()
                        Level3(self.color_snake, self.color_apple).run()

                    # Обработка нажатия кнопки "Главная"
                    elif (self.btn_main_pos[0] < mouse_pos[0] < self.btn_main_pos[0] + self.btn_main_pos[2] and
                          self.btn_main_pos[1] < mouse_pos[1] < self.btn_main_pos[1] + self.btn_main_pos[3]):
                        qt_process = (
                            multiprocessing.Process
                            (target=viewing_database_snake.tb_app('level3', self.mark, datetime.date.today())))
                        qt_process.start()
                        start_game.Game(self.color_snake, self.color_apple).run()

                    # Обработка нажатия кнопки "История"
                    elif (self.btn_history_pos[0] < mouse_pos[0] < self.btn_history_pos[0] +
                          self.btn_history_pos[2] and
                          self.btn_history_pos[1] < mouse_pos[1] < self.btn_history_pos[1] +
                          self.btn_history_pos[3]):
                        qt_process = multiprocessing.Process(target=viewing_database_snake.print_app('level3'))
                        qt_process.start()

            # Обновление позиции змейки в соответствии с выбранным направлением
            if self.direction == 'UP':
                if (self.snake_pos[0][1] - 1) % self.matrix_size == 0 and len(self.snake_pos) > 1:
                    print(6573409)
                    self.snake_pos.pop()
                self.snake_pos.insert(0, [self.snake_pos[0][0], (self.snake_pos[0][1] - 1)
                                          % self.matrix_size])
            elif self.direction == 'DOWN':
                if (self.snake_pos[0][1] + 1) % self.matrix_size == 0 and len(self.snake_pos) > 1:
                    print(7890)
                    self.snake_pos.pop()
                self.snake_pos.insert(0, [self.snake_pos[0][0], (self.snake_pos[0][1] + 1)
                                          % self.matrix_size])
            elif self.direction == 'LEFT':
                if (self.snake_pos[0][0] - 1) % self.matrix_size == 0 and len(self.snake_pos) > 1:
                    print(123)
                    self.snake_pos.pop()
                self.snake_pos.insert(0, [(self.snake_pos[0][0] - 1) % self.matrix_size,
                                          self.snake_pos[0][1]])
            elif self.direction == 'RIGHT':
                if (self.snake_pos[0][0] + 1) % self.matrix_size == 0 and len(self.snake_pos) > 1:
                    print(123456)
                    self.snake_pos.pop()
                self.snake_pos.insert(0, [(self.snake_pos[0][0] + 1) % self.matrix_size,
                                          self.snake_pos[0][1]])

            # Проверка столкновения с яблоком
            if self.snake_pos[0] == self.apple_pos:
                def apple_check():
                    self.apple_pos = [random.randrange(1, self.matrix_size - 1) for _ in range(2)]
                    if self.matrix[self.apple_pos[0]][self.apple_pos[1]] == 0:
                        self.matrix[self.apple_pos[0]][self.apple_pos[1]] = 2  # Отметить позицию яблока на матрице
                        print(self.matrix)
                    else:
                        apple_check()

                apple_check()
                self.mark += 1
                print(f'Текущие очки: {self.mark}')
            else:
                tail = self.snake_pos.pop()
                self.matrix[tail[0]][tail[1]] = 0

            # Проверка столкновения с преградой или самой собой
            if (self.matrix[self.snake_pos[0][0]][self.snake_pos[0][1]] == 1
                    or self.matrix[self.snake_pos[0][0]][self.snake_pos[0][1]] == 3):
                qt_process = (
                    multiprocessing.Process
                    (target=viewing_database_snake.tb_app('level3', self.mark, datetime.date.today())))
                qt_process.start()
                game_over_menu.Game().run('lvl3', self.color_snake, self.color_apple)

            else:
                self.matrix[self.snake_pos[0][0]][self.snake_pos[0][1]] = 1

            if (self.snake_pos[0][0] < 0 or self.snake_pos[0][0] >= self.matrix_size or
                    self.snake_pos[0][1] < 0 or self.snake_pos[0][1] >= self.matrix_size):
                print(123)
                # self.snake_pos[-1].pop()

            if self.mark == 10:
                qt_process = (
                    multiprocessing.Process
                    (target=viewing_database_snake.tb_app('level3', self.mark, datetime.date.today())))
                qt_process.start()
                end_game_snake.Game().run(self.color_snake, self.color_apple)

            self.win.fill((0, 0, 0))

            # Отрисовка сетки на игровом поле
            for i in range(0, self.win_size, self.snake_size):
                pygame.draw.lines(self.win, (125, 125, 125), True, ((i, 0),
                                                                    (i, self.win_size)), 1)
                pygame.draw.lines(self.win, (125, 125, 125), True, ((0, i),
                                                                    (self.win_size, i)), 1)

            # Отрисовка змейки
            for pos in self.snake_pos:
                pygame.draw.rect(self.win, self.color_snake,
                                 pygame.Rect(pos[0] * self.snake_size, pos[1] * self.snake_size, self.snake_size,
                                             self.snake_size),
                                 border_radius=10)

            # Отрисовка яблока
            pygame.draw.rect(self.win, self.color_apple,
                             pygame.Rect(self.apple_pos[0] * self.snake_size, self.apple_pos[1] * self.snake_size,
                                         self.snake_size, self.snake_size),
                             border_radius=50)

            # Отрисовка преграды
            for i in range(self.matrix_size):
                for j in range(self.matrix_size):
                    if self.matrix[i][j] == 3:
                        pygame.draw.rect(self.win, self.dark_red,
                                         pygame.Rect(i * self.snake_size, j * self.snake_size, self.snake_size,
                                                     self.snake_size))

            # Отрисовка кнопок
            self.button("Очки: " + str(len(self.snake_pos) - 1), *self.btn_point_pos, self.dark, self.green)
            self.button("Главная", *self.btn_main_pos, self.blue, self.dark_blue)
            self.button("История", *self.btn_history_pos, self.yellow, self.dark_yellow)
            self.button("Заново", *self.btn_again_pos, self.red, self.dark_red)

            pygame.display.update()

            pygame.time.Clock().tick(10)
