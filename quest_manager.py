class Quest:
    def __init__(self, title, description, status="进行中"):
        self.title = title
        self.description = description
        self.status = status  # "进行中" 或 "已完成"

class QuestManager:
    def __init__(self):
        self.quests = []
        self.visible_filter = "全部"

    def add_quest(self, quest):
        self.quests.append(quest)

    def complete_quest(self, title):
        for q in self.quests:
            if q.title == title:
                q.status = "已完成"

    def get_quest(self, title):
        for q in self.quests:
            if q.title == title:
                return q
        return None

    def get_filtered_quests(self):
        if self.visible_filter == "全部":
            return self.quests
        return [q for q in self.quests if q.status == self.visible_filter]

    def toggle_filter(self):
        options = ["全部", "进行中", "已完成"]
        current = options.index(self.visible_filter)
        self.visible_filter = options[(current + 1) % len(options)]
