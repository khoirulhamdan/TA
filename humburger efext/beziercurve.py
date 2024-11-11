import tkinter as tk
import customtkinter as ctk
import random
from PIL import Image, ImageTk
import os

# Set your base directory where the icons folder is located
base_dir = os.path.dirname(os.path.abspath(__file__))

def get_icon_path(filename):
    return os.path.join(base_dir, "icons", filename)

# Global container for all nodes
node_app_container = []
active_line = None

class Node:
    def __init__(self, canvas, node_type, image_id):
        self.canvas = canvas
        self.radius = 5
        self.type = node_type  # Store node type
        self.image_id = image_id  # Store the image_id reference (created in BezierCurveApp)
        
        # Bezier curve related attributes
        self.line_id = None
        self.connected_node = None  # Track the connected node

        # Get the current position of the image from canvas
        self.x, self.y = self.canvas.coords(self.image_id)  # Extract x, y coordinates from canvas image ID

        # Bind events for the node
        self.canvas.tag_bind(self.image_id, '<Button-1>', self.start_connection)
        self.canvas.tag_bind(self.image_id, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.image_id, '<ButtonRelease-1>', self.on_release)
        self.connection_line = None

    def start_connection(self, event):
        # Start a line from this node
        global active_line
        active_line = self

    def on_drag(self, event):
        # Update the curve as it's being dragged
        global active_line
        if active_line:
            # If there is an existing connection, delete the old line
            if self.connected_node:
                self.canvas.delete(self.line_id)
                self.connected_node.connected_node = None
                self.connected_node = None

            # Update the curve dynamically
            self.update_curve(self.x, self.y, event.x, event.y)

    def on_release(self, event):
        # Check if release is over another node and types match
        global node_app_container, active_line
        for node in node_app_container:
            if node != self and node.is_inside(event.x, event.y):
                # Connect to the other node only if types match and no connection exists
                if node.type == self.type and not node.connected_node and not self.connected_node:
                    self.update_curve(self.x, self.y, node.x, node.y)
                    self.connection_line = self
                    self.connected_node = node
                    node.connected_node = self  # Create mutual connection
                    active_line = None
                    break

        if active_line:
            # If not connected, remove the temporary line
            self.canvas.delete(self.line_id)
            active_line = None

    def is_inside(self, x, y):
        # Check if a point is inside this node
        return (self.x - self.radius <= x <= self.x + self.radius and
                self.y - self.radius <= y <= self.y + self.radius)

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

class BezierCurveApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bezier Curve with Tkinter and CustomTkinter")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load images for each node type once and store them in a dictionary
        self.node_images = {
            1: self.load_image("image2.png"),
            2: self.load_image("image3.png"),
            3: self.load_image("image4.png")
        }

        self.create_button = ctk.CTkButton(self, text="Add Node", command=self.add_node)
        self.create_button.pack(side=tk.BOTTOM, pady=10)

    def load_image(self, filename):
        # Load and resize image, then return PhotoImage object
        img_path = get_icon_path(filename)
        original_image = Image.open(img_path)
        resized_image = original_image.resize((10, 10))  # Resize image as needed
        return ImageTk.PhotoImage(resized_image)

    def create_node_image(self, x, y, node_type):
        # Use this method to create the node image on canvas and return the image ID
        return self.canvas.create_image(x, y, image=self.node_images[node_type])

    def add_node(self):
        # Determine position and type of new node
        x, y = 100 + len(node_app_container) * 60, random.randint(100, 400)  # Define x and y in BezierCurveApp
        node_type = random.choice([1, 2, 3])  # Randomly assign a type (1, 2, or 3)
        
        # Create image on canvas and get its ID
        image_id = self.create_node_image(x, y, node_type)
        
        # Create Node object with canvas image ID and type (x, y are determined here)
        node = Node(self.canvas, node_type, image_id)
        node_app_container.append(node)

if __name__ == "__main__":
    app = BezierCurveApp()
    app.mainloop()
