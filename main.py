import pygame
import os
from player import Player
from dialogue import DialogueBox
from map_manager import MapManager
from npc import NPC
from quest_manager import Quest, QuestManager
from puzzle_game import MiniGame
from mouse import Mouse

pygame.init()

WIDTH, HEIGHT = 1280, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("喵影迷踪")

map_manager = MapManager(WIDTH, HEIGHT)
player = Player(800, 600)
quest_manager = QuestManager()

font = pygame.font.SysFont("Microsoft YaHei", 18)
dialogue = DialogueBox(WIDTH, HEIGHT, font)

painter_cat = NPC(
    x=300, y=600,
    image_path=os.path.join("assets", "npcs", "painter_cat_tail.png"),
    dialogue_texts=[
        "你好，我是图书馆新来的画家猫咪。你在找胖团吗？我看到它往钟楼那边去了喵！",
        "你找到胖团留下的日记了！好棒喵~ 那你可以帮它找找小老鼠玩具吗？",
        "你完成任务啦喵！太棒了，继续游戏吧~"
    ],
    scene_index=0
)

mouse = Mouse(x=700, y=600, scene_index=2)

clock = pygame.time.Clock()
running = True
dialogue_triggered = False
show_quest_panel = True
task1_added = False
task2_added = False
task2_ready = False

minigame = MiniGame(WIDTH, HEIGHT, font)
minigame_active = False
minigame_hint_shown = False

diary_img = pygame.image.load(os.path.join("assets", "items", "diary.png")).convert_alpha()
diary_glow_alpha = 0
diary_glow_increase = True
diary_rect = diary_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

dialogue_timer = 0
mouse_hint_timer = 0
mouse_hint_shown = False

while running:
    if not minigame_active:
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        player.update(keys)
        painter_cat.update(map_manager.current_index)
        mouse.update(dt)

        if player.x > WIDTH:
            if map_manager.current_index < 2:
                map_manager.switch(map_manager.current_index + 1)
                player.x = 0
        elif player.x < 0:
            if map_manager.current_index > 0:
                map_manager.switch(map_manager.current_index - 1)
                player.x = WIDTH - 1

        quest1 = next((q for q in quest_manager.quests if q.title == "前往钟楼"), None)
        if map_manager.current_index == 1 and quest1 and quest1.status != "已完成":
            quest_manager.complete_quest("前往钟楼")

        quest1 = next((q for q in quest_manager.quests if q.title == "前往钟楼"), None)
        quest2 = next((q for q in quest_manager.quests if q.title == "寻找玩具小老鼠"), None)

        if task2_ready and not task2_added:
            dialogue.set_text(painter_cat.dialogue_texts[1])
            task2_added = True
            quest_manager.add_quest(Quest("寻找玩具小老鼠", "帮画家猫找玩具"))
            task2_ready = False
            dialogue_triggered = True

        if dialogue.visible and dialogue.current_text == "恭喜你找到了！":
            if pygame.time.get_ticks() - dialogue_timer > 2000:
                dialogue.visible = False
                dialogue_triggered = False

        if not dialogue.visible and map_manager.current_index == painter_cat.scene_index:
            dx = abs(player.x - painter_cat.x)
            dy = abs(player.y - painter_cat.y)
            if dx < 80 and dy < 80 and not dialogue_triggered:
                if not task1_added:
                    dialogue.set_text(painter_cat.dialogue_texts[0])
                    task1_added = True
                    quest_manager.add_quest(Quest("前往钟楼", "去钟楼找胖团的踪迹"))
                elif quest2 and quest2.status == "已完成":
                    dialogue.set_text(painter_cat.dialogue_texts[2])
                dialogue_triggered = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dialogue.visible:
                    dialogue.advance()
                    if not dialogue.visible:
                        dialogue_triggered = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (map_manager.current_index == 1 and
                    diary_rect.collidepoint(event.pos) and
                    quest1 and quest1.status == "已完成" and
                    not task2_added and
                    not minigame.completed):
                    minigame_active = True
                elif (map_manager.current_index == 2 and
                      mouse.rect.collidepoint(event.pos) and
                      quest2 and quest2.status != "已完成"):
                    quest_manager.complete_quest("寻找玩具小老鼠")
                    dialogue.set_text("恭喜你找到了！")
                    dialogue.visible = True
                    dialogue_triggered = True
                    dialogue_timer = pygame.time.get_ticks()
                    mouse_hint_timer = pygame.time.get_ticks()
                    mouse_hint_shown = True
                    mouse.found = True  # 让鼠标被点击后消失

        if dialogue.visible and map_manager.current_index == painter_cat.scene_index:
            dx = abs(player.x - painter_cat.x)
            dy = abs(player.y - painter_cat.y)
            if (dx ** 2 + dy ** 2) ** 0.5 > 80:
                dialogue.visible = False
                dialogue_triggered = False

        if map_manager.current_index == 1 and quest1 and quest1.status == "已完成" and not task2_added:
            if diary_glow_increase:
                diary_glow_alpha += 3
                if diary_glow_alpha >= 200:
                    diary_glow_increase = False
            else:
                diary_glow_alpha -= 3
                if diary_glow_alpha <= 50:
                    diary_glow_increase = True

        map_manager.draw(screen)
        if map_manager.current_index == painter_cat.scene_index:
            painter_cat.draw(screen, map_manager.current_index)
        if map_manager.current_index == mouse.scene_index:
            mouse.draw(screen)
        player.draw(screen)
        dialogue.draw(screen, HEIGHT)

        if map_manager.current_index == 1 and quest1 and quest1.status == "已完成" and not task2_added:
            glow_surface = diary_img.copy()
            glow_surface.set_alpha(diary_glow_alpha)
            screen.blit(glow_surface, diary_rect.topleft)

        if show_quest_panel:
            panel_width = 250
            panel_height = 150
            panel_x = WIDTH - panel_width - 10
            panel_y = 10
            pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height))
            pygame.draw.rect(screen, (0, 0, 0), (panel_x, panel_y, panel_width, panel_height), 2)

            title = font.render("任务日志（{}）".format(quest_manager.visible_filter), True, (0, 0, 0))
            screen.blit(title, (panel_x + 10, panel_y + 10))

            filtered_quests = quest_manager.get_filtered_quests()
            for i, quest in enumerate(filtered_quests):
                y = panel_y + 40 + i * 20
                if y < panel_y + panel_height - 10:
                    text = f"{quest.title} - {quest.status}"
                    screen.blit(font.render(text, True, (0, 0, 0)), (panel_x + 10, y))

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not minigame.completed:
                minigame.handle_event(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                minigame_active = False
                minigame_hint_shown = False
                if minigame.completed:
                    task2_ready = True
                    dialogue.set_text("恭喜你找到了！")
                    dialogue.visible = True
                    dialogue_triggered = True
                    dialogue_timer = pygame.time.get_ticks()

        screen.fill((200, 200, 200))
        minigame.draw(screen)
        if minigame.completed and not minigame_hint_shown:
            hint = font.render("再回图书馆看看吧", True, (100, 50, 50))
            screen.blit(hint, (WIDTH // 2 - 100, HEIGHT // 2 + 140))
            minigame_hint_shown = True

    pygame.display.flip()
    if minigame_active:
        clock.tick(60)

pygame.quit()
