import sys
from pathlib import Path
import customtkinter as ctk
from customtkinter import filedialog
import requests
import json


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
        self.find_and_apply_theme()
        super().__init__()
        self.title("Letter Editor Pro")

        self.bottom_bar = ctk.CTkFrame(self)

        self.topmost_toggle = ctk.CTkSwitch(self.bottom_bar, text="Top Lock", onvalue=True, offvalue=False, command=lambda: self.wm_attributes("-topmost", topmost_toggle.get()))
        self.topmost_toggle.pack(side="left", padx=5, pady=5)

        self.update_button = ctk.CTkButton(self.bottom_bar, text="Update", width=100, command=self.update)
        self.update_button.pack(side="right", padx=5, pady=5)

        self.apply_theme_button = ctk.CTkButton(self.bottom_bar, text="Apply Theme", width=100, command=self.apply_theme)
        self.apply_theme_button.pack(side="right", padx=5, pady=5)

        self.bottom_bar.pack(fill="x", padx=10, pady=(0, 10))

    def update(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "code"
        else:
            path = Path(__file__).resolve().parent / "code"
        path.unlink(missing_ok=True)
        self.destroy()

    def find_and_apply_theme(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "theme.json"
        else:
            path = Path(__file__).resolve().parent / "theme.json"
        if path.exists():
            ctk.set_default_color_theme(str(path))

    def apply_theme(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "theme.json"
        else:
            path = Path(__file__).resolve().parent / "theme.json"
        org = filedialog.askopenfilename(title="Open File", filetypes=[("Theme File", "*.json")])
        if org:
            org = Path(org).resolve()
            if org.exists():
                theme = json.loads(org.read_text())
                path.write_text(json.dumps(theme, indent=4))
                self.destroy()


if __name__ == "__main__":
    editor = LetterEditorPro()
    editor.mainloop()