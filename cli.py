import re
from typing import Iterable

from prompt_toolkit.completion import WordCompleter, CompleteEvent, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import CompleteStyle, prompt

from clipboard import copy2clip


class KaomojiCompleter(WordCompleter):
    KAOMOJI_SUB_REGEX = r'(\w+\s+)+'

    def get_kaomoji(self, text: str) -> str:
        return re.sub(self.KAOMOJI_SUB_REGEX, '', text)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        # Get list of words.
        words = self.words
        if callable(words):
            words = words()

        word_before_cursor = document.text_before_cursor.lower()

        def word_matches(word: str) -> bool:
            """ True when the word before the cursor matches. """
            return word_before_cursor in word.lower()

        for a in words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, "")
                yield Completion(self.get_kaomoji(a), -len(word_before_cursor), display_meta=display_meta)


def main():
    words = []
    with open('data/kaomoji') as f:
        words.extend([line[:-1] for line in f.readlines()])
    kaomoji_completer = KaomojiCompleter(words=words)

    while True:
        try:
            text = prompt(
                "Give me an idea: ",
                completer=kaomoji_completer,
                complete_style=CompleteStyle.MULTI_COLUMN,
            )
            copy2clip(text)
            print(f"{text} copied to clipboard")
        except (KeyboardInterrupt, EOFError):
            print("Quitting...")
            break


if __name__ == "__main__":
    main()
