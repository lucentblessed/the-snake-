import os
import sys
import pygame

import start_game
import level_choice_win



class Skin:
    def __init__(self, clr_snake, clr_apple):
        pygame.init()
        self.size = self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load('data/skin_snake_and_apple_menu.png')
        pygame.display.set_caption('Змейка: Скины')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        # Текущие цвета
        self.color_snake = clr_snake
        self.color_apple = clr_apple

        # Позици текущих цветов
        self.color_snake_pos = [578, 77, 50, 50]
        self.color_apple_pos = [653, 77, 50, 50]

        # Позици новых цветов
        self.color_snake_pos_green = [335, 515, 50, 50]
        self.color_snake_pos_blue = [410, 515, 50, 50]
        self.color_snake_pos_white = [485, 515, 50, 50]

        self.color_apple_pos_red = [660, 515, 50, 50]
        self.color_apple_pos_yellow = [735, 515, 50, 50]
        self.color_apple_pos_blue = [810, 515, 50, 50]

        self.btn_confirm_pos = [522, 629, 203, 48]

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


    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h), border_radius=22)
        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h), border_radius=22)

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def exit_button(self):
        self.button(self.width - 70, 30, 40, 40, (0, 0, 0), '[->', 20, x_indent=12,
                    y_indent=10, font_size=30, filled=1)
        for event in pygame.event.get():
            self.Mouse_x, self.Mouse_y = pygame.mouse.get_pos()
            if (event.type == pygame.MOUSEBUTTONDOWN and self.Mouse_x in range(self.width - 70, self.width - 70 + 40)
                    and self.Mouse_y in range(30, 30 + 40)):
                self.running = False
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Обработка нажатия кнопки "Играть"
                    #if (self.btn_play_pos[0] < mouse_pos[0] < self.btn_play_pos[0] + self.btn_play_pos[2] and
                            #self.btn_play_pos[1] < mouse_pos[1] < self.btn_play_pos[1] + self.btn_play_pos[3]):
                        #level_choice_win.Game().run()

                    if (self.color_snake_pos_green[0] < mouse_pos[0] < self.color_snake_pos_green[0] + self.color_snake_pos_green[2] and
                            self.color_snake_pos_green[1] < mouse_pos[1] < self.color_snake_pos_green[1] + self.color_snake_pos_green[3]):
                        self.color_snake = (16, 207, 117)

                    if (self.color_snake_pos_blue[0] < mouse_pos[0] < self.color_snake_pos_blue[0] + self.color_snake_pos_blue[2] and
                            self.color_snake_pos_blue[1] < mouse_pos[1] < self.color_snake_pos_blue[1] + self.color_snake_pos_blue[3]):
                        self.color_snake = (165, 166, 246)

                    if (self.color_snake_pos_white[0] < mouse_pos[0] < self.color_snake_pos_white[0] + self.color_snake_pos_white[2] and
                            self.color_snake_pos_white[1] < mouse_pos[1] < self.color_snake_pos_white[1] + self.color_snake_pos_white[3]):
                        self.color_snake = (255, 255, 255)

                    if (self.color_apple_pos_red[0] < mouse_pos[0] < self.color_apple_pos_red[0] + self.color_apple_pos_red[2] and
                            self.color_apple_pos_red[1] < mouse_pos[1] < self.color_apple_pos_red[1] + self.color_apple_pos_red[3]):
                        self.color_apple = (235, 87, 87)

                    if (self.color_apple_pos_yellow[0] < mouse_pos[0] < self.color_apple_pos_yellow[0] + self.color_apple_pos_yellow[2] and
                            self.color_apple_pos_yellow[1] < mouse_pos[1] < self.color_apple_pos_yellow[1] + self.color_apple_pos_yellow[3]):
                        self.color_apple = (255, 218, 68)

                    if (self.color_apple_pos_blue[0] < mouse_pos[0] < self.color_apple_pos_blue[0] + self.color_apple_pos_blue[2] and
                            self.color_apple_pos_blue[1] < mouse_pos[1] < self.color_apple_pos_blue[1] + self.color_apple_pos_blue[3]):
                        self.color_apple = (88, 155, 212)

                    if (self.btn_confirm_pos[0] < mouse_pos[0] < self.btn_confirm_pos[0] + self.btn_confirm_pos[2] and
                            self.btn_confirm_pos[1] < mouse_pos[1] < self.btn_confirm_pos[1] + self.btn_confirm_pos[3]):
                        start_game.Game(self.color_snake, self.color_apple).run()

            self.button('', *self.color_snake_pos, self.color_snake, self.color_snake)
            self.button('', *self.color_apple_pos, self.color_apple, self.color_apple)
            pygame.display.update()

            self.screen.blit(self.background_image, (0, 0))
            #pygame.display.flip()
            self.clock.tick(50)

        pygame.quit()