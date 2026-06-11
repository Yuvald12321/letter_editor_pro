import sys
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk
import requests


def get_code():
    if getattr(sys, "frozen", False):
        path = Path(sys.executable).resolve().parent / "code"
    else:
        path = Path(__file__).resolve().parent / "code"
    if not path.exists():
        url = "https://raw.githubusercontent.com/Yuvald12321/letter_editor/refs/heads/master/main.py"
        code = requests.get(url).content
        path.write_bytes(code)
    else:
        code = path.read_bytes()
    namespace = {"sys": sys, "Path": Path, "filedialog": filedialog, "ctk": ctk}
    exec(code, namespace)
    return namespace["LetterEditor"]


class LetterEditorPro(get_code()):
    def __init__(self):
        super().__init__()
        self.title("Letter Editor Pro")

        self.bottom_bar = ctk.CTkFrame(self)

        topmost_toggle = ctk.CTkSwitch(self.bottom_bar, text="Top Lock", onvalue=1, offvalue=0, command=lambda: self.wm_attributes("-topmost", topmost_toggle.get()))
        topmost_toggle.pack(side="left", padx=5, pady=5)

        update_button = ctk.CTkButton(self.bottom_bar, text="Update", width=100, command=self.update)
        update_button.pack(side="right", padx=5, pady=5)

        self.bottom_bar.pack(fill="x", padx=10, pady=(0, 10))

    def update(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "code"
        else:
            path = Path(__file__).resolve().parent / "code"
        path.unlink(missing_ok=True)
        self.destroy()


if __name__ == "__main__":
    ctk.set_default_color_theme("green")
    editor = LetterEditorPro()
    editor.mainloop()