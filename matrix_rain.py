import tkinter as tk
import random

W, H = 980, 620
FONT_SIZE = 16
COLUMNS = W // FONT_SIZE
CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$#@%&*"

class MatrixRain:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Rain")
        self.canvas = tk.Canvas(root, width=W, height=H, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.drops = [random.randint(-H // FONT_SIZE, 0) for _ in range(COLUMNS)]
        self.speed = [random.randint(1, 3) for _ in range(COLUMNS)]
        self.running = True

        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<space>", self.toggle)
        root.bind("r", self.reset)

        self.draw_hud()
        self.tick()

    def draw_hud(self):
        self.canvas.create_text(
            12,
            12,
            anchor="nw",
            fill="#7CFF7C",
            font=("Consolas", 11, "bold"),
            text="Matrix Rain  •  SPACE pause/resume  •  R reset  •  ESC quit",
            tags="hud",
        )

    def reset(self, _=None):
        self.drops = [random.randint(-H // FONT_SIZE, 0) for _ in range(COLUMNS)]
        self.speed = [random.randint(1, 3) for _ in range(COLUMNS)]

    def toggle(self, _=None):
        self.running = not self.running

    def tick(self):
        self.canvas.create_rectangle(0, 0, W, H, fill="black", outline="", stipple="gray50")

        if self.running:
            for i in range(COLUMNS):
                x = i * FONT_SIZE + FONT_SIZE // 2
                y = self.drops[i] * FONT_SIZE
                char = random.choice(CHARS)

                self.canvas.create_text(x, y, text=char, fill="#CCFFCC", font=("Consolas", FONT_SIZE, "bold"))
                self.canvas.create_text(x, y - FONT_SIZE, text=random.choice(CHARS), fill="#66FF66", font=("Consolas", FONT_SIZE))
                self.canvas.create_text(x, y - 2 * FONT_SIZE, text=random.choice(CHARS), fill="#22AA22", font=("Consolas", FONT_SIZE))

                self.drops[i] += self.speed[i]
                if y > H + random.randint(0, 300):
                    self.drops[i] = random.randint(-25, 0)
                    self.speed[i] = random.randint(1, 3)

        self.draw_hud()
        self.root.after(40, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    MatrixRain(root)
    root.mainloop()
