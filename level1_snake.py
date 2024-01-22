import pygame
import sys
import random
import os

import start_game
import game_over_menu
import win_game_skane

import datetime
import viewing_database_snake
import multiprocessing


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 500, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Level1:
    def __init__(self, clr_snake, clr_apple):
        pygame.init()

        # Установка размеров окна
        self.win_size = 800
        self.win = pygame.display.set_mode((1280, self.win_size))
        pygame.display.set_caption('Змейка: Уровень 1')

        # Установка размера и начального положения змейки
        self.snake_size = 40
        self.snake_pos = [[0, 0]]

        self.btn_point_pos = [800, 0, 100, 50]  # Позиция кнопки с отображением очков
        self.btn_main_pos = [800, 50, 100, 50]  # Позиция кнопки "Главная"
        self.btn_history_pos = [800, 100, 100, 50]  # Позиция кнопки "История"
        self.btn_again_pos = [800, 150, 100, 50]  # Позиция кнопки "Заново"

        self.blue = (165, 166, 246)
        self.yellow = (255, 218, 68)
        self.green = (16, 207, 117)
        self.red = (235, 87, 87)
        self.gray = (35, 62, 84)
        self.color_snake = clr_snake
        self.color_apple = clr_apple

        self.dark = (0, 0, 0)
        self.dark_yellow = (94, 80, 23)
        self.dark_red = (158, 27, 36)
        self.dark_blue = (79, 79, 117)
        self.dark_green = (8, 105, 59)

        # Установка направления движения змейки
        self.direction = 'RIGHT'

        # Создание яблока
        self.apple_pos = [random.randrange(0, self.win_size, self.snake_size) for _ in range(2)]
        self.mark = 0  # Количество собранных яблок

        self.dragon = AnimatedSprite(load_image("анимка.png"), 4, 2, 0, 0)

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

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Изменение направления движения змейки при нажатии клавиш
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
                            (target=viewing_database_snake.tb_app('level1', self.mark, datetime.date.today())))
                        qt_process.start()
                        Level1(self.color_snake, self.color_apple).run()

                    # Обработка нажатия кнопки "Главная"
                    elif (self.btn_main_pos[0] < mouse_pos[0] < self.btn_main_pos[0] + self.btn_main_pos[2] and
                          self.btn_main_pos[1] < mouse_pos[1] < self.btn_main_pos[1] + self.btn_main_pos[3]):
                        qt_process = (
                            multiprocessing.Process
                            (target=viewing_database_snake.tb_app('level1', self.mark, datetime.date.today())))
                        qt_process.start()


                        start_game.Game(self.color_snake, self.color_apple).run()

                    # Обработка нажатия кнопки "История"
                    elif (self.btn_history_pos[0] < mouse_pos[0] < self.btn_history_pos[0] + self.btn_history_pos[2] and
                          self.btn_history_pos[1] < mouse_pos[1] < self.btn_history_pos[1] + self.btn_history_pos[3]):
                        qt_process = multiprocessing.Process(target=viewing_database_snake.print_app('level1'))
                        qt_process.start()

            # Обновление позиции змейки
            if self.direction == 'UP':
                self.snake_pos.insert(0,
                                      [self.snake_pos[0][0], (self.snake_pos[0][1] - self.snake_size)
                                       % self.win_size])
            elif self.direction == 'DOWN':
                self.snake_pos.insert(0,
                                      [self.snake_pos[0][0], (self.snake_pos[0][1] + self.snake_size)
                                       % self.win_size])
            elif self.direction == 'LEFT':
                self.snake_pos.insert(0,
                                      [(self.snake_pos[0][0] - self.snake_size) % self.win_size,
                                       self.snake_pos[0][1]])
            elif self.direction == 'RIGHT':
                self.snake_pos.insert(0,
                                      [(self.snake_pos[0][0] + self.snake_size) % self.win_size,
                                       self.snake_pos[0][1]])

            # Проверка на столкновение с яблоком
            if self.snake_pos[0] == self.apple_pos:
                self.apple_pos = [random.randrange(0, self.win_size, self.snake_size) for _ in range(2)]
                self.mark += 1
                print(f'Текущие очки: {self.mark}')
            else:
                self.snake_pos.pop()

            # Проверка на столкновение с собственным телом
            if self.snake_pos[0] in self.snake_pos[1:]:
                qt_process = (
                    multiprocessing.Process
                    (target=viewing_database_snake.tb_app('level1', self.mark, datetime.date.today())))
                qt_process.start()
                game_over_menu.Game().run('lvl1', self.color_snake, self.color_apple)

            if self.mark == 5:
                qt_process = (
                    multiprocessing.Process
                    (target=viewing_database_snake.tb_app('level1', self.mark, datetime.date.today())))
                qt_process.start()
                win_game_skane.Game().run('lvl1', self.color_snake, self.color_apple)

            # Очистка окна
            self.win.fill((255, 255, 255))

            # Отрисовка сетки
            for i in range(0, self.win_size, self.snake_size):
                pygame.draw.lines(self.win, (125, 125, 125), True, ((i, 0),
                                                                    (i, self.win_size)), 1)
                pygame.draw.lines(self.win, (125, 125, 125), True, ((0, i),
                                                                    (self.win_size, i)), 1)

            # Отрисовка змейки
            for pos in self.snake_pos:
                pygame.draw.rect(self.win, self.color_snake, pygame.Rect(pos[0], pos[1], self.snake_size,
                                                                         self.snake_size),
                                 border_radius=10)

            # Отрисовка кнопок

            self.button("Очки: " + str(len(self.snake_pos) - 1), *self.btn_point_pos, self.dark, self.green)
            self.button("Главная", *self.btn_main_pos, self.blue, self.dark_blue)
            self.button("История", *self.btn_history_pos, self.yellow, self.dark_yellow)
            self.button("Заново", *self.btn_again_pos, self.red, self.dark_red)

            # Отрисовка яблока
            pygame.draw.rect(self.win, self.color_apple,
                             pygame.Rect(self.apple_pos[0], self.apple_pos[1], self.snake_size, self.snake_size),
                             border_radius=50)
            pygame.display.update()
            all_sprites.draw(self.win)
            pygame.time.Clock().tick(10)  # Задержка
