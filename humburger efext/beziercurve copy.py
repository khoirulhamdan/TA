import tkinter as tk
import customtkinter as ctk
import random
from PIL import Image, ImageTk
import os

# Set your base directory where the icons folder is located
base_dir = os.path.dirname(os.path.abspath(__file__))

def get_icon_path(filename):
    return os.path.join(base_dir, "icons", filename)

nodes = []
active_line = None

class BezierCurve:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.line_id = None
        self.update_curve(x1, y1, x2, y2)

    def update_curve(self, x1, y1, x2, y2):
        # Update the coordinates for the curve
        self.canvas.delete(self.line_id)
        cx1, cy1 = (x1 + x2) / 2, y1
        cx2, cy2 = (x1 + x2) / 2, y2
        points = self.bezier_points(x1, y1, cx1, cy1, cx2, cy2, x2, y2)
        self.line_id = self.canvas.create_line(points, fill="red", width=2, tags="line", smooth=True)

    def bezier_points(self, x1, y1, cx1, cy1, cx2, cy2, x2, y2, num_points=100):
        points = []
        for t in range(num_points + 1):
            t /= num_points
            x = (1 - t) ** 3 * x1 + 3 * (1 - t) ** 2 * t * cx1 + 3 * (1 - t) * t ** 2 * cx2 + t ** 3 * x2
            y = (1 - t) ** 3 * y1 + 3 * (1 - t) ** 2 * t * cy1 + 3 * (1 - t) * t ** 2 * cy2 + t ** 3 * y2
            points.append((x, y))
        return points

class Node:
    def __init__(self, canvas, x, y, node_type):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = 5
        self.type = node_type  # Add type to the node

        self.image = self.load_image(node_type)
        self.id = self.canvas.create_image(self.x, self.y, image=self.image)

        self.canvas.tag_bind(self.id, '<Button-1>', self.start_connection)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.connection_line = None

    def load_image(self, node_type):
        # Load images based on node type using get_icon_path
        if node_type == 1:
            img_path = get_icon_path("image1.png")  # Replace with your image filename
        elif node_type == 2:
            img_path = get_icon_path("image2.png")  # Replace with your image filename
        elif node_type == 3:
            img_path = get_icon_path("image3.png")  # Replace with your image filename
        else:
            return None

        # Load the image and resize it to 5x5 pixels
        original_image = Image.open(img_path)
        resized_image = original_image.resize((10, 10))  # Resize to 5x5 pixels
        return ImageTk.PhotoImage(resized_image)


    def start_connection(self, event):
        # Start a line from this node
        global active_line
        active_line = BezierCurve(self.canvas, self.x, self.y, event.x, event.y)

    def on_drag(self, event):
        # Update the curve as it's being dragged
        global active_line
        if active_line:
            active_line.update_curve(self.x, self.y, event.x, event.y)

    def on_release(self, event):
        # Check if release is over another node and types match
        global nodes, active_line
        for node in nodes:
            if node != self and node.is_inside(event.x, event.y):
                # Connect to the other node only if types match
                if node.type == self.type:
                    active_line.update_curve(self.x, self.y, node.x, node.y)
                    self.connection_line = active_line
                    active_line = None
                    break

        if active_line:
            # If not connected, remove the temporary line
            self.canvas.delete(active_line.line_id)
            active_line = None

    def is_inside(self, x, y):
        # Check if a point is inside this node
        return (self.x - self.radius <= x <= self.x + self.radius and
                self.y - self.radius <= y <= self.y + self.radius)


class BezierCurveApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bezier Curve with Tkinter and CustomTkinter")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_button = ctk.CTkButton(self, text="Add Node", command=self.add_node)
        self.create_button.pack(side=tk.BOTTOM, pady=10)

    def add_node(self):
        x, y = 100 + len(nodes) * 60, random.randint(100, 400)
        node_type = random.choice([1, 2, 3])  # Randomly assign a type (1, 2, or 3)
        node = Node(self.canvas, x, y, node_type)
        nodes.append(node)


if __name__ == "__main__":
    app = BezierCurveApp()
    app.mainloop()
