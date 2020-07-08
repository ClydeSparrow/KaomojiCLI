import re
from typing import Iterable

from prompt_toolkit.completion import WordCompleter, CompleteEvent, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import CompleteStyle, prompt

from clipboard import copy2clip


class KaomojiCompleter(WordCompleter):

    KAOMOJI_SUB_REGEX = r'(\w+\s+)+'

    def __init__(self, kaomoji_list, *args, **kwargs):
        kwargs['sentence'] = True
        kwargs['ignore_case'] = True
        kwargs['match_middle'] = True

        super().__init__(kaomoji_list, *args, **kwargs)

    def get_kaomoji(self, text: str) -> str:
        return re.sub(self.KAOMOJI_SUB_REGEX, '', text)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        # Get list of words.
        words = self.words
        if callable(words):
            words = words()

        word_before_cursor = document.text_before_cursor

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word: str) -> bool:
            """ True when the word before the cursor matches. """
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return word_before_cursor in word
            else:
                return word.startswith(word_before_cursor)

        for a in words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, "")
                yield Completion(self.get_kaomoji(a), -len(word_before_cursor), display_meta=display_meta)


def main():
    words = []
    with open('kaomoji') as f:
        words.extend([line[:-1] for line in f.readlines()])
    kaomoji_completer = KaomojiCompleter(kaomoji_list=words)

    while True:
        try:
            text = prompt(
                "Give me idea: ",
                completer=kaomoji_completer,
                complete_style=CompleteStyle.MULTI_COLUMN,
            )
            copy2clip(text)
            print(f"{text}")
        except (KeyboardInterrupt, EOFError):
            print("Quitting...")
            break


if __name__ == "__main__":
    main()
