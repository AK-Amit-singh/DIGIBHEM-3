import tkinter as tk
import random

WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
MOVE_INCREMENT = SNAKE_SIZE
DELAY = 100

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.snake = []
        self.food = None
        self.direction = "Right"
        self.score = 0
        self.running = False
        self.paused = False

        self.score_text = self.canvas.create_text(50, 10, text="Score: 0", fill="white", font=("Arial", 14))
        self.instruction_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 50,
            text="Controls:\nArrow Keys to Move\nP to Pause/Resume", fill="white", font=("Arial", 16))

        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 14), bg="green", fg="white", command=self.start_game)
        self.start_button.pack(pady=10)

        self.root.bind("<KeyPress>", self.handle_keypress)

    def start_game(self):
        self.start_button.pack_forget()
        self.canvas.delete("all")
        self.canvas.create_text(50, 10, text="Score: 0", fill="white", font=("Arial", 14), tag="score")
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = "Right"
        self.score = 0
        self.running = True
        self.paused = False
        self.draw_snake()
        self.create_food()
        self.move_snake()

    def draw_snake(self):
        self.canvas.delete("snake")

        for index, (x, y) in enumerate(self.snake):
            if index == 0:
                # Snake head
                self.canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="#228B22", tag="snake")
                # Eyes
                eye_size = 3
                offset = 5
                if self.direction in ["Left", "Right"]:
                    self.canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white", tag="snake")
                    self.canvas.create_oval(x + offset, y + SNAKE_SIZE - offset - eye_size, x + offset + eye_size, y + SNAKE_SIZE - offset, fill="white", tag="snake")
                else:
                    self.canvas.create_oval(x + offset, y + offset, x + offset + eye_size, y + offset + eye_size, fill="white", tag="snake")
                    self.canvas.create_oval(x + SNAKE_SIZE - offset - eye_size, y + offset, x + SNAKE_SIZE - offset, y + offset + eye_size, fill="white", tag="snake")
            else:
                self.canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="#32CD32", tag="snake")

    def move_snake(self):
        if not self.running or self.paused:
            return

        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= MOVE_INCREMENT
        elif self.direction == "Down":
            head_y += MOVE_INCREMENT
        elif self.direction == "Left":
            head_x -= MOVE_INCREMENT
        elif self.direction == "Right":
            head_x += MOVE_INCREMENT

        new_head = (head_x, head_y)

        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in self.snake
        ):
            self.game_over()
            return

        self.snake = [new_head] + self.snake

        if new_head == self.food:
            self.score += 1
            self.canvas.itemconfigure("score", text=f"Score: {self.score}")
            self.create_food()
        else:
            self.snake.pop()

        self.draw_snake()
        self.root.after(DELAY, self.move_snake)

    def handle_keypress(self, event):
        if not self.running:
            return

        key = event.keysym
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        if key in ["Up", "Down", "Left", "Right"] and key != opposite.get(self.direction):
            self.direction = key
        elif key.lower() == "p":
            self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.move_snake()
        else:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="PAUSED", fill="yellow", font=("Arial", 30), tag="pause")
        if not self.paused:
            self.canvas.delete("pause")

    def create_food(self):
        while True:
            x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
            y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
        self.canvas.delete("food")
        self.canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="red", tag="food")

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill="white", font=("Arial", 30))
        self.start_button.config(text="Restart Game")
        self.start_button.pack(pady=10)


# Run game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
