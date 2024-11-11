import tkinter as tk
from PIL import ImageTk, Image, ImageColor

def create_button(root, color_hex, text="", alpha=int(255 * 0.5), width=100, height=30):
    """Membuat tombol dengan gambar transparan sebagai latar belakang dan teks."""
    transparent_image = create_transparent_image(color_hex, alpha, width, height)
    tk_image = ImageTk.PhotoImage(transparent_image)
    
    button = tk.Button(root, image=tk_image, text=text, compound="center", 
                       font=("Arial", 10), relief="flat", borderwidth=0, 
                       fg="black", padx=10, pady=5)
    
    button.image = tk_image  # Simpan referensi untuk mencegah penghapusan gambar
    button.pack(padx=20, pady=20)
    
    return button

def create_transparent_image(color_hex, alpha, width=100, height=30):
    """Membuat gambar dengan warna dan transparansi yang ditentukan."""
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rgba_color = ImageColor.getrgb(color_hex) + (alpha,)
    for x in range(width):
        for y in range(height):
            image.putpixel((x, y), rgba_color)
    return image
