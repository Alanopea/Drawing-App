from tkinter import *
import math
from tkinter import colorchooser, simpledialog, messagebox


root = Tk()
root.title("Drawing App")
root.geometry("2048x1080")
#root.geometry("1000x800")
root.configure(bg="#f0f0f0")

# Creating frames
frame_right = Frame(root, height=600, width=300, bg="#d4d4d4", padx=10, pady=10)
frame_right.grid(row=1, column=1)

frame_canvas = Frame(root, height=600, width=600, bg="#ffffff", padx=10, pady=10, relief=RIDGE, bd=5)
frame_canvas.grid(row=1, column=0)

# Canvas
canvas_width = 600
canvas_height = 600
canvas = Canvas(frame_canvas, height=canvas_height, width=canvas_width, bg="white")
canvas.pack()

# Basic settings
line_color = "black"
line_width = 2

# Line colour F
def choose_color():
    global line_color
    color = colorchooser.askcolor(title="Choose Line Color")
    if color[1]:
        line_color = color[1]

# Line width F
def set_line_width():
    global line_width
    width = simpledialog.askinteger("Line Width", "Enter line width (1-10):", minvalue=1, maxvalue=10)
    if width:
        line_width = width

# Manual coordinates F
def enter_coordinates():
    global points
    try:
        x1 = simpledialog.askinteger("Input", "Enter X1 coordinate:")
        if x1 is None:
            return

        y1 = simpledialog.askinteger("Input", "Enter Y1 coordinate:")
        if y1 is None:
            return

        x2 = simpledialog.askinteger("Input", "Enter X2 coordinate:")
        if x2 is None:
            return

        y2 = simpledialog.askinteger("Input", "Enter Y2 coordinate:")
        if y2 is None:
            return 
        
        points = [(x1, y1), (x2, y2)]
        draw_line()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for the coordinates.")

# Clear all F
def reset_canvas():
    global points, line_coords
    points.clear()
    line_coords.clear()
    canvas.delete("all")
    coords_label.config(text="Coordinates: (x1, y1) | (x2, y2) | Sequence: []")

# Exit F
def exit_app():
    root.destroy()

# Select method F
def enable_drawing(method):
    global drawing_enabled, current_method
    drawing_enabled = True
    current_method = method
    reset_canvas()

# Storing points for line drawing
points = []
drawing_enabled = False
line_coords = []

# Label for coordinates and cursor position
coords_label = Label(frame_right, text="Coordinates: (x1, y1) | (x2, y2) | Sequence: []", bg="#d4d4d4", fg="black", wraplength=250)
coords_label.pack(pady=10)

cursor_label = Label(frame_right, text="Cursor: (0, 0)", bg="#d4d4d4", fg="black")
cursor_label.pack(pady=10)

# Function to round values
def Round(value):
    return int(round(value))

# Function to plot pixels
def plot_pixel(x, y):
    size = 8
    canvas.create_rectangle(
        x * size + (canvas_width // 2) - size // 2,
        (canvas_height // 2) - y * size - size // 2,
        x * size + (canvas_width // 2) + size // 2,
        (canvas_height // 2) - y * size + size // 2,
        outline=line_color, fill=line_color, width=line_width
    )
    line_coords.append((x, y))

# Method I (Slope-Intercept)
def plot_line_slope_intercept(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if dx == 0:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            plot_pixel(x1, y)
        return
    
    step = 1 if x1 < x2 else -1
    m = dy / dx
    b = y1 - m * x1

    x = x1
    end = x2 + step
    while x != end:
        y = round(m * x + b)
        plot_pixel(x, y)
        x += step

# Method II (DDA - Digital Differential Analyzer)
def plot_line_dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    M = max(abs(dx), abs(dy))
    dx_prime = dx / M
    dy_prime = dy / M

    x = x1 + 0.5
    y = y1 + 0.5
    for i in range(M + 1):
        plot_pixel(int(math.floor(x)), int(math.floor(y)))
        x += dx_prime
        y += dy_prime

# Method III (Bresenham's algorithm)
def plot_line_bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    s1 = 1 if x2 > x1 else -1
    s2 = 1 if y2 > y1 else -1
    interchange = False
    if dy > dx:
        dx, dy = dy, dx
        interchange = True
    ne = 2 * dy - dx
    x, y = x1, y1
    plot_pixel(x, y)
    for i in range(dx):
        if ne > 0:
            if interchange:
                x += s1
            else:
                y += s2
            ne -= 2 * dx
        if interchange:
            y += s2
        else:
            x += s1
        ne += 2 * dy
        plot_pixel(x, y)

# Drawing line F
def draw_line():
    if len(points) == 2:
        x1, y1 = points[0]
        x2, y2 = points[1]
        
        if current_method == 'slope_intercept':
            plot_line_slope_intercept(x1, y1, x2, y2)
        elif current_method == 'dda':
            plot_line_dda(x1, y1, x2, y2)
        elif current_method == 'bresenham':
            plot_line_bresenham(x1, y1, x2, y2)
        
        points.clear()
        line_coords.clear()

# Canvas click F
def on_canvas_click(event):
    if drawing_enabled:
        adjusted_x = (event.x - (canvas_width // 2)) // 8
        adjusted_y = ((canvas_height // 2) - event.y) // 8
        points.append((adjusted_x, adjusted_y))
        canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="yellow")
        if len(points) == 2:
            draw_line()

# Cursos position F
def update_cursor_position(event):
    adjusted_x = (event.x - (canvas_width // 2)) // 8
    adjusted_y = ((canvas_height // 2) - event.y) // 8
    cursor_label.config(text=f"Cursor: ({adjusted_x}, {adjusted_y})")


# Buttons design
button_color = Button(frame_right, text="Choose Color", command=choose_color, bg="#1e87ca", width=15, height=2, fg="white")
button_color.pack(pady=10)

button_line_width = Button(frame_right, text="Set Line Width", command=set_line_width, bg="#1e87ca", width=15, height=2, fg="white")
button_line_width.pack(pady=10)

button_coords = Button(frame_right, text="Enter Coordinates", command=enter_coordinates, bg="#1e87ca", width=15, height=2, fg="white")
button_coords.pack(pady=10)

button_reset = Button(frame_right, text="Clear All", command=reset_canvas, bg="#ff9595", width=15, height=2, fg="white")
button_reset.pack(pady=10)

button_exit = Button(frame_right, text="Exit", command=exit_app, bg="#ff4343", width=15, height=2, fg="white")
button_exit.pack(pady=10)

button_slope_intercept = Button(frame_right, text="M I (Slope-Intercept)", command=lambda: enable_drawing('slope_intercept'), bg="#5cb85c", width=15, height=2, fg="white")
button_slope_intercept.pack(pady=10)

button_dda = Button(frame_right, text="M II (DDA)", command=lambda: enable_drawing('dda'), bg="#5cb85c", width=15, height=2, fg="white")
button_dda.pack(pady=10)

button_bresenham = Button(frame_right, text="M III (Bresenham)", command=lambda: enable_drawing('bresenham'), bg="#5cb85c", width=15, height=2, fg="white")
button_bresenham.pack(pady=10)


canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Motion>", update_cursor_position)

root.mainloop()