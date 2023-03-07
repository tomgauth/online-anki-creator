

# a block is a single unit of a lesson. It's made of:
# - a phrase in language 1
# - a phrase in language 2
# - possibly an explanation of the phrase in language 1

class Block:
    def __init__(self, phrase_1, phrase_2, explanation, explanation_language):
        self.phrase_1 = phrase_1
        self.phrase_2 = phrase_2
        self.explanation = explanation
        self.explanation_language = explanation_language
    
    @classmethod
    def from_json(cls, json_block):
        return cls(json_block['phrase_1'], json_block['phrase_2'], json_block['explanation'], json_block['explanation_language'])        

 