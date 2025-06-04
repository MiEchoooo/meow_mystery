import pygame

class DialogueBox:
    def __init__(self, width, height, font):
        self.font = font
        self.width = width
        self.height = 120
        self.box_surface = pygame.Surface((width, self.height))
        self.box_surface.set_alpha(220)
        self.box_surface.fill((255, 255, 240))

        self.padding = 20
        self.text_lines = []
        self.current_index = 0
        self.visible = False

    def set_text(self, text):
        self.current_text = text  # ✅ 保存原始文本
        # 自动分行
        words = text.split(" ")
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] < self.width - 2 * self.padding:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        self.text_lines = lines
        self.current_index = 0
        self.visible = True

    def advance(self):
        self.current_index += 2  # 每次显示两行
        if self.current_index >= len(self.text_lines):
            self.visible = False

    def draw(self, screen, bottom_y):
        if not self.visible:
            return

        screen.blit(self.box_surface, (0, bottom_y - self.height))

        # 渲染文字
        for i in range(2):  # 一次最多显示两行
            if self.current_index + i < len(self.text_lines):
                line = self.text_lines[self.current_index + i]
                rendered = self.font.render(line, True, (0, 0, 0))
                screen.blit(rendered, (self.padding, bottom_y - self.height + self.padding + i * 30))
