

# a block is a single unit of a lesson. It's made of:
# - a phrase in language 1
# - a phrase in language 2
# - possibly an explanation of the phrase in language 1

class Block:
    def __init__(self, phrase_1, phrase_2, origin_language, target_language, explanation=""):
        self.phrase_1 = phrase_1
        self.phrase_2 = phrase_2
        self.origin_language = origin_language
        self.target_language = target_language
        self.explanation = explanation
        self.explanation_language = origin_language
    
    @classmethod
    def from_json(cls, json_block):
        return cls(
            json_block["phrase_1"],
            json_block["phrase_2"],
            json_block["origin_language"],
            json_block["target_language"],
            json_block["explanation"],
            json_block["explanation_language"],
        )

 