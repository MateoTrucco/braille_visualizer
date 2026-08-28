"""Educational desktop six-dot Braille-cell visualizer."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from braille import render_board, translate
from ui_theme import apply_theme, text_style


class BrailleApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Six-dot Braille Visualizer")
        self.root.geometry("850x620")
        self.root.minsize(650, 500)
        self.colors = apply_theme(root, "#0284c7")
        style = ttk.Style(root)
        style.configure("Hint.TLabel", font=("Segoe UI", 10), foreground=self.colors["muted"])

        container = ttk.Frame(root, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(5, weight=1)

        ttk.Label(container, text="Text to six-dot cells", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            container,
            text="Supports letters, Spanish accented characters, capitals, numbers and common punctuation.",
            style="Hint.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, 12))

        self.input_text = tk.Text(container, height=4, wrap="word", font=("Segoe UI", 12))
        self.input_text.grid(row=2, column=0, sticky="ew")
        self.input_text.insert("1.0", "Hola Mateo 2026")
        text_style(self.input_text, self.colors)

        button_row = ttk.Frame(container)
        button_row.grid(row=3, column=0, sticky="ew", pady=10)
        ttk.Button(button_row, text="Translate", style="Accent.TButton", command=self.update_translation).pack(side="left")
        ttk.Button(button_row, text="Copy Unicode", command=self.copy_unicode).pack(side="left", padx=8)
        ttk.Button(button_row, text="Clear", command=self.clear).pack(side="left")

        self.unicode_var = tk.StringVar()
        unicode_frame = ttk.LabelFrame(container, text="Unicode Braille", padding=10)
        unicode_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        ttk.Entry(
            unicode_frame,
            textvariable=self.unicode_var,
            state="readonly",
            font=("Segoe UI Symbol", 18),
        ).pack(fill="x")

        board_frame = ttk.LabelFrame(container, text="Dot view", padding=10)
        board_frame.grid(row=5, column=0, sticky="nsew")
        board_frame.columnconfigure(0, weight=1)
        board_frame.rowconfigure(0, weight=1)
        self.board = tk.Text(
            board_frame,
            wrap="none",
            font=("Consolas", 12),
            state="disabled",
            padx=10,
            pady=10,
        )
        self.board.grid(row=0, column=0, sticky="nsew")
        text_style(self.board, self.colors, readonly=True)
        scrollbar = ttk.Scrollbar(board_frame, orient="vertical", command=self.board.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.board.configure(yscrollcommand=scrollbar.set)

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(container, textvariable=self.status_var).grid(row=6, column=0, sticky="w", pady=(8, 0))

        self.input_text.bind("<Control-Return>", lambda _event: self.update_translation())
        self.root.bind("<Configure>", self._resize_board)
        self.update_translation()

    def _cells_per_line(self) -> int:
        width = max(self.root.winfo_width(), 650)
        return max(4, min(18, (width - 120) // 70))

    def _resize_board(self, _event=None) -> None:
        self.root.after_idle(self.update_translation)

    def update_translation(self) -> None:
        text = self.input_text.get("1.0", "end-1c")
        result = translate(text)
        self.unicode_var.set(result.unicode_text)
        board_text = render_board(result, self._cells_per_line())
        self.board.configure(state="normal")
        self.board.delete("1.0", "end")
        self.board.insert("1.0", board_text)
        self.board.configure(state="disabled")
        if result.unknown_characters:
            unknown = " ".join(repr(char) for char in result.unknown_characters)
            self.status_var.set(f"Unknown characters shown as a full cell: {unknown}")
        else:
            self.status_var.set(f"{len(result.cells)} cells generated.")

    def copy_unicode(self) -> None:
        value = self.unicode_var.get()
        if not value:
            messagebox.showinfo("Nothing to copy", "Translate some text first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.status_var.set("Unicode cells copied to the clipboard.")

    def clear(self) -> None:
        self.input_text.delete("1.0", "end")
        self.update_translation()
        self.input_text.focus_set()


def main() -> None:
    root = tk.Tk()
    BrailleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
