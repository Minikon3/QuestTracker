import tkinter as tk
import os


class QuestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest Tracker")

        self.quest_data = self.load_quest_data()
        self.completed_levels = self.load_completed_levels()

        self.create_interface()

    def load_quest_data(self):
        quest_data = {}
        with open('quests.txt', 'r') as file:
            lines = file.readlines()
            current_difficulty = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line == 'Normal' or line == 'Hard':
                    current_difficulty = line
                    quest_data[current_difficulty] = []
                else:
                    level, moves = line.split()
                    quest_data[current_difficulty].append((level, int(moves)))
        return quest_data

    def load_completed_levels(self):
        completed_levels = set()
        try:
            with open('completed_levels.txt', 'r') as file:
                lines = file.readlines()
                completed_levels = set(line.strip() for line in lines)
        except FileNotFoundError:
            pass
        return completed_levels

    def save_completed_levels(self):
        with open('completed_levels.txt', 'w') as file:
            for level in self.completed_levels:
                file.write(level + '\n')

    def create_interface(self):
        self.frames = []

        for difficulty, levels in self.quest_data.items():
            frame = tk.Frame(self.root)
            frame.pack(side=tk.LEFT, padx=10, pady=10)
            tk.Label(frame, text=difficulty).pack()

            for level, moves in levels:
                level_text = f"{level} ({moves} moves)"
                var = tk.StringVar(value=level in self.completed_levels)
                checkbox = tk.Checkbutton(frame, text=level_text, variable=var, onvalue=True, offvalue=False)
                checkbox.pack(anchor=tk.W)
                checkbox.bind('<Button-1>', lambda event, l=level, v=var: self.update_completion(l, v))

            self.frames.append(frame)

        tk.Button(self.root, text="Save", command=self.save_completed_levels).pack()
        tk.Button(self.root, text="Reset", command=self.reset_completed_levels).pack()

    def update_completion(self, level, var):
        if var.get():
            self.completed_levels.add(level)
        else:
            self.completed_levels.discard(level)

    def reset_completed_levels(self):
        if os.path.exists('completed_levels.txt'):
            os.remove('completed_levels.txt')
        self.root.destroy()
        self.__init__(tk.Tk())


if __name__ == "__main__":
    root = tk.Tk()
    app = QuestApp(root)
    root.mainloop()
