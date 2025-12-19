import turtle
import random
import threading
import time
from playsound import playsound

# 🎵 Play music in background using threading
def play_music():
    try:
        playsound(r"C:\Users\Deepsha\Music\YourBirthdaySong.mp3")  # ✅ Make sure this path is correct
    except Exception as e:
        print("Music error:", e)

# Start music in a separate thread
threading.Thread(target=play_music, daemon=True).start()

# Screen Setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Happy Birthday Animation")
screen.tracer(0)  # Turn off auto updates for smoother control

# Draw cake layers
def draw_cake_layer(t, width, height, y_pos, color):
    t.penup()
    t.goto(-width // 2, y_pos)
    t.color(color)
    t.begin_fill()
    t.pendown()
    t.forward(width)
    t.circle(height // 2, 90)
    t.forward(height)
    t.circle(height // 2, 90)
    t.forward(width)
    t.circle(height // 2, 90)
    t.forward(height)
    t.circle(height // 2, 90)
    t.end_fill()

cake = turtle.Turtle()
cake.hideturtle()
cake.speed(0)

# Draw 3 colorful layers
draw_cake_layer(cake, 220, 50, -160, "#f7c6c6")
draw_cake_layer(cake, 180, 45, -100, "#f4a4a4")
draw_cake_layer(cake, 140, 40, -50, "#f08080")

# Candles
candle = turtle.Turtle()
candle.hideturtle()
candle.speed(0)
candle.color("white")
candle_width = 15
candle_height = 40
candle_positions = [-50, -25, 0, 25, 50]

for x in candle_positions:
    candle.penup()
    candle.goto(x, -10)
    candle.pendown()
    candle.begin_fill()
    for _ in range(2):
        candle.forward(candle_width)
        candle.left(90)
        candle.forward(candle_height)
        candle.left(90)
    candle.end_fill()

# Flames
flame = turtle.Turtle()
flame.hideturtle()
flame.speed(0)

def draw_flames():
    flame.clear()
    for x in candle_positions:
        flame.penup()
        flame.goto(x + candle_width // 2, 35)
        flame.color(random.choice(["orange", "yellow"]))
        flame.begin_fill()
        flame.circle(7)
        flame.end_fill()
    screen.update()

# Flickering flames
for _ in range(10):
    draw_flames()
    time.sleep(0.2)

# Blow out flames with fade effect
def blow_out_flames():
    for size in range(7, 0, -1):  # Shrink flame gradually
        flame.clear()
        for x in candle_positions:
            flame.penup()
            flame.goto(x + candle_width // 2, 35)
            flame.color("orange")
            flame.begin_fill()
            flame.circle(size)
            flame.end_fill()
        screen.update()
        time.sleep(0.1)

    # Optional smoke puff
    for x in candle_positions:
        flame.penup()
        flame.goto(x + candle_width // 2, 35)
        flame.color("gray")
        flame.begin_fill()
        flame.circle(5)
        flame.end_fill()
    screen.update()

blow_out_flames()

# Birthday message
message = turtle.Turtle()
message.hideturtle()
message.speed(0)
message.penup()
message.goto(-120, 100)
message.color("yellow")
message.write("Happy Birthday Deepsha!", align="left", font=("Arial", 22, "bold"))
screen.update()

# Bounce 
for bounce in range(6):
    message.clear()
    message.goto(-120, 100 + bounce * 10)
    message.write("Happy Birthday Deepsha!", align="left", font=("Arial", 22, "bold"))
    screen.update()
    time.sleep(0.4)

# Finish
turtle.done()
