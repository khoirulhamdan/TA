import tkinter as tk
from tkinter import ttk

def hex_to_rgb(hex_color):
    """Mengonversi warna hex ke format RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Mengonversi warna RGB ke format hex."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def add_hex_colors(hex_color1, hex_color2):
    """Menambahkan dua warna hex dan mengembalikannya dalam format hex."""
    rgb1 = hex_to_rgb(hex_color1)
    rgb2 = hex_to_rgb(hex_color2)
    
    # Menambahkan nilai RGB masing-masing
    added_rgb = tuple(min(a + b, 255) for a, b in zip(rgb1, rgb2))
    
    return rgb_to_hex(added_rgb)

def calculate_color():
    """Mengambil input dari user, menghitung hasil, dan menampilkan warna hasilnya."""
    color1 = color1_entry.get()
    color2 = color2_entry.get()
    
    # Validasi input
    if not (color1.startswith('#') and len(color1) == 7) or not (color2.startswith('#') and len(color2) == 7):
        result_label.config(text="Silakan masukkan warna hex yang valid (contoh: #FF5733).")
        result_color_display.config(bg='white')
        return

    result_color = add_hex_colors(color1, color2)
    result_label.config(text=f"Warna hasil penjumlahan: {result_color}")
    result_color_display.config(bg=result_color)

# Membuat jendela utama
root = tk.Tk()
root.title("Penjumlahan Warna Hex")

# Membuat widget
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

color1_label = ttk.Label(frame, text="Warna Hex 1:")
color1_label.grid(row=0, column=0, sticky=tk.W)
color1_entry = ttk.Entry(frame, width=10)
color1_entry.grid(row=0, column=1)

color2_label = ttk.Label(frame, text="Warna Hex 2:")
color2_label.grid(row=1, column=0, sticky=tk.W)
color2_entry = ttk.Entry(frame, width=10)
color2_entry.grid(row=1, column=1)

calculate_button = ttk.Button(frame, text="Hitung", command=calculate_color)
calculate_button.grid(row=2, column=0, columnspan=2)

result_label = ttk.Label(frame, text="Warna hasil penjumlahan:")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

result_color_display = tk.Label(frame, width=20, height=2, relief=tk.RAISED)
result_color_display.grid(row=4, column=0, columnspan=2)

# Menjalankan aplikasi
root.mainloop()
