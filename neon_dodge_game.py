import tkinter as tk
import random

W, H = 980, 600
PLAYER_SIZE = 16
ENEMY_SIZE = 14
MAX_ENEMIES = 45

class NeonDodge:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Dodge (Optimized)")
        self.c = tk.Canvas(root, width=W, height=H, bg="#090f1f", highlightthickness=0)
        self.c.pack()

        self.keys = set()
        self.running = True
        self.game_over = False
        self.score = 0
        self.best = 0

        self.px = W // 2
        self.py = H - 50
        self.speed = 9

        self.enemies = []  # [x,y,vy]
        self.spawn_cd = 0

        # Pre-create draw objects (fast)
        self.bg = self.c.create_rectangle(0, 0, W, H, fill="#090f1f", outline="")
        self.player = self.c.create_oval(0, 0, 0, 0, fill="#65f4ff", outline="")
        self.player_glow = self.c.create_oval(0, 0, 0, 0, outline="#2de3ff")
        self.enemy_items = [
            self.c.create_rectangle(-100, -100, -80, -80, fill="#ff5f93", outline="")
            for _ in range(MAX_ENEMIES)
        ]
        self.hud = self.c.create_text(12, 10, anchor="nw", fill="#a8d8ff", font=("Segoe UI", 11, "bold"), text="")
        self.overlay = self.c.create_text(W // 2, H // 2, fill="#ffd7e5", font=("Segoe UI", 30, "bold"), text="")

        root.bind("<KeyPress>", self.on_key_down)
        root.bind("<KeyRelease>", self.on_key_up)
        root.bind("r", self.on_restart)
        root.bind("<Escape>", lambda e: root.destroy())

        self.tick()

    def on_key_down(self, e):
        self.keys.add(e.keysym.lower())

    def on_key_up(self, e):
        self.keys.discard(e.keysym.lower())

    def on_restart(self, _=None):
        if self.game_over:
            self.best = max(self.best, self.score)
            self.score = 0
            self.px = W // 2
            self.enemies.clear()
            self.spawn_cd = 0
            self.game_over = False

    def spawn_enemy(self):
        x = random.randint(20, W - 20)
        y = -20
        vy = random.uniform(4.0, 8.5)
        self.enemies.append([x, y, vy])

    def update_game(self):
        if self.game_over:
            return

        # player movement
        vx = 0
        if "a" in self.keys or "left" in self.keys:
            vx -= self.speed
        if "d" in self.keys or "right" in self.keys:
            vx += self.speed
        self.px = max(PLAYER_SIZE, min(W - PLAYER_SIZE, self.px + vx))

        # spawn logic
        self.spawn_cd += 1
        rate = max(7, 24 - self.score // 45)
        if self.spawn_cd >= rate:
            self.spawn_cd = 0
            if len(self.enemies) < MAX_ENEMIES:
                self.spawn_enemy()

        # enemy updates + collision
        alive = []
        for ex, ey, vy in self.enemies:
            ey += vy
            if ey < H + 30:
                alive.append([ex, ey, vy])
                if abs(ex - self.px) < (PLAYER_SIZE + ENEMY_SIZE) and abs(ey - self.py) < (PLAYER_SIZE + ENEMY_SIZE):
                    self.game_over = True
        self.enemies = alive

        self.score += 1

    def render(self):
        # subtle fade trail by changing bg each frame (cheap)
        self.c.itemconfig(self.bg, fill="#090f1f")

        # player
        p = PLAYER_SIZE
        self.c.coords(self.player, self.px - p, self.py - p, self.px + p, self.py + p)
        self.c.coords(self.player_glow, self.px - p - 6, self.py - p - 6, self.px + p + 6, self.py + p + 6)

        # enemies
        for i, item in enumerate(self.enemy_items):
            if i < len(self.enemies):
                ex, ey, _ = self.enemies[i]
                e = ENEMY_SIZE
                self.c.coords(item, ex - e, ey - e, ex + e, ey + e)
            else:
                self.c.coords(item, -100, -100, -80, -80)

        self.best = max(self.best, self.score)
        self.c.itemconfig(
            self.hud,
            text=f"Neon Dodge (optimized)  |  Score: {self.score}  |  Best: {self.best}  |  A/D or ←/→ move  |  R restart  |  ESC quit"
        )

        if self.game_over:
            self.c.itemconfig(self.overlay, text="GAME OVER
Press R to restart")
        else:
            self.c.itemconfig(self.overlay, text="")

    def tick(self):
        if self.running:
            self.update_game()
            self.render()
        self.root.after(16, self.tick)  # ~60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    NeonDodge(root)
    root.mainloop()
