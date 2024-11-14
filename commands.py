class Command:
    def __init__(self, player):
        self.player = player

class PlayCommand(Command):
    def __call__(self):
        self.player.play_track_with_speed()

class StopCommand(Command):
    def __call__(self):
        self.player.stop_track()

class PauseCommand(Command):
    def __call__(self):
        self.player.toggle_pause()

class NextCommand(Command):
    def __call__(self):
        self.player.next_track()

class PreviousCommand(Command):
    def __call__(self):
        self.player.prev_track()