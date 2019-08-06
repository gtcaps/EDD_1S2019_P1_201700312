from Classes.Player import Player

class QueueNode:

    def __init__(self, new_player=Player() ,next=None):
        self.new_player = new_player
        self.next = next

    def get_player(self):
        return self.new_player

    def get_next(self):
        return self.next

    def set_player(self, name):
        self.new_player.set_name(name)

    def set_score(self, score):
        self.new_player.set_score(score)


