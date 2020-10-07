import re
import os

from typing import Iterable

from prompt_toolkit.completion import WordCompleter, CompleteEvent, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import CompleteStyle, prompt

from clipboard import copy2clip

DATA_FOLDER = 'data/'


class KaomojiCompleter(WordCompleter):
    KAOMOJI_SUB_REGEX = r'^(\w+\s+)+'

    def __init__(self, *args, **kwargs):
        super(KaomojiCompleter, self).__init__(*args, **kwargs)
        # `search_history` is a set of last used words
        # TODO: list should be replaced with something like queue of unique values
        # self.search_history = list()
        self.search_history = []
        self._words = kwargs.get('words') or []
        self.words = self.get_words_by_search_history

    @classmethod
    def get_kaomoji(cls, text: str) -> str:
        return re.sub(cls.KAOMOJI_SUB_REGEX, '', text)

    def get_words_by_search_history(self):
        """Returns words giving priority to search history"""
        return self.search_history + [w for w in self._words if w not in self.search_history]

    def update_search_history(self, kaomoji):
        word = next((w for w in self._words if kaomoji in w), None)
        if word is None:
            return None
        if word in self.search_history:
            self.search_history.remove(word)
        self.search_history.insert(0, word)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        # Get list of words.
        words = self.words
        if callable(words):
            words = words()

        word_before_cursor = document.text_before_cursor.lower()

        # TODO: If no words were found for search, return an error instead of copying input

        for a in words:
            if word_before_cursor in a.lower():
                display_meta = self.meta_dict.get(a, "")
                yield Completion(self.get_kaomoji(a), -len(word_before_cursor), display_meta=display_meta)


def main():
    words = []
    for file in os.listdir('data'):
        with open(os.path.join(DATA_FOLDER, file)) as f:
            for line in f.readlines():
                line = line.strip()
                kaomoji = KaomojiCompleter.get_kaomoji(line)
                if kaomoji not in line:
                    print(f"Skipping '{kaomoji}': Failed to correctly parse from '{line}'")
                    continue
                words.append(line)

    kaomoji_completer = KaomojiCompleter(words=words)

    while True:
        try:
            text = prompt(
                "Give me an idea: ",
                completer=kaomoji_completer,
                complete_style=CompleteStyle.MULTI_COLUMN,
            )
            kaomoji_completer.update_search_history(text)

            copy2clip(text)
            print(f"{text} copied to clipboard")
        except (KeyboardInterrupt, EOFError):
            print("Quitting...")
            break


if __name__ == "__main__":
    main()
