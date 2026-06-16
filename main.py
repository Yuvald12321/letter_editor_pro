import importlib.util
import json
import sys
from pathlib import Path
import customtkinter as ctk
import requests
from customtkinter import filedialog


def get_path(name):
    if getattr(sys, "frozen", False):
        path = Path(sys.executable).resolve().parent / name
    else:
        path = Path(__file__).resolve().parent / name
    return path


def get_code():
    path = get_path("code.py")
    if not path.exists():
        url = "https://raw.githubusercontent.com/Yuvald12321/letter_editor/refs/heads/master/main.py"
        code = requests.get(url).content
        path.write_bytes(code)
    spec = importlib.util.spec_from_file_location("dynamic_code", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LetterEditor


class LetterEditorPro(get_code()):
    def __init__(self):
        self.find_and_apply_theme()
        super().__init__()

        self.title("Letter Editor Pro")

        self.bottom_bar = ctk.CTkFrame(self)

        self.topmost_toggle = ctk.CTkSwitch(self.bottom_bar, text="Top lock", command=lambda: self.wm_attributes("-topmost", self.topmost_toggle.get()))
        self.topmost_toggle.pack(side="left", padx=5, pady=5)

        self.more_options_button = ctk.CTkButton(self.bottom_bar, text="More options", width=100, command=self.setup_more_options)
        self.more_options_button.pack(side="right", padx=5, pady=5)

        self.tasks_button = ctk.CTkButton(self.bottom_bar, text="Tasks", width=100, command=self.setup_tasks)
        self.tasks_button.pack(side="right", padx=5, pady=5)

        self.bottom_bar.grid(column=0, row=2, sticky="ew", padx=10, pady=(0, 10))

    def setup_more_options(self):
        self.more_options_button.configure(state="disabled")

        self.more_options_frame = ctk.CTkFrame(self)

        self.more_options_label = ctk.CTkLabel(self.more_options_frame, text="More options")
        self.more_options_label.pack(fill="x", padx=5, pady=5)

        self.more_options_close_button = ctk.CTkButton(self.more_options_label, text="❌", fg_color="transparent", hover_color="red", width=0, command=self.close_more_options)
        self.more_options_close_button.grid(column=1, row=0)

        self.update_button = ctk.CTkButton(self.more_options_frame, text="update", command=self.update)
        self.update_button.pack(padx=5, pady=(0, 5))

        self.apply_theme_button = ctk.CTkButton(self.more_options_frame, text="apply theme", command=self.load_new_theme)
        self.apply_theme_button.pack(padx=5, pady=(0, 5))

        self.delete_theme_button = ctk.CTkButton(self.more_options_frame, text="remove theme", command=self.delete_theme)
        self.delete_theme_button.pack(padx=5, pady=(0, 5))

        self.delete_tasks_button = ctk.CTkButton(self.more_options_frame, text="delete all tasks", command=self.delete_tasks)
        self.delete_tasks_button.pack(padx=5, pady=(0, 5))

        self.more_options_frame.grid(column=1, row=0, rowspan=3, sticky="nsew", padx=(0, 10), pady=10)

    def close_more_options(self):
        self.more_options_button.configure(state="normal")
        self.more_options_frame.destroy()

    def update(self):
        path = get_path("code.py")
        path.unlink(missing_ok=True)
        self.destroy()

    def find_and_apply_theme(self):
        path = get_path("theme.json")
        if path.exists():
            ctk.set_default_color_theme(str(path))

    def load_new_theme(self):
        path = get_path("theme.json")
        org = filedialog.askopenfilename(filetypes=[("Theme File", "*.json")])
        if org:
            org = Path(org).resolve()
            if org.exists():
                theme = json.loads(org.read_text())
                path.write_text(json.dumps(theme, indent=4))
                self.destroy()

    def delete_theme(self):
        get_path("theme.json").unlink(missing_ok=True)

    def setup_tasks(self):
        self.tasks_button.configure(state="disabled")

        self.tasks_path = get_path("tasks.json")
        if not self.tasks_path.exists():
            self.tasks_path.write_text("{}")

        self.tasks = json.loads(self.tasks_path.read_text())

        self.tasks_window = ctk.CTkToplevel(self)
        self.tasks_window.title("Tasks")
        self.tasks_window.geometry("300x400")
        self.tasks_window.wm_attributes("-topmost", True)
        self.tasks_window.protocol("WM_DELETE_WINDOW", self.close_tasks)

        self.tasks_label = ctk.CTkLabel(self.tasks_window, text="Tasks")
        self.tasks_label.pack(side="top")

        self.tasks_frame = ctk.CTkScrollableFrame(self.tasks_window)
        self.tasks_frame.pack(fill="both", expand=True, padx=5)

        self.add_task_frame = ctk.CTkFrame(self.tasks_window)

        self.add_task_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="Enter task")
        self.add_task_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.add_task_entry.bind("<Return>", lambda _: self.add_task(self.add_task_entry.get()))

        self.add_task_button = ctk.CTkButton(self.add_task_frame, text="Add", width=1, command=lambda: self.add_task(self.add_task_entry.get()))
        self.add_task_button.pack(side="right", padx=(0, 5), pady=5)

        self.add_task_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        self.update_tasks()

    def close_tasks(self):
        self.tasks_button.configure(state="normal")
        self.tasks_window.destroy()

    def save_tasks(self):
        self.tasks_path.write_text(json.dumps(self.tasks, indent=4))

    def update_tasks(self):
        for child in self.tasks_frame.winfo_children():
            child.destroy()
        for n, (task, is_completed) in enumerate(self.tasks.items()):
            ctk.CTkButton(self.tasks_frame, text="⨉", fg_color="transparent", width=0, command=lambda t=task: self.remove_task(t)).grid(row=n, column=0, sticky="w", padx=5, pady=5)
            checkbox = ctk.CTkCheckBox(self.tasks_frame, text=task)
            checkbox.grid(column=1, row=n, sticky="w", padx=0, pady=5)
            if is_completed:
                checkbox.select()
            checkbox.configure(command=lambda c=checkbox, t=task: self.toggle_task(c, t))

    def toggle_task(self, checkbox, task):
        self.tasks[task] = bool(checkbox.get())
        self.save_tasks()

    def add_task(self, task):
        if task and task not in self.tasks:
            self.tasks[task] = False
            self.save_tasks()
            self.add_task_entry.delete(0, "end")
            self.update_tasks()

    def remove_task(self, task):
        if task in self.tasks:
            del self.tasks[task]
            self.save_tasks()
            self.update_tasks()

    def delete_tasks(self):
        get_path("tasks.json").unlink(missing_ok=True)


if __name__ == "__main__":
    editor = LetterEditorPro()
    editor.mainloop()