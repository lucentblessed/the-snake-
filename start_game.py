import os
import sys
import pygame

import level_choice_win
import skins_snake


class Game:
    def __init__(self, color_snake, color_apple):
        pygame.init()
        self.size = self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode(self.size)
        self.background_image = pygame.image.load('data/main_menu.png')
        pygame.display.set_caption('Змейка: Главная')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.btn_play_pos = [585, 450, 151, 36]
        self.btn_skin_pos = [587, 501, 148, 36]

        self.color_snake = color_snake#(255, 135, 255) #(16, 207, 117)
        self.color_apple = color_apple

        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.dragon = self.AnimatedSprite(self.all_sprites, self.load_image("анимка.png"), 4, 2, 0, 300)
        self.dragon = self.AnimatedSprite(self.all_sprites, self.load_image("анимка.png"), 4, 2, 925, 300)

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
            if (event.type == pygame.MOUSEBUTTONDOWN and self.Mouse_x in range(1205, 1265)
                    and self.Mouse_y in range(19, 71)):
                self.running = False

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, all_sprites, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
            self.cur_frame = 0
            self.cut_sheet(sheet, columns, rows)
            self.image = self.frames[self.cur_frame]
            self.rect = self.image.get_rect(topleft=(x, y))

        def cut_sheet(self, sheet, columns, rows):
            frame_width = sheet.get_width() // columns
            frame_height = sheet.get_height() // rows
            for j in range(rows):
                for i in range(columns):
                    frame_location = (frame_width * i, frame_height * j)
                    frame = sheet.subsurface(pygame.Rect(frame_location, (frame_width, frame_height)))
                    self.frames.append(frame)

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Обработка нажатия кнопки "Играть"
                    if (self.btn_play_pos[0] < mouse_pos[0] < self.btn_play_pos[0] + self.btn_play_pos[2] and
                            self.btn_play_pos[1] < mouse_pos[1] < self.btn_play_pos[1] + self.btn_play_pos[3]):
                        level_choice_win.Game().run(self.color_snake, self.color_apple)
                    elif (self.btn_skin_pos[0] < mouse_pos[0] < self.btn_skin_pos[0] + self.btn_skin_pos[2] and
                          self.btn_skin_pos[1] < mouse_pos[1] < self.btn_skin_pos[1] + self.btn_skin_pos[3]):
                        skins_snake.Skin(self.color_snake, self.color_apple).run()
                    elif mouse_pos[0] in range(1205, 1265) and mouse_pos[1] in range(19, 71):
                        self.running = False
            self.all_sprites.update()
            # Comment out the following line to keep the background image visible
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background_image, (0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()


if __name__ == "__main__":
    Game((255, 135, 255), (200, 200, 200)).run()