import customtkinter as ctk

# Class MyApp untuk menyimpan data
class MyApp:
    def __init__(self, name, frameworks, link):
        self.name = name
        self.frameworks = frameworks  # Daftar framework
        self.link = link

    def update_data(self, name, framework, link):
        """Perbarui data dalam class MyApp"""
        self.name = name
        self.frameworks = [framework] if framework else self.frameworks  # Update framework jika ada
        self.link = link

    def print_info(self):
        """Cetak info yang diperbarui ke konsol"""
        print(f"Name: {self.name}")
        print(f"Link: {self.link}")
        print(f"Framework: {self.frameworks[0]}")  # Cetak framework pertama

# Class GUI menggunakan CustomTkinter
class MyAppGUI(ctk.CTk):
    def __init__(self, app_data):
        super().__init__()
        
        self.app_data = app_data
        self.title("MyApp GUI")
        self.geometry("400x400")

        # Text input untuk memasukkan nama
        self.name_label = ctk.CTkLabel(self, text="Name:", font=("Arial", 14))
        self.name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.insert(0, self.app_data.name)  # Menampilkan nama awal
        self.name_entry.pack(pady=10)
        # Event binding untuk memperbarui data setiap kali teks diubah
        self.name_entry.bind("<KeyRelease>", self.update_info)

        # Combo box untuk menampilkan frameworks jika lebih dari 1
        if len(self.app_data.frameworks) > 1:
            self.framework_label = ctk.CTkLabel(self, text="Framework:", font=("Arial", 14))
            self.framework_label.pack(pady=10)
            
            self.framework_combo = ctk.CTkComboBox(self, values=self.app_data.frameworks, command= self.update_info)
            self.framework_combo.pack(pady=10)
            self.framework_combo.set(self.app_data.frameworks[0])  # Set default pilihan pertama
        else:
            self.framework_label = ctk.CTkLabel(self, text=f"Framework: {self.app_data.frameworks[0]}", font=("Arial", 14))
            self.framework_label.pack(pady=10)
            self.framework_combo = None  # Tidak ada combo box jika hanya ada 1 framework

        # Text input untuk memasukkan link
        self.link_label = ctk.CTkLabel(self, text="Link:", font=("Arial", 14))
        self.link_label.pack(pady=10)
        self.link_entry = ctk.CTkEntry(self)
        self.link_entry.insert(0, self.app_data.link)  # Menampilkan link awal
        self.link_entry.pack(pady=10)
        # Event binding untuk memperbarui data setiap kali teks diubah
        self.link_entry.bind("<KeyRelease>", self.update_info)

        # Tombol untuk mencetak informasi dari class MyApp
        self.print_button = ctk.CTkButton(self, text="Print Info", command=self.app_data.print_info)
        self.print_button.pack(pady=20)

    # Fungsi untuk memperbarui data di MyApp secara otomatis setiap ada perubahan input
    def update_info(self, event=None):
        name = self.name_entry.get()
        link = self.link_entry.get()
        framework = self.framework_combo.get() if self.framework_combo else self.app_data.frameworks[0]  # Pilih framework dari combo box atau ambil satu framework
        self.app_data.update_data(name, framework, link)

# Inisialisasi objek MyApp
app = MyApp("My Application", ["CustomTkinter", "Tkinter", "PyQt"], "http://example.com")

# Inisialisasi dan menjalankan GUI
if __name__ == "__main__":
    gui = MyAppGUI(app)
    gui.mainloop()
