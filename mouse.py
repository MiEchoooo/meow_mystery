import pygame

class Mouse:
    def __init__(self, x, y, scene_index):
        self.x = x
        self.y = y
        self.scene_index = scene_index
        self.frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.found = False  # ✅ 被点击后设置为 True

        # 加载精灵图
        sprite_sheet = pygame.image.load("assets/items/Mouse-Sheet.png").convert_alpha()
        frame_width = sprite_sheet.get_width() // 4
        frame_height = sprite_sheet.get_height()

        for i in range(4):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt):
        if self.found:
            return  # ✅ 不再更新动画
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

    def draw(self, screen):
        if not self.found:  # ✅ 被发现后不再绘制
            screen.blit(self.image, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.found = True
            return True
        return False
