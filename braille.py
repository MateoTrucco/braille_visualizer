"""Educational text-to-six-dot-cell utilities.

This project is a visual learning tool, not a certified Braille transcriber.
It preserves unknown characters as a visible replacement cell and reports them
to the caller instead of silently treating them as supported.
"""

from __future__ import annotations

from dataclasses import dataclass

Dots = tuple[int, ...]

LETTER_DOTS: dict[str, Dots] = {
    "a": (1,), "b": (1, 2), "c": (1, 4), "d": (1, 4, 5), "e": (1, 5),
    "f": (1, 2, 4), "g": (1, 2, 4, 5), "h": (1, 2, 5), "i": (2, 4),
    "j": (2, 4, 5), "k": (1, 3), "l": (1, 2, 3), "m": (1, 3, 4),
    "n": (1, 3, 4, 5), "o": (1, 3, 5), "p": (1, 2, 3, 4),
    "q": (1, 2, 3, 4, 5), "r": (1, 2, 3, 5), "s": (2, 3, 4),
    "t": (2, 3, 4, 5), "u": (1, 3, 6), "v": (1, 2, 3, 6),
    "w": (2, 4, 5, 6), "x": (1, 3, 4, 6), "y": (1, 3, 4, 5, 6),
    "z": (1, 3, 5, 6),
    "ñ": (1, 2, 4, 5, 6),
    "á": (1, 2, 3, 5, 6), "é": (2, 3, 4, 6), "í": (3, 4),
    "ó": (3, 4, 6), "ú": (2, 3, 4, 5, 6), "ü": (1, 2, 5, 6),
}

PUNCTUATION_DOTS: dict[str, Dots] = {
    " ": (), ",": (2,), ";": (2, 3), ":": (2, 5), ".": (2, 5, 6),
    "?": (2, 3, 6), "¿": (2, 3, 6), "!": (2, 3, 5), "¡": (2, 3, 5),
    "\"": (2, 3, 6), "'": (3,), "-": (3, 6), "(": (1, 2, 6), ")": (3, 4, 5),
    "/": (3, 4), "*": (3, 5),
}

CAPITAL_SIGN: Dots = (6,)
NUMBER_SIGN: Dots = (3, 4, 5, 6)
UNKNOWN_SIGN: Dots = (1, 2, 3, 4, 5, 6)
DIGIT_TO_LETTER = {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e",
                   "6": "f", "7": "g", "8": "h", "9": "i", "0": "j"}


@dataclass(frozen=True)
class BrailleCell:
    source: str
    dots: Dots
    kind: str = "character"

    @property
    def unicode(self) -> str:
        value = sum(1 << (dot - 1) for dot in self.dots)
        return chr(0x2800 + value)


@dataclass(frozen=True)
class Translation:
    cells: tuple[BrailleCell, ...]
    unknown_characters: tuple[str, ...] = ()

    @property
    def unicode_text(self) -> str:
        return "".join(cell.unicode for cell in self.cells)


def translate(text: str) -> Translation:
    cells: list[BrailleCell] = []
    unknown: list[str] = []
    in_number = False

    for character in text:
        if character.isdigit():
            if not in_number:
                cells.append(BrailleCell("#", NUMBER_SIGN, "number-sign"))
                in_number = True
            cells.append(BrailleCell(character, LETTER_DOTS[DIGIT_TO_LETTER[character]], "digit"))
            continue

        in_number = False
        lower = character.lower()
        if lower in LETTER_DOTS:
            if character.isupper():
                cells.append(BrailleCell("⇧", CAPITAL_SIGN, "capital-sign"))
            cells.append(BrailleCell(character, LETTER_DOTS[lower]))
        elif character in PUNCTUATION_DOTS:
            cells.append(BrailleCell(character, PUNCTUATION_DOTS[character]))
        elif character in {"\n", "\t"}:
            cells.append(BrailleCell(" ", (), "space"))
        else:
            cells.append(BrailleCell(character, UNKNOWN_SIGN, "unknown"))
            if character not in unknown:
                unknown.append(character)

    return Translation(tuple(cells), tuple(unknown))


def dot_rows(cell: BrailleCell, on: str = "●", off: str = "○") -> tuple[str, str, str]:
    active = set(cell.dots)
    return (
        f"{on if 1 in active else off} {on if 4 in active else off}",
        f"{on if 2 in active else off} {on if 5 in active else off}",
        f"{on if 3 in active else off} {on if 6 in active else off}",
    )


def render_board(translation: Translation, cells_per_line: int = 12) -> str:
    if cells_per_line <= 0:
        raise ValueError("cells_per_line must be positive")
    if not translation.cells:
        return ""

    sections: list[str] = []
    for start in range(0, len(translation.cells), cells_per_line):
        chunk = translation.cells[start : start + cells_per_line]
        rows = [[], [], [], []]
        for cell in chunk:
            visual = dot_rows(cell)
            rows[0].append(visual[0])
            rows[1].append(visual[1])
            rows[2].append(visual[2])
            label = cell.source if cell.source.strip() else "␠"
            rows[3].append(label[:3].center(3))
        sections.append("\n".join("   ".join(row) for row in rows))
    return "\n\n".join(sections)
