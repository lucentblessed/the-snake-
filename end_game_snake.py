import os
import sys
import pygame

import start_game
import level1_snake
import level2_snake
import level3_snake


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


class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load('data/end_game_menu.png')
        pygame.display.set_caption('Змейка: Конец')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.btn_play_pos = [476, 346, 329, 80]
        self.btn_main_menu_pos = [476, 428, 329, 80]

        self.clock = pygame.time.Clock()
        self.running = True

    def load_image(self, name, colorkey=None):
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

    def exit_button(self):
        self.button(self.width - 70, 30, 40, 40, (0, 0, 0), '[->', 20, x_indent=12,
                    y_indent=10, font_size=30, filled=1)
        for event in pygame.event.get():
            self.Mouse_x, self.Mouse_y = pygame.mouse.get_pos()
            if (event.type == pygame.MOUSEBUTTONDOWN and self.Mouse_x in range(self.width - 70, self.width - 70 + 40)
                    and self.Mouse_y in range(30, 30 + 40)):
                self.running = False
    def run(self,  color_snake, color_apple ):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Обработка нажатия кнопки "Заново"
                    if (self.btn_play_pos[0] < mouse_pos[0] < self.btn_play_pos[0] + self.btn_play_pos[2] and
                            self.btn_play_pos[1] < mouse_pos[1] < self.btn_play_pos[1] + self.btn_play_pos[3]):
                        level3_snake.Level3(color_snake, color_apple).run()

                    # Обработка нажатия кнопки "Главная"
                    elif (self.btn_main_menu_pos[0] < mouse_pos[0] < self.btn_main_menu_pos[0] + self.btn_main_menu_pos[2] and
                          self.btn_main_menu_pos[1] < mouse_pos[1] < self.btn_main_menu_pos[1] + self.btn_main_menu_pos[3]):
                        start_game.Game(color_snake, color_apple).run()


            self.screen.blit(self.background_image, (0, 0))
            pygame.display.flip()
            self.clock.tick(50)

        pygame.quit()