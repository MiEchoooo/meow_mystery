import pygame
import os

class Player:
    def __init__(self, x, y):
        sheet = pygame.image.load(os.path.join("assets", "xiaoying", "xiaoying_tail.png")).convert_alpha()
        frame_width, frame_height, frame_count = 32, 32, 7
        scale = 4
        self.width = frame_width * scale
        self.height = frame_height * scale

        self.right_frames = [
            pygame.transform.scale(
                sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)),
                (self.width, self.height)
            )
            for i in range(frame_count)
        ]
        self.left_frames = [pygame.transform.flip(f, True, False) for f in self.right_frames]

        self.x = x
        self.y = y
        self.speed = 3
        self.facing = "right"
        self.frame = 0
        self.timer = 0
        self.frame_delay = 8
        self.frame_count = frame_count

    def update(self, keys):
        moved = False
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.facing = "left"
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.facing = "right"
            moved = True
        elif keys[pygame.K_UP]:
            self.y -= self.speed
            moved = True
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            moved = True

        if moved:
            self.timer += 1
            if self.timer >= self.frame_delay:
                self.frame = (self.frame + 1) % self.frame_count
                self.timer = 0
        else:
            self.frame = 0

    def draw(self, screen):
        image = self.right_frames[self.frame] if self.facing == "right" else self.left_frames[self.frame]
        screen.blit(image, (self.x, self.y))

