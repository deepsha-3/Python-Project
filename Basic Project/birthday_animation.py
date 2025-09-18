import turtle
import time
import random
from playsound import playsound
import threading

# 🎵 Play music in background using threading
def play_music():
    try:
        playsound(r"C:\Users\Deepsha\Music\YourBirthdaySong.mp3")  # Replace with your actual file path
    except Exception as e:
        print("Music error:", e)

# Start music in a separate thread so it doesn't block animation
threading.Thread(target=play_music, daemon=True).start()

# 🎨 Screen Setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Happy Birthday Animation")

# 🍰 Draw Cake Layers
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
draw_cake_layer(cake, 220, 50, -160, "#f7c6c6")  # Bottom layer
draw_cake_layer(cake, 180, 45, -100, "#f4a4a4")  # Middle layer
draw_cake_layer(cake, 140, 40, -50, "#f08080")   # Top layer

# 🕯️ Draw Large Candles
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

# 🔥 Flickering Flames
flame = turtle.Turtle()
flame.hideturtle()
flame.speed(0)

def draw_flames():
    for x in candle_positions:
        flame.penup()
        flame.goto(x + candle_width // 2, 35)
        flame.color(random.choice(["orange", "yellow"]))
        flame.begin_fill()
        flame.circle(7)
        flame.end_fill()

for _ in range(10):
    draw_flames()
    time.sleep(0.2)
    flame.clear()

# 💨 Blow Out Candles
time.sleep(1)
for x in candle_positions:
    flame.penup()
    flame.goto(x + candle_width // 2, 35)
    flame.color("black")
    flame.begin_fill()
    flame.circle(7)
    flame.end_fill()

# 🎉 Birthday Message
message = turtle.Turtle()
message.hideturtle()
message.speed(0)
message.penup()
message.goto(-120, 100)  # Adjusted position to appear above cake
message.color("yellow")
message.write("Happy Birthday Deepsha!", align="left", font=("Arial", 22, "bold"))
time.sleep(1)

# 🎊 Bounce Animation
for bounce in range(6):
    message.clear()
    message.goto(-120, 100 + bounce * 10)
    message.write("Happy Birthday Deepsha!", align="left", font=("Arial", 22, "bold"))
    time.sleep(0.4)

# 🧵 Finish
turtle.done()
