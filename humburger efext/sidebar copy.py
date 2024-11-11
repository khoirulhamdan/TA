import os
from PIL import Image
import customtkinter as ctk
import random

import pywinstyles.py_win_style
import codesaver
import beziercurve as nodecurve
import tkinter as tk
import pywinstyles as pywin

# Atur mode tampilan (light/dark)
ctk.set_appearance_mode("dark")  

# Define your base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define colors and other constants
PRIMARY_COLOR = "#78ABA8"
ORANGE_PALLETE = "#EF9C66"
YELLOW_PALLETE = "#FCDC94"
LIGHT_GREEN_PALLETE = "#C8CFA0"
SECONDARY_COLOR = "#646464"
GREEN_PALLETE = "#78ABA8"
HOVER_COLOR = "#0056b3"
BACKGROUND_COLOR = "#343a40"
TEXT_COLOR = "#ffffff"
DARK_COLOR = "#000000"

# Define constant toggle visual or code
toggle_visual_or_code = True
node_container = []
zoom_level = 1.0

def get_icon_path(filename):
    return os.path.join(base_dir, "icons", filename)

class Button:
    def __init__(self, button_name, icon_button, sub_buttons=None):
        self.button_name = button_name
        self.icon_button = self._create_image(icon_button)
        self.sub_buttons = sub_buttons if sub_buttons else []
        self.expand_status = False  # Initialize expand status
        self.subbutton_frame = None  # To hold the frame for sub-buttons
        self.main_button = None

    def _create_image(self, icon_button):
        icon_path = get_icon_path(icon_button)
        return ctk.CTkImage(Image.open(icon_path), size=(16, 16))

    def toggle_expand(self):
        self.expand_status = not self.expand_status
    
    def toggle_expand_off(self):
        self.expand_status = False

# SubButton class remains the same
class SubButton:
    def __init__(self, sub_button_name, sub_button_icon, hover_color):
        self.sub_button_name = sub_button_name
        self.icon_path = get_icon_path(sub_button_icon)
        self.sub_button_icon = self._create_image(height=15, width=15)
        self.hover_color = hover_color

    def _create_image(self, height = 75 , width = 75):
        return ctk.CTkImage(Image.open(self.icon_path), size=(height, width))
    
class DraggableNode(ctk.CTkFrame):

    def __init__(self, master, name, icon, visual_framer, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name
        self.configure(width=65, height=50, fg_color="transparent", corner_radius=5)

        self.preferences = codesaver.init_processing(name)
        self.code = self.preferences.code 
        # Create icon label

        self.icon_bg = ctk.CTkLabel(self, width=50, height=50, corner_radius=5, fg_color=SECONDARY_COLOR, text="")
        self.icon_bg.place(relx=0.5, rely=0.5, anchor="center")

        self.icon_label = ctk.CTkLabel(self, fg_color=SECONDARY_COLOR, image=icon, text="")
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add a small delete button (e.g., "X") on the top-right corner of the node
        self.delete_button = ctk.CTkButton(
            self,
            text="x",
            width=5,
            height=5,
            fg_color="#FF1111",  # Red color for delete button
            hover_color="#FF6666",
            command=self.delete_node,
            text_color="white",
            font=("Arial", 10, "bold")
        )
        self.delete_button.place(x = 5, rely=0.1, anchor="center")  # Position at top-right corner
        self.delete_button.lower()

        self.delete_button_hover = False

        # tambahkan icon image berukuran 10 x 10 dengan posisi di sebelah kanan draggable node
        self.node_icon = ctk.CTkLabel(self, height=5, width=5, fg_color="transparent", image=self._node(get_icon_path("image1.png")), text="")
        self.node_icon.place(relx=0.9, rely=0.5, anchor="center")
        #pywin.set_opacity(self.node_icon, value = 0.5)

        self.pos_x_init = 0
        self.pos_y_init = 0
        self._enable_dragging()

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_hover_leave)
        self.icon_bg.bind("<Enter>", self.on_hover)
        self.icon_bg.bind("<Leave>", self.on_hover_leave)
        self.icon_label.bind("<Enter>", self.on_hover)
        self.icon_label.bind("<Leave>", self.on_hover_leave)

        self.delete_button.bind("<Enter>", self.on_delete_button_hover)
        self.delete_button.bind("<Leave>", self.on_delete_button_leave)

    def delete_node(self):
        """Delete the current node from the visual frame and node_container."""
        # Remove the node from node_container
        if self in node_container:
            node_container.remove(self)
        # Destroy the node widget from the UI
        self.destroy()
        # Update the sidebar buttons when a node is deleted
        update_sidebar_buttons()
        void_preference()

    def on_hover(self, event=None):
        """Show the delete button when the node is hovered."""
        if len(node_container) > 1:
            if self != node_container[0] :
                self.delete_button.lift()  # Bring the delete button to the front
        else:
            self.delete_button.lift() 

    def on_hover_leave(self, event=None):
        """Hide the delete button when the hover ends."""
        self.delete_button.lower()  # Send the delete button to the back

    def on_delete_button_hover(self, event=None):
        """Set delete button hover flag to True when hovered."""
        self.delete_button_hover = True
        self.delete_button.lift()  # Keep the delete button visible

    def on_delete_button_leave(self, event=None):
        """Reset delete button hover flag when no longer hovered."""
        self.delete_button_hover = False
        self.delete_button.lower()  # Hide the delete button

    def _node(self, icon):
        icon_path = get_icon_path(icon)
        return ctk.CTkImage(Image.open(icon_path), size=(10, 10))


    def _enable_dragging(self):

        """Enable dragging functionality for the widget."""

        def on_drag_start(event):
            # Store initial mouse position and widget's position
            self.start_x = event.x_root
            self.start_y = event.y_root

        def on_drag_motion(event):
            # Calculate the new position based on the movement
            self.new_x = event.x_root - self.start_x + self.pos_x_init
            self.new_y = event.y_root - self.start_y + self.pos_y_init
            # Move the widget to the new position
            self.place(x=self.new_x, y=self.new_y)

        def release_motion(event):
            # Update initial position after dragging
            self.pos_x_init = self.new_x
            self.pos_y_init = self.new_y

        # Bind mouse events to the widget
        self.icon_bg.bind("<Button-1>", on_drag_start)
        self.icon_bg.bind("<B1-Motion>", on_drag_motion)
        self.icon_bg.bind("<ButtonRelease-1>", release_motion)
        self.icon_bg.bind("<Button-3>", lambda event: update_preference(event, self))

        # Also bind the same events to the icon label
        self.icon_label.bind("<Button-1>", on_drag_start)
        self.icon_label.bind("<B1-Motion>", on_drag_motion)
        self.icon_label.bind("<ButtonRelease-1>", release_motion)
        self.icon_label.bind("<Button-3>", lambda event: update_preference(event, self))


# Define buttons and sub-buttons
buttons = [
    Button("Input System", "home.png", [
        SubButton("folder", "folder.png",GREEN_PALLETE),
        SubButton("gdrive", "gdrive.png",GREEN_PALLETE)
    ]),
    Button("Konsep Pendahuluan", "cpm1.png", [
        SubButton("pembentukan citra", "pembentukan citra.png", LIGHT_GREEN_PALLETE),
    ]),
    Button("Pengolahan\nCitra digital", "cpm2.png", [
        SubButton("analisa biner", "analisa_citra_biner.png", YELLOW_PALLETE),
        SubButton("analisa abu", "analisa_citra_abu.png", YELLOW_PALLETE),
        SubButton("transformasi fourier", "transformasi_fourier.png", YELLOW_PALLETE)
    ]),
    Button("Klasifikasi dan        \n Pengenalan Object", "cpm3.png", [
        SubButton("deteksi tepi", "deteksi_tepi.png", ORANGE_PALLETE),
        SubButton("ekstraksi_fitur", "ekstraksi_fitur.png", ORANGE_PALLETE)
    ])
]

text_code = " lorem opjhgfjjjojjjkhbfff \n dolor sit amet,\n iii"

# Create main window
root = tk.Tk()
root.geometry("1000x500")
root.title("Skripsi program visual programming")

# Create sidebar frame
sidebar = ctk.CTkFrame(root, width=200, height=500, corner_radius=0, bg_color=BACKGROUND_COLOR)
sidebar.grid(row=0, column=0, sticky="nsw")

# Create sidebar label
sidebar_label = ctk.CTkLabel(sidebar, text="Connection", font=("Arial", 16, "bold"), text_color=TEXT_COLOR)
sidebar_label.grid(row=0, column=0, padx=20, pady=20)

# Function to create main sidebar buttons
def create_sidebar_buttons():
    for i, button in enumerate(buttons):
        # Create main button with icon and text
        main_button = ctk.CTkButton(
            master=sidebar,
            text=f" {button.button_name}",
            image=button.icon_button,
            compound="left",
            command=lambda b=button: toggle_expand(b),
            height=25,
            width=180,
            anchor="w",
            corner_radius=5,
            fg_color="transparent",
            hover_color=SECONDARY_COLOR
        )
        main_button.grid(row=i*2+1, column=0, padx=5, pady=5, sticky="w")
        button.main_button = main_button

        # Create frame for sub buttons
        subbutton_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        subbutton_frame.grid(row=i*2+2, column=0, padx=30, pady=0, sticky="w")
        subbutton_frame.grid_remove()  # Initially hide the frame
        
        button.subbutton_frame = subbutton_frame  # Assign the frame to the button
        
        # Create sub buttons inside frame
        max_columns = 3
        for j, sub_button in enumerate(button.sub_buttons):
            subbutton = ctk.CTkButton(
                master=subbutton_frame,
                text="",
                image=sub_button.sub_button_icon,
                height=20,
                width=20,
                corner_radius=5,
                fg_color="transparent",
                hover_color=sub_button.hover_color
            )
            subbutton.grid(row=j // max_columns, column=j % max_columns, padx=5, pady=5)
            # Bind hover events
            subbutton.bind("<Enter>", lambda event, icon=sub_button._create_image(60,60), name=sub_button.sub_button_name: show_frame(event, icon, name))
            subbutton.bind("<Leave>", hide_frame)
            subbutton.bind("<Double-1>", lambda event,icon=sub_button._create_image(30,30), button_name=sub_button.sub_button_name: on_double_click(event, button_name,icon))

    update_sidebar_buttons()

def  update_sidebar_buttons(): 

    def toggle_expand_off(button):
        button.toggle_expand_off()
        if button.expand_status:
            button.subbutton_frame.grid()
            button.main_button.configure(fg_color=SECONDARY_COLOR)

        else:
            button.subbutton_frame.grid_remove()
            button.main_button.configure(fg_color="transparent", hover_color=SECONDARY_COLOR)

    if not node_container:
        for index in range(1, len(buttons)):
            buttons[index].main_button.configure(state="disabled")
            toggle_expand_off(buttons[index])
        buttons[0].main_button.configure(state="normal")
    
    else :
        for index in range(1, len(buttons)):
            buttons[index].main_button.configure(state="normal")
        buttons[0].main_button.configure(state="disabled")
        toggle_expand_off(buttons[0])


def on_double_click(event, name, icon):
    global toggle_visual_or_code
    if toggle_visual_or_code:  # If the visual frame is active
        spawn_node(name, icon)
    update_sidebar_buttons()


def spawn_node(name, icon):
    # Random offset between 10 and 20 pixels, converted to relative values based on the visual frame size
    offset_x = random.randint(-10, 10) / visual_frame.winfo_width()
    offset_y = random.randint(-10, 10) / visual_frame.winfo_height()

    # Create a new DraggableNode instance in the center of the visual frame, with random offset
    relx = 0.5 + offset_x
    rely = 0.5 + offset_y

    node = DraggableNode(visual_frame, name, icon, canvas)
    node.place(relx=relx, rely=rely, anchor="center")
    node_container.append(node)

# Function to toggle expand/collapse of sub buttons
def toggle_expand(button):
    button.toggle_expand()
    
    if button.expand_status:
        button.subbutton_frame.grid()
        button.main_button.configure(fg_color=SECONDARY_COLOR)

    else:
        button.subbutton_frame.grid_remove()
        button.main_button.configure(fg_color="transparent", hover_color=SECONDARY_COLOR)

# Function to show a new frame on hover
def show_frame(event, icon, name):
    subbutton = event.widget
    frame = ctk.CTkFrame(master=root, width=120, height=100, corner_radius=0, fg_color=SECONDARY_COLOR)
    frame.place(x=180 + 20, y=subbutton.winfo_rooty() - root.winfo_rooty())
    
    subbutton.hover_frame = frame

    icon_label = ctk.CTkLabel(master=frame, image=icon, text="")
    icon_label.place(relx=0.5, y = 10, anchor='n')

    name_label = ctk.CTkLabel(master=frame, text=name, font=("Arial", 12))
    name_label.place(relx=0.5, y=75, anchor='n')

# Function to hide the new frame when hover ends
def hide_frame(event):
    if hasattr(event.widget, 'hover_frame'):
        try:
            event.widget.hover_frame.destroy()
            event.widget.hover_frame = None
        except AttributeError:
            pass  # Tidak melakukan apa-apa jika hover_frame tidak ada


def void_preference(event = None): 
    for widget in preference_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(master=preference_frame, text="Preferences", font=("Arial", 16, "bold"))
    title.pack(pady=20, padx = 60)

# Create sidebar buttons
create_sidebar_buttons()

# Create content area and other widgets
content = ctk.CTkFrame(root, width=600, height=500, corner_radius=0, fg_color="#252525")
content.grid(row=0, column=1, sticky="nsew")  # Make content frame expandable

# Configure grid for content area
content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(2, weight=1)

button_frame = ctk.CTkFrame(content, fg_color="#252525")
button_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ne")

# Create frames for code and visual content
code_frame = ctk.CTkFrame(content, fg_color=DARK_COLOR, width=300, height=300, corner_radius=0)
visual_frame = ctk.CTkFrame(content, fg_color="#252525", width=300, height=300, corner_radius=0)

inner_frame = tk.Frame(visual_frame, bg="#252525")
inner_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(inner_frame, bg="#252525", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Initially show visual frame and hide code frame
visual_frame.grid(row=2, column=0, pady=10, sticky="nsew")
visual_frame.bind("<Button-3>", void_preference)
code_frame.grid_remove()

def toggle_buttons():
    global toggle_visual_or_code, text_code
    if toggle_visual_or_code:
        # If visual button is active, show visual frame and hide code frame
        visual_frame.grid(row=2, column=0, pady=0, sticky="nsew")
        code_frame.grid_remove()
        visual_button.configure(state="disabled", fg_color=ORANGE_PALLETE, text_color=DARK_COLOR)
        code_button.configure(state="normal", fg_color="#2B2B2B", text_color=TEXT_COLOR)
    else:
        # If code button is active, show code frame and hide visual frame
        code_frame.grid(row=2, column=0, pady=0, sticky="nsew")
        visual_frame.grid_remove()
        code_button.configure(state="disabled", fg_color=GREEN_PALLETE, text_color=DARK_COLOR)
        visual_button.configure(state="normal", fg_color="#2B2B2B", text_color=TEXT_COLOR)
        text_code = combine_all_codes()  # Dapatkan gabungan semua kode dari node
        lorem_label.configure(text=text_code)  # Perbarui teks di label

def on_code_button_click():
    global toggle_visual_or_code
    toggle_visual_or_code = False
    toggle_buttons()

def on_visual_button_click():
    global toggle_visual_or_code
    toggle_visual_or_code = True
    toggle_buttons()

def update_preference(event, self):
    # Contoh penggunaan self di dalam fungsi
    for widget in preference_frame.winfo_children():
        widget.destroy()
    
    title = ctk.CTkLabel(master=preference_frame, text="Preferences", font=("Arial", 16, "bold"))
    title.pack(pady=20, padx = 60)

    def update_info(event=None):

        if link is None :
            linken = None
        else :
            linken = link_entry.get()
            
        namen = name_entry.get()
        frameworken = framework_combo.get() # Pilih framework dari combo box atau ambil satu framework
        self.preferences.update_data(namen, frameworken, linken)

    # Buat label baru dengan informasi tentang node
    framework = self.preferences.framework
    selected_framework = self.preferences.selected_framework
    name = self.preferences.name
    link = self.preferences.link

    name_label = ctk.CTkLabel(master=preference_frame, 
                              text="Name:                        ", 
                              font=("Arial", 14))
    name_label.pack(pady=(0,0))
    name_entry = ctk.CTkEntry(master=preference_frame)
    name_entry.insert(0, name)
    name_entry.pack(pady=(0,10))
    
    # Event binding untuk memperbarui data setiap kali teks diubah
    name_entry.bind("<KeyRelease>", update_info)

    framework_label = ctk.CTkLabel(master=preference_frame, text="Framework:                ", font=("Arial", 14))
    framework_label.pack(pady=(10,0))
            
    framework_combo = ctk.CTkComboBox(master=preference_frame, 
                                      values=framework, 
                                      command= update_info)
    
    framework_combo.pack(padx=30,pady=0)
    framework_combo.set(selected_framework)

    if link is not None:
    # lakukan sesuatu jika link tidak None
        link_label = ctk.CTkLabel(master=preference_frame, 
                                  text="Link:                          ", 
                                  font=("Arial", 14))
        link_label.pack(pady=(20, 0))
        link_entry = ctk.CTkEntry(master=preference_frame)
        link_entry.insert(0, link)  # Menampilkan link awal
        link_entry.pack(pady=0)
        # Event binding untuk memperbarui data setiap kali teks diubah
        link_entry.bind("<KeyRelease>", update_info)
    

code_button = ctk.CTkButton(
    master=button_frame,
    text="Code",
    width=80,
    height=30,
    corner_radius=5,
    fg_color=BACKGROUND_COLOR,
    hover_color=GREEN_PALLETE,
    command=on_code_button_click,
    text_color_disabled= DARK_COLOR
)
code_button.grid(row=0, column=0, padx=5, pady=5)

visual_button = ctk.CTkButton(
    master=button_frame,
    text="Visual Programming",
    width=150,
    height=30,
    corner_radius=5,
    fg_color=BACKGROUND_COLOR,
    hover_color=ORANGE_PALLETE,
    command=on_visual_button_click, 
    text_color_disabled= DARK_COLOR
)
visual_button.grid(row=0, column=1, padx=5, pady=5)

# Add copy button to code_frame
def copy_code():
    print(text_code)

# Atur kode frame dengan konfigurasi grid yang sesuai
code_frame.grid_rowconfigure(0, weight=1)  # Atur weight agar tombol tetap di pojok kanan
code_frame.grid_columnconfigure(0, weight=1)  # Atur weight agar tombol tetap di pojok kanan

copy_button = ctk.CTkButton(
    master=code_frame,
    text="Copy",
    width=40,
    height=40,
    corner_radius=5,
    fg_color="#2B2B2B",
    hover_color=SECONDARY_COLOR,
    command=copy_code,
    image = ctk.CTkImage(light_image=Image.open(get_icon_path("copy.png")), size=(20, 20))
)
copy_button.grid(row=0, column=0, padx=5, pady=5, sticky="se")  # Tempelkan tombol ke pojok kanan bawah

def combine_all_codes():
    combined_code = ""
    for node in node_container:
        combined_code += node.code + "\n\n"  # Tambahkan kode dari setiap node dan beri jarak antar kode
    return combined_code

# Add the 'Lorem Ipsum' label to code_frame
lorem_label = ctk.CTkLabel(
    master=code_frame,
    text="",
    font=("Arial", 14, "normal"),
    text_color=TEXT_COLOR, anchor="w",
    justify="left"
      # Align text to the left
)
lorem_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
toggle_buttons()

preference_frame = ctk.CTkFrame(root, width=200, height=500, corner_radius=0)
preference_frame.grid(row=0, column=2, sticky="ns")
void_preference() #initial preference

# Configure columns and rows to allow resizing
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Run the application
root.mainloop()
