import tkinter as tk
from tkinter import messagebox
import random


class PongGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Ping Pong Game")
        self.master.geometry("1366x768")

        #self.player1_name = player1_name
        #self.player2_name = player2_name

                # Entry widgets for Player 1 and Player 2 names
        self.player1_label = tk.Label(self.master, text="Enter Player 1:")
        self.player1_label.pack()
        self.player1_entry = tk.Entry(self.master)
        self.player1_entry.pack()

        self.player2_label = tk.Label(self.master, text="Enter Player 2:")
        self.player2_label.pack()
        self.player2_entry = tk.Entry(self.master)
        self.player2_entry.pack()

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.timer_label = tk.Label(self.master, text="Timer: 00:00")
        self.timer_label.pack()

        self.timer_running = False
        self.elapsed_time = 0

        self.player1_name = None
        self.player2_name = None
        self.game_started = False

        

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            timer_text = f"Timer: {minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=timer_text)
            self.master.after(1000, self.update_timer)

    def reset_timer(self):
        self.timer_running = False  # Stop the timer
        self.elapsed_time = 0  # Reset the elapsed time to 0
        timer_text = f"Timer: 00:00"
        self.timer_label.config(text=timer_text)
        self.timer_running = True
        self.update_timer()
        
    def start_game(self):

        self.player1_name = self.player1_entry.get()
        self.player2_name = self.player2_entry.get()

        if self.player1_name and self.player2_name:
            self.game_started = True
            # Start the game logic here...

            self.start_timer()
        

            self.canvas = tk.Canvas(self.master, bg="black", width=1366, height=580)
            self.canvas.pack()

            self.paddle_a = self.canvas.create_rectangle(0, 240, 20, 340, fill="white")
            self.paddle_b = self.canvas.create_rectangle(1346, 240, 1366, 340, fill="white")
            self.ball = self.canvas.create_oval(668, 275, 688, 295, fill="white")

            self.ball_speed = [4, 4]
            self.paddle_a_speed = 0
            self.paddle_b_speed = 0

            self.score_a = 0
            self.score_b = 0
            self.max_score = 5  # Set the maximum score

            self.score_display = self.canvas.create_text(683, 30, text=f"Score: {self.score_a} - {self.score_b}", fill="white")
            self.game_over_text = None

            self.canvas.bind("<KeyPress-w>", self.paddle_a_up)
            self.canvas.bind("<KeyPress-s>", self.paddle_a_down)
            self.canvas.bind("<KeyPress-Up>", self.paddle_b_up)
            self.canvas.bind("<KeyPress-Down>", self.paddle_b_down)


        else:
            # If names are not provided, display a message or handle accordingly
            print("Please enter both player names.")

        self.canvas.focus_set()

        self.update()

    def restart_game(self):
        self.reset_timer()
        self.score_a = 0
        self.score_b = 0
        self.update_score_display()
        self.reset_ball()
        self.game_started = False
        self.end_game_text = None
        
        
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None
        self.update()

    def update(self):
        if self.score_a < self.max_score and self.score_b < self.max_score:
            self.move_ball()
            self.move_paddle_a()
            self.move_paddle_b()
            self.check_score()
            self.master.after(10, self.update)
        else:
            self.end_game()

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_speed[0], self.ball_speed[1])

        ball_pos = self.canvas.coords(self.ball)

        if ball_pos[1] <= 0 or ball_pos[3] >= 580:
            self.ball_speed[1] *= -1

        if (ball_pos[0] <= 0 or ball_pos[2] >= 1366 or self.hit_paddle(ball_pos, self.paddle_a) or self.hit_paddle(ball_pos, self.paddle_b)):
            self.ball_speed[0] *= -1

    def move_paddle_a(self):
        self.canvas.move(self.paddle_a, 0, self.paddle_a_speed)
        paddle_pos = self.canvas.coords(self.paddle_a)
        if paddle_pos[1] <= 0 or paddle_pos[3] >= 580:
            self.paddle_a_speed = 0

    def move_paddle_b(self):
        self.canvas.move(self.paddle_b, 0, self.paddle_b_speed)
        paddle_pos = self.canvas.coords(self.paddle_b)
        if paddle_pos[1] <= 0 or paddle_pos[3] >= 580:
            self.paddle_b_speed = 0

    def paddle_a_up(self, event):
        self.paddle_a_speed = -5

    def paddle_a_down(self, event):
        self.paddle_a_speed = 5

    def paddle_b_up(self, event):
        self.paddle_b_speed = -5

    def paddle_b_down(self, event):
        self.paddle_b_speed = 5

    def hit_paddle(self, ball_pos, paddle):
        paddle_pos = self.canvas.coords(paddle)
        return (ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2] and paddle_pos[1] <= ball_pos[3] and paddle_pos[3] >= ball_pos[1])

    def check_score(self):
        ball_pos = self.canvas.coords(self.ball)
        if ball_pos[0] <= 0:
            self.score_b += 1
            self.reset_ball()
        elif ball_pos[2] >= 1366:
            self.score_a += 1
            self.reset_ball()

        self.update_score_display()

    def reset_ball(self):
        self.canvas.coords(self.ball, 673, 280, 693, 300)
        self.ball_speed = [random.choice([4, -4]), random.choice([4, -4])]

    def update_score_display(self):
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score_a} - {self.score_b}")

    def end_game(self):
        self.stop_timer()
        if not self.game_over_text:
            winner = self.player1_name if self.score_a >= self.max_score else self.player2_name
            self.game_over_text = self.canvas.create_text(683, 200, text=f"Game Over!\n{winner} wins!", fill="white", font=("Helvetica", 24))
            self.show_end_game_message()

    def show_end_game_message(self):
        choice = messagebox.askquestion("Game Over", "Do you want to play again?")
        if choice == 'yes':
            # Reset the game if players choose to play again
            self.restart_game()
        else:
            self.master.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
