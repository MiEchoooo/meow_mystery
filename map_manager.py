import pygame

class MapManager:
    def __init__(self, width, height):
        self.maps = {
            "library": {"file": "assets/maps/cat_library2.jpg", "color": (245, 245, 220)},
            "clocktower": {"file": "assets/maps/clocktower.png", "color": (210, 240, 255)},
            "sewer": {"file": "assets/maps/garden.png", "color": (180, 200, 170)},
        }
        self.map_keys = list(self.maps.keys())
        self.current_index = 0
        self.width = width
        self.height = height
        self.surface = self.load_map(self.map_keys[self.current_index])

    def load_map(self, name):
        try:
            return pygame.image.load(self.maps[name]["file"]).convert()
        except:
            surf = pygame.Surface((self.width, self.height))
            surf.fill(self.maps[name]["color"])
            return surf

    def switch(self, index):
        self.current_index = index
        name = self.map_keys[index]
        self.surface = self.load_map(name)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def get_current_name(self):
        return self.map_keys[self.current_index].capitalize()
