import pygame
import random

class MiniGame:
    def __init__(self, width, height, font, image_path="assets/minigame/puzzle.jpg"):
        self.width = width
        self.height = height
        self.font = font
        self.rows = 2
        self.cols = 3
        self.image = pygame.image.load(image_path).convert()
        self.tile_width = self.image.get_width() // self.cols
        self.tile_height = self.image.get_height() // self.rows
        self.margin_x = width // 2 - (self.cols * self.tile_width) // 2
        self.margin_y = height // 2 - (self.rows * self.tile_height) // 2

        # 切割图片
        self.tiles = []
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height)
                sub_img = self.image.subsurface(rect).copy()
                self.tiles.append(sub_img)

        self.correct_order = list(range(len(self.tiles)))
        self.current_order = self.correct_order[:]
        random.shuffle(self.current_order)

        self.selected = None
        self.completed = False

    def draw(self, screen):
        for i, tile_index in enumerate(self.current_order):
            x = i % self.cols
            y = i // self.cols
            screen.blit(self.tiles[tile_index], (
                self.margin_x + x * self.tile_width,
                self.margin_y + y * self.tile_height
            ))

        # 边框
        pygame.draw.rect(screen, (0, 0, 0), (
            self.margin_x - 5, self.margin_y - 5,
            self.cols * self.tile_width + 10,
            self.rows * self.tile_height + 10), 2)

        # 完成提示
        if self.completed:
            done_text = self.font.render("拼图完成！按 ESC 关闭", True, (0, 150, 0))
            screen.blit(done_text, (self.width // 2 - 100, self.margin_y + self.rows * self.tile_height + 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if self.margin_x <= mouse_x < self.margin_x + self.cols * self.tile_width and \
               self.margin_y <= mouse_y < self.margin_y + self.rows * self.tile_height:
                grid_x = (mouse_x - self.margin_x) // self.tile_width
                grid_y = (mouse_y - self.margin_y) // self.tile_height
                index = grid_y * self.cols + grid_x

                if self.selected is None:
                    self.selected = index
                else:
                    # 交换块
                    self.current_order[self.selected], self.current_order[index] = self.current_order[index], self.current_order[self.selected]
                    self.selected = None
                    if self.current_order == self.correct_order:
                        self.completed = True

def run_puzzle_game():
    """运行拼图小游戏，完成后返回 True"""
    pygame.init()
    WIDTH, HEIGHT = 600, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("拼图小游戏")
    font = pygame.font.SysFont("Microsoft YaHei", 24)

    game = MiniGame(WIDTH, HEIGHT, font)
    clock = pygame.time.Clock()
    running = True
    finished = False

    while running:
        screen.fill((240, 240, 240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game.completed:
                    running = False
                    finished = True
            else:
                game.handle_event(event)

        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return finished
