


# a controller that takes a lesson and parameters and generates an audio file with the lesson
class AudioLessonGenerator():
    # takes a list of audio blocks and parameters and generates an audio file with the lesson
    def __init__(self, blocks: list, **params: dict):
        self.blocks = blocks
        self.params = params


# takes a phrase and parameters and generates an audio block
class AudioBlockGenerator():
    def __init__(self, block, **params: dict):
        self.block = block
        self.params = params

    def generate(self):
        # generates an audio block
        pass
