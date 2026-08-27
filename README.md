# Six-dot Braille Visualizer

An educational desktop visualizer with Unicode Braille cells and a six-dot view. It is not a certified transcription tool; punctuation and language conventions should be verified for any formal use.

## Features

- Capital and number indicators
- Spanish letters and common punctuation
- Unknown-character reporting
- Clipboard export
- Resize-aware visual board
- Unit-tested conversion logic

## Run

```bash
python main.py
```

## Test

```bash
python -m pytest tests
```

---

## Live demo

**[Open the live demo](https://mateotrucco.github.io/braille_visualizer/)**

The demo runs the repository’s original Python logic directly in the browser with Pyodide 314.0.4. The desktop Tkinter interface remains available through `main.py`.

## Repository setup

This separated repository also includes:

- MIT license
- project-specific `.gitignore`
- automated tests / CI
- GitHub Pages deployment for the demo
- `screenshots/` placeholder for portfolio images

The source files from the cleaned portfolio base were preserved unless a web-demo integration file had to be added.

