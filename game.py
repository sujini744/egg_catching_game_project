from random import randrange
from tkinter import Canvas, Tk, messagebox, font

# Simple Egg Catcher Game

canvas_width = 800
canvas_height = 400

root = Tk()
root.title("Egg Catcher")
c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="sea green", width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

# Colors for eggs 
colors = ["light blue", "light green", "light pink", "light yellow", "light cyan"]
color_index = 0

egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty = 0.95

catcher_color = "blue"
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height

catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2,
                       start=200, extent=140, style="arc", outline=catcher_color, width=3)

game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: " + str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor="ne", font=game_font, fill="darkblue", text="Lives: " + str(lives_remaining))

eggs = []

def create_egg():
    global color_index
    x_position = randrange(10, 740)
    y_position = 40
    # Choose color from list
    egg_color = colors[color_index]
    color_index += 1
    if color_index >= len(colors):
        color_index = 0
    new_egg = c.create_oval(x_position, y_position, x_position + egg_width, y_position + egg_height, fill=egg_color, width=0)
    eggs.append(new_egg)
    # Schedule next egg creation
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    if egg in eggs:
        eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: " + str(score))
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining = lives_remaining - 1
    c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))

def check_catch():
    (catcher_left, catcher_top, catcher_right, catcher_bottom) = c.coords(catcher)
    eggs_to_remove = []
    for egg in eggs:
        (egg_left, egg_top, egg_right, egg_bottom) = c.coords(egg)
        # Check if egg is within catcher bounds
        if catcher_left < egg_left and egg_right < catcher_right:
            # Check vertical proximity
            if (catcher_bottom - egg_bottom) < 40:
                eggs_to_remove.append(egg)
    for egg in eggs_to_remove:
        if egg in eggs:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    # Check again after 100 ms
    root.after(100, check_catch)

def increase_score(points):
    global score
    global egg_speed
    global egg_interval
    # Increase the score by points
    score = score + points
    # Make the game harder by increasing speed and decreasing interval
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    # Update the score display
    c.itemconfigure(score_text, text="Score: " + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        if x1 - 20 >= 0:
            c.move(catcher, -20, 0)
        else:
            c.move(catcher, -x1, 0)  # Move only to the edge

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        if x2 + 20 <= canvas_width:
            c.move(catcher, 20, 0)
        else:
            c.move(catcher, canvas_width - x2, 0)  # Move only to the edge

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()

root.after(1000, create_egg)
root.after(1000, move_eggs)
root.after(1000, check_catch)

root.mainloop()

  
