import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import string
import pyqrcode
from PIL import Image, ImageTk
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Генератор паролей")
        self.geometry("400x550")
        self.resizable(False, False)

        self.password_list = []  # Список для сохранения паролей

        # Путь к иконке
        self.icon_path = r"C:\Users\Apathy\Desktop\11\3333.ico"
        
        # Печать пути иконки для проверки
        print("Путь к иконке:", self.icon_path)

        # Устанавливаем иконку для основного окна через Tkinter
        try:
            self.iconbitmap(self.icon_path)  # Для основного окна
            print("Иконка для основного окна установлена.")
        except Exception as e:
            print("Ошибка при установке иконки в основном окне:", e)

        # Путь к шрифту
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'SanFranciscoProText-SemiBoldItalic.ttf')

        # Загрузка кастомного шрифта с помощью CTkFont
        try:
            self.custom_font = ctk.CTkFont(family=font_path, size=14)
        except:
            # Если не удалось загрузить, используем стандартный шрифт
            self.custom_font = ("Arial", 14)

        self.label = ctk.CTkLabel(self, text="Генератор паролей by apathy", font=self.custom_font)
        self.label.pack(pady=10)

        self.length_label = ctk.CTkLabel(self, text="Длина:", font=self.custom_font)
        self.length_label.pack()

        self.length_entry = ctk.CTkEntry(self, width=50, font=self.custom_font)
        self.length_entry.insert(0, "12")
        self.length_entry.pack(pady=5)

        self.numbers_var = tk.BooleanVar()
        self.letters_var = tk.BooleanVar()
        self.specials_var = tk.BooleanVar()

        self.numbers_switch = ctk.CTkSwitch(self, text="Цифры", variable=self.numbers_var, onvalue=True, offvalue=False, fg_color="#03fca1")
        self.numbers_switch.pack()

        self.letters_switch = ctk.CTkSwitch(self, text="Буквы", variable=self.letters_var, onvalue=True, offvalue=False, fg_color="#03fca1")
        self.letters_switch.pack()

        self.specials_switch = ctk.CTkSwitch(self, text="Спецсимволы", variable=self.specials_var, onvalue=True, offvalue=False, fg_color="#03fca1")
        self.specials_switch.pack()

        self.generate_button = ctk.CTkButton(self, text="Генерировать", command=self.generate_password, fg_color="#03fca1", text_color="black")
        self.generate_button.pack(pady=10)

        self.password_output = ctk.CTkTextbox(self, height=100, width=300, font=self.custom_font)
        self.password_output.pack(pady=10)

        self.copy_button = ctk.CTkButton(self, text="Копировать", command=self.copy_password, fg_color="#03fca1", text_color="black")
        self.copy_button.pack(pady=5)

        self.save_button = ctk.CTkButton(self, text="Сохранить", command=self.save_password, fg_color="#03fca1", text_color="black")
        self.save_button.pack(pady=5)

        self.qr_button = ctk.CTkButton(self, text="Показать QR-код", command=self.show_qr, fg_color="#03fca1", text_color="black")
        self.qr_button.pack(pady=5)

    def generate_password(self):
        length = int(self.length_entry.get())
        characters = ""

        if self.numbers_var.get():
            characters += string.digits
        if self.letters_var.get():
            characters += string.ascii_letters
        if self.specials_var.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Ошибка", "Выберите хотя бы один параметр!")
            return

        password = "".join(random.choice(characters) for _ in range(length))
        self.password_list.append(password)

        self.password_output.delete("1.0", "end")
        self.password_output.insert("1.0", "\n".join(self.password_list))

    def copy_password(self):
        password = self.password_output.get("1.0", "end").strip()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update()
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

    def save_password(self):
        # Определяем путь для сохранения файла
        file_path = os.path.join(os.path.expanduser("~"), "Documents", "saved_passwords.txt")
        
        try:
            # Сохраняем пароль в файл
            with open(file_path, "w") as file:
                file.write("\n".join(self.password_list))
            
            # Выводим сообщение об успехе с полным путем
            messagebox.showinfo("Успех", f"Пароли сохранены в файл:\n{file_path}")
            print(f"Пароли сохранены в файл: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def show_qr(self):
        password = self.password_output.get("1.0", "end").strip()
        if not password:
            messagebox.showerror("Ошибка", "Нет пароля для генерации QR-кода")
            return

        qr = pyqrcode.create(password)
        qr_image_path = "qr_code.png"
        qr.png(qr_image_path, scale=5)

        qr_image = Image.open(qr_image_path)
        qr_image = qr_image.resize((250, 250), Image.Resampling.LANCZOS)

        # Создание окна с QR-кодом
        qr_window = ctk.CTkToplevel(self)
        qr_window.title("QR-код пароля")
        qr_window.geometry("300x300")
        qr_window.resizable(False, False)

        # Позиционирование окна чуть выше основного
        main_x = self.winfo_x()  # Получаем X-координату основного окна
        main_y = self.winfo_y()  # Получаем Y-координату основного окна
        qr_window.geometry(f"+{main_x + 50}+{main_y - 100}")  # Позиционируем окно с учетом смещения

        # Устанавливаем иконку для окна с QR-кодом через iconphoto
        try:
            qr_icon = Image.open(self.icon_path)
            qr_icon = qr_icon.resize((16, 16))  # Размер иконки для окна
            qr_icon = ImageTk.PhotoImage(qr_icon)
            qr_window.iconphoto(True, qr_icon)  # Используем iconphoto для установки иконки
            print("Иконка для окна QR установлена.")
        except Exception as e:
            print("Ошибка при установке иконки для окна QR:", e)

        qr_photo = ImageTk.PhotoImage(qr_image)

        qr_label = tk.Label(qr_window, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(expand=True)

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
