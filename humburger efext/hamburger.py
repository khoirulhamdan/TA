import tkinter as tk
import customtkinter as ctk

# Inisialisasi jendela utama
root = ctk.CTk()
root.geometry("1440x900")
root.title("Hamburger Menu Effect with Main Frame")

# Frame utama
main_frame = ctk.CTkFrame(root, corner_radius=10, width=1440, height=900)
main_frame.pack(fill="both", expand=True)

# Fungsi untuk membuat fitur hamburger yang berhenti di jarak tertentu dari tombol
def create_hamburger_menu(parent_frame, menu_width=210, button_width=30, speed=10):
    # Variabel untuk mengatur status menu
    menu_open = False

    # Posisi akhir ketika menutup (berhenti pada jarak tambahan 20px dari tombol hamburger)
    stop_position = button_width + 20

    # Frame untuk menu (sidebar)
    menu_frame = ctk.CTkFrame(parent_frame, corner_radius=0, width=menu_width, height=900)
    menu_frame.place(x=-menu_width + stop_position, y=0)  # Posisi awal sedikit terlihat (di belakang tombol)

    # Fungsi untuk menggerakkan menu frame dengan animasi slide
    def animate_menu(target_x):
        current_x = menu_frame.winfo_x()
        if current_x != target_x:
            direction = 1 if target_x > current_x else -1
            new_x = current_x + direction * speed
            if abs(target_x - new_x) < speed:
                new_x = target_x
            menu_frame.place(x=new_x, y=0)
            parent_frame.after(10, lambda: animate_menu(target_x))

    # Fungsi untuk membuka/menutup menu
    def toggle_menu():
        nonlocal menu_open
        if menu_open:
            animate_menu(-menu_width + stop_position)  # Menu berhenti di posisi tombol + 20px
            menu_open = False
        else:
            menu_frame.place(x=-menu_width + stop_position, y=0)  # Pastikan menu berada sedikit di belakang tombol
            animate_menu(0)  # Menu slide masuk
            menu_open = True

    # Tombol untuk membuka/menutup menu
    hamburger_button = ctk.CTkButton(parent_frame, text="☰", command=toggle_menu, width=button_width, height=30)
    hamburger_button.place(x=10, y=10)  # Posisi tombol hamburger di parent_frame

    return menu_frame  # Kembalikan menu_frame jika ingin menambahkan lebih banyak elemen ke menu

# Membuat hamburger menu di main_frame
menu_frame = create_hamburger_menu(main_frame)

# Konten di frame utama
content_label = ctk.CTkLabel(main_frame, text="Konten Utama", font=("Arial", 24))
content_label.place(x=300, y=100)  # Tambahkan konten di main_frame

root.mainloop()
