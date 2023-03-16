from models.block import Block


class Lesson:
    def __init__(self, lesson_name, origin_language, target_language, content, intro, outro, separator=";"):
        self.lesson_name = lesson_name
        self.origin_language = origin_language
        self.target_language = target_language
        self.content = content        
        self.intro = intro
        self.outro = outro
        self.separator = separator
        self.blocks = None    
    
    def generate_blocks(self):
        blocks = []
        # split the content into blocks. Each line is a block, first is the phrase in the origin language, second is the phrase in the target language
        for line in self.content.splitlines():
            phrases = line.split(self.separator)
            if len(phrases) == 2:
                phrase_1 = phrases[0].strip()
                phrase_2 = phrases[1].strip()
                block = Block(phrase_1, phrase_2, self.origin_language, self.target_language)
                blocks.append(block)
            if len(phrases) == 3:
                phrase_1 = phrases[0].strip()
                phrase_2 = phrases[1].strip()
                explanation = phrases[2].strip()
                block = Block(phrase_1, phrase_2, self.origin_language, self.target_language, explanation)
                blocks.append(block)
        self.blocks = blocks
        return blocks
    


def test():
    # create a lesson and generate the blocks
    lesson = Lesson(
        lesson_name="test one",
        origin_language="EN-US",
        target_language="FR",
        content="Hello;Bonjour\nHow are you?;Comment allez-vous?\nGoodbye;Au revoir\nsalut;hello; this is also a way to say goodbye""",
        intro="Intro to lesson one",
        outro="Outro to lesson one",
    )
    blocks = lesson.generate_blocks(lesson.content, lesson.origin_language, lesson.target_language)
    print(blocks)
    print(blocks[0].phrase_1)
    print(blocks[0].phrase_2)
    print(blocks[0].explanation)
    print(blocks[3].phrase_1)
    print(blocks[3].explanation)
    return lesson

