import customtkinter as ctk
from PIL import Image, ImageTk

def hex_to_rgb(hex_color):
    """Mengonversi warna heksadesimal ke RGB"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def apply_transparency(rgb_color, alpha):
    """Menambahkan transparansi ke warna RGB"""
    return rgb_color + (int(alpha * 255),)

def create_transparent_image(hex_color, alpha, width=100, height=50):
    """
    Mengonversi warna heksadesimal ke RGBA dengan transparansi, lalu membuat gambar dengan transparansi.
    :param hex_color: Warna dalam format heksadesimal.
    :param alpha: Nilai transparansi antara 0 (transparan penuh) dan 1 (opaque penuh).
    :param width: Lebar gambar.
    :param height: Tinggi gambar.
    :return: Gambar dengan warna dan transparansi yang diinginkan.
    """
    rgb_color = hex_to_rgb(hex_color)
    rgba_color = apply_transparency(rgb_color, alpha)
    
    # Buat gambar dengan warna transparan
    img = Image.new("RGBA", (width, height), rgba_color)
    return ImageTk.PhotoImage(img)