from braille import CAPITAL_SIGN, NUMBER_SIGN, dot_rows, render_board, translate


def test_lowercase_letter():
    result = translate("a")
    assert result.cells[0].dots == (1,)
    assert result.unicode_text == "⠁"


def test_capital_adds_capital_sign():
    result = translate("A")
    assert result.cells[0].dots == CAPITAL_SIGN
    assert result.cells[1].dots == (1,)
    assert result.unicode_text == "⠠⠁"


def test_number_sign_is_added_once_per_number_run():
    result = translate("12 3")
    assert [cell.dots for cell in result.cells].count(NUMBER_SIGN) == 2
    assert result.unicode_text == "⠼⠁⠃⠀⠼⠉"


def test_unknown_character_is_reported():
    result = translate("a@")
    assert result.unknown_characters == ("@",)
    assert result.cells[-1].kind == "unknown"


def test_dot_rows_are_six_dot_layout():
    assert dot_rows(translate("a").cells[0]) == ("● ○", "○ ○", "○ ○")


def test_render_board_rejects_invalid_width():
    try:
        render_board(translate("a"), 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
