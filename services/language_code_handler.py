

GOOGLE_LANGUAGES = ['af', 'ar', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'en-au', 'en-uk', 'en-us', 'eo', 'es', 'es-es', 'es-us', 'fi', 'fr', 'hi', 'hr', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'nl', 'no', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sk', 'sq', 'sr', 'sv', 'sw', 'ta', 'th', 'tr', 'vi', 'zh', 'zh-cn', 'zh-tw', 'zh-yue']

DEEPL_LANGUAGES = ['BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'EN-US', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT-BR', 'PT-PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH']

SPECIAL_CODES = [
["EN-GB", "en-uk"],
["ZH", "zh-cn"]]



class CodeValidator():
    def __init__(self, language_code):
        self.language_code = language_code        

    def deepl_to_google(self):
        # check if the lowercase language code is in the other list            
        if self.language_code.lower() in GOOGLE_LANGUAGES:
            return self.language_code.lower()
        elif self.language_code.lower() == "zh":
            return "zh-cn"
        elif self.language_code.lower() == "en-gb":
            return "en-uk"
    
    def google_to_deepl(self):
        # check if the lowercase language code is in the other list            
        if self.language_code.upper() in DEEPL_LANGUAGES:
            return self.language_code.upper()
        # else try with the first 2 letters
        elif self.language_code.upper()[0:2] in DEEPL_LANGUAGES:
            return self.language_code.upper()[0:2]
        elif self.language_code == "en-uk":
            return "EN-GB"