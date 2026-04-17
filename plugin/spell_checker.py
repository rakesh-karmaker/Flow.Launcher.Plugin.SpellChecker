# encoding=utf8
from flowlauncher import FlowLauncher
from spellchecker import SpellChecker
import pyperclip
import wikipedia
import warnings

try:
    from bs4 import GuessedAtParserWarning
except Exception:
    GuessedAtParserWarning = None

if GuessedAtParserWarning is not None:
    # Prevent wikipedia->BeautifulSoup parser warnings from being printed to stderr.
    # Flow Launcher treats stderr output as plugin execution failure.
    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

spell = SpellChecker(language='en')
    
class Main(FlowLauncher):
    IMG_SUCCESS = "success"
    IMG_FAILURE = "failure"
    IMG_SUGGESTION = "suggestion"
    IMG_ICON = "icon"
    ADD_DEFINITION = False
    MEANING_FINDER = 'default'
    WORDNET_NOT_FOUND_TAG = "--not-installed--"
    NO_DEFINITION_TAG = "--no-definition--"

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

    def tryToParseValueAsText(self, text: str):
        if text.strip() == "":
            return (False, text)
        return (True, text)
    
    def getDefinitionFromWordNet(self, text: str) -> str:
        try:
            from nltk.corpus import wordnet
            
            synsets = wordnet.synsets(text.lower(), lang='eng')
            if synsets:
                return str(synsets[0].definition()).capitalize()
            
            return self.NO_DEFINITION_TAG
        except LookupError:
            return self.WORDNET_NOT_FOUND_TAG
        

    def getDefinition(self, text: str):
        if not self.ADD_DEFINITION:
            return ""
        try:
            if self.MEANING_FINDER == 'wikipedia':
                summary = wikipedia.summary(text, sentences=1)
                return summary if summary else "No definition found"
            
            wordnet_definition = self.getDefinitionFromWordNet(text)
            if wordnet_definition == self.WORDNET_NOT_FOUND_TAG or wordnet_definition == self.NO_DEFINITION_TAG:
                wordnet_error_note = " (WordNet is not installed thus the definition may be slow. Run: python -m nltk.downloader wordnet)" if wordnet_definition == self.WORDNET_NOT_FOUND_TAG else ""
                wikipedia_definition = wikipedia.summary(text, sentences=1)
                if wikipedia_definition:
                    return f"{wikipedia_definition}{wordnet_error_note}"
                else:
                    return f"No definition found{wordnet_error_note}"
            return wordnet_definition
        
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple definitions found for '{text}': {', '.join(e.options[:5])}..."
        except:
            return "No definition found"
    
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
                suggestions.remove(correct_spelling) if correct_spelling in suggestions else None
                self.addMessage(
                    f"Did you mean '{correct_spelling}'? {f'({', '.join(suggestions)})' if suggestions else ''}".strip(),
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
        self.messages = []
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
                match value.lower():
                    case "-d":
                        self.ADD_DEFINITION = not self.ADD_DEFINITION
                        continue
                    case "-dw":
                        self.ADD_DEFINITION = not self.ADD_DEFINITION
                        self.MEANING_FINDER = 'wikipedia' if self.MEANING_FINDER == 'default' else 'default'
                        continue
                    case _:
                        self.checkSpelling(value)
            else:
                self.addMessage(
                    "Error:  {}  is not an text!".format(value),
                    "Please provide a valid text to check the spelling for.",
                    self.IMG_FAILURE
                )

        return self.messages
    
    def copyToClipboard(self, text: str):
        pyperclip.copy(text)