import pygame

class Diary:
    def __init__(self, x, y, image_path, scene_index):
        self.x = x
        self.y = y
        self.base_image = pygame.image.load(image_path).convert_alpha()
        self.scale = 0.3  # 初始缩放
        self.max_scale = 1.5
        self.scale_step = 0.05
        self.image = pygame.transform.smoothscale(
            self.base_image,
            (int(self.base_image.get_width() * self.scale),
             int(self.base_image.get_height() * self.scale))
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.scene_index = scene_index

        self.visible = True
        self.animating = False
        self.animation_done = False

    def start_animation(self):
        if not self.animating and not self.animation_done:
            self.animating = True

    def update(self):
        if self.animating and self.scale < self.max_scale:
            self.scale += self.scale_step
            self.image = pygame.transform.smoothscale(
                self.base_image,
                (int(self.base_image.get_width() * self.scale),
                 int(self.base_image.get_height() * self.scale))
            )
            self.rect = self.image.get_rect(center=(self.x, self.y))
        elif self.animating:
            self.animating = False
            self.animation_done = True

    def draw(self, screen, current_scene):
        if self.visible and current_scene == self.scene_index:
            screen.blit(self.image, self.rect)

    def is_near(self, player_x, player_y):
        dx = abs(player_x - self.x)
        dy = abs(player_y - self.y)
        return dx < 80 and dy < 80
