import customtkinter as ctk

# Create the main window
app = ctk.CTk()
app.geometry("400x300")

# Create a frame to hold the scrollable content
frame = ctk.CTkFrame(app)
frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

# Create a canvas widget for scrolling
canvas = ctk.CTkCanvas(frame)
canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

# Create a scrollbar and link it to the canvas
scrollbar = ctk.CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create another frame to hold the content inside the canvas
content_frame = ctk.CTkFrame(canvas)

# Create a window inside the canvas to contain the content frame
canvas.create_window((0, 0), window=content_frame, anchor='nw')

# Add content to the content frame (example with multiple buttons)
for i in range(50):
    button = ctk.CTkButton(content_frame, text=f"Button {i+1}")
    button.pack(pady=5)

# Update the scroll region of the canvas when the content frame is resized
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", on_frame_configure)

# Start the application
app.mainloop()
