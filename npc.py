import pygame

class NPC:
    def __init__(self, x, y, image_path, dialogue_texts, scene_index=0, patrol_area=None):
        self.x = x
        self.y = y
        self.dialogue_texts = dialogue_texts  # 多阶段对话文本列表
        self.dialogue_stage = 0               # 当前对话阶段
        self.scene_index = scene_index        # 所属场景编号
        self.patrol_area = patrol_area        # 巡逻范围（现在不再使用）
        self.direction = 1                    # 移动方向（保留变量结构）
        self.speed = 1                        # 移动速度（保留变量结构）

        # 加载动画图像
        sheet = pygame.image.load(image_path).convert_alpha()
        self.frames = []
        frame_width = 32
        frame_height = 32
        scale = 4
        for i in range(7):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            self.frames.append(frame)

        self.frame = 0
        self.timer = 0
        self.frame_delay = 10

    def update(self, current_scene_index):
        # 仅当处于目标场景时才更新动画帧
        if current_scene_index != self.scene_index:
            return

        self.timer += 1
        if self.timer >= self.frame_delay:
            self.frame = (self.frame + 1) % len(self.frames)
            self.timer = 0

    def draw(self, screen, current_scene_index):
        # 仅当处于目标场景时才绘制
        if current_scene_index == self.scene_index:
            screen.blit(self.frames[self.frame], (self.x, self.y))

    def get_current_dialogue(self):
        return self.dialogue_texts[self.dialogue_stage]

    def advance_dialogue_stage(self):
        if self.dialogue_stage < len(self.dialogue_texts) - 1:
            self.dialogue_stage += 1
