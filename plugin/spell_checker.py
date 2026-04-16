# encoding=utf8
from flowlauncher import FlowLauncher
from spellchecker import SpellChecker
import pyperclip

spell = SpellChecker(language='en')
    
class Main(FlowLauncher):
    MSG_NO_SUGGESTION = "No suggestions found for '{}'."
    IMG_SUCCESS = "success"
    IMG_FAILURE = "failure"
    IMG_SUGGESTION = "suggestion"
    IMG_ICON = "icon"
    ADD_DEFINITION = False

    messages = []

    def addMessage(self, title: str, subtitle: str, image: str, copyText: str = None):
        self.messages.append({
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": "assets/{}.png".format(image),
            "JsonRPCAction": {
                "method": "copyToClipboard",
                "parameters": [copyText if copyText is not None else ""]
            }
        })

    def copyToClipboard(self, text: str):
        pyperclip.copy(text)

    def tryToParseValueAsText(self, text: str):
        if text.strip() == "":
            return (False, text)
        return (True, text)
    
    def getDefinition(self, text: str):
        if not self.ADD_DEFINITION:
            return ""
        try:
            from nltk.corpus import wordnet

            synsets = wordnet.synsets(text.lower(), lang='eng')
            if synsets:
                return str(synsets[0].definition()).capitalize()

            return "No definition found"
        except LookupError:
            return "WordNet is not installed. Run: python -m nltk.downloader wordnet"
        except Exception:
            return "Error fetching definition. Please download the WordNet data using python -m nltk.downloader wordnet"
    
    def checkSpelling(self, text: str):
        misspelled = spell.unknown([text])
        if len(misspelled) == 0:
            self.addMessage(
                f"'{text}' is spelled correctly.",
                self.getDefinition(text),
                self.IMG_SUCCESS,
                text
            )
        else:
            suggestions = spell.candidates(text)
            correct_spelling = spell.correction(text)
        
            if suggestions and len(suggestions) > 0:
                self.addMessage(
                    f"Did you mean '{correct_spelling}'? ({', '.join(suggestions)})",
                    f'{correct_spelling}: {self.getDefinition(correct_spelling)}' if self.ADD_DEFINITION else "",
                    self.IMG_SUGGESTION,
                    correct_spelling
                )
            else:
                self.addMessage(
                    f"'{text}' is misspelled and no suggestions available.",
                    "",
                    self.IMG_FAILURE
                )

    def query(self, query):
        words = query.strip()
        if len(words) == 0:
            return [
                {
                    "Title": "Please enter a word to check its spelling.",
                    "SubTitle": "You can also toggle definitions with '-d'.",
                    "IcoPath": "assets/{}.png".format(self.IMG_ICON)
                }
            ]

        for word in words.split(" "):
            isText, value = self.tryToParseValueAsText(word)

            if isText:
                if value.lower() == "-d":
                    self.ADD_DEFINITION = not self.ADD_DEFINITION
                    continue

                self.checkSpelling(value)
            else:
                self.addMessage(
                    "Error:  {}  is not an text!".format(value),
                    "Please provide a valid text to check the spelling for.",
                    self.IMG_FAILURE
                )

        return self.messages