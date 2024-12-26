import tkinter as tk
import secrets
import string
import pyperclip
import qrcode
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

# Функция для генерации пароля
def generate_password(length=12, use_digits=True, use_letters=True, use_specials=True):
    alphabet = ''
    if use_digits:
        alphabet += string.digits
    if use_letters:
        alphabet += string.ascii_letters
    if use_specials:
        alphabet += string.punctuation

    if not alphabet:
        return "Ошибка: выберите хотя бы один параметр!"
    
    return ''.join(secrets.choice(alphabet) for i in range(length))

# Оценка надежности пароля
def evaluate_strength(password):
    score = 0
    if len(password) >= 12:
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    if score == 4:
        return "Очень надежный"
    elif score == 3:
        return "Надежный"
    elif score == 2:
        return "Средний"
    else:
        return "Слабый"

# Функция для генерации QR-кода
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Функция для отображения QR-кода в новом окне
def show_qr_code():
    password = label_password.cget("text")
    if password and not password.startswith("Ошибка"):
        qr_img = generate_qr_code(password)
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        # Создаем новое окно для QR-кода
        qr_window = tk.Toplevel(root)
        qr_window.title("QR Код")
        
        label_qr = tk.Label(qr_window, image=qr_photo)
        label_qr.image = qr_photo  # Сохраняем ссылку на изображение
        label_qr.pack(padx=10, pady=10)

        qr_window.geometry(f"{qr_img.size[0] + 20}x{qr_img.size[1] + 20}")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, сгенерируйте пароль сначала.")

# Функция для сохранения пароля в файл с выбором пути
def save_password():
    password = label_password.cget("text")
    if password and not password.startswith("Ошибка"):
        # Открытие диалога для выбора пути сохранения файла
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "a") as file:
                file.write(f"{password}\n")
            messagebox.showinfo("Успех", f"Пароль успешно сохранен в файл: {file_path}")
        else:
            messagebox.showwarning("Отмена", "Сохранение пароля было отменено.")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, сгенерируйте пароль для сохранения.")

# Функция для копирования пароля в буфер обмена
def copy_to_clipboard():
    password = label_password.cget("text")
    if password and not password.startswith("Ошибка"):
        pyperclip.copy(password)
        label_password.config(text="Пароль скопирован!")

# Функция для обработки генерации пароля
def on_generate():
    try:
        length = int(entry_length.get())
        use_digits = var_digits.get()
        use_letters = var_letters.get()
        use_specials = var_specials.get()
        password = generate_password(length, use_digits, use_letters, use_specials)
        label_password.config(text=password)
        
        # Оценка надежности пароля
        strength = evaluate_strength(password)
        label_strength.config(text=f"Надежность: {strength}")

        add_to_history(password)
    except ValueError:
        label_password.config(text="Ошибка: введите корректное число.")

# Функция для добавления пароля в историю
def add_to_history(password):
    history.insert(0, password)
    text_history.delete('1.0', tk.END)
    for i, pw in enumerate(history):
        text_history.insert(tk.END, f"{i + 1}. {pw}\n")

# Функция для переключения темы
def toggle_theme():
    global current_theme
    if current_theme == 'light':
        root.config(bg="#2e2e2e")
        frame_options.config(bg="#2e2e2e", highlightbackground="#444", highlightcolor="#444")
        label_length.config(bg="#2e2e2e", fg="#ffffff")
        entry_length.config(bg="#444444", fg="#ffffff", insertbackground="#ffffff")
        button_generate.config(bg="#555555", fg="#ffffff")
        button_copy.config(bg="#555555", fg="#ffffff")
        button_toggle_theme.config(bg="#555555", fg="#ffffff")
        label_password.config(bg="#2e2e2e", fg="#ffffff")
        label_strength.config(bg="#2e2e2e", fg="#ffffff")
        label_history.config(bg="#2e2e2e", fg="#ffffff")
        text_history.config(bg="#444444", fg="#ffffff", insertbackground="#ffffff")
        var_digits.set(True)
        current_theme = 'dark'
    else:
        root.config(bg="#ffffff")
        frame_options.config(bg="#ffffff", highlightbackground="#ccc", highlightcolor="#ccc")
        label_length.config(bg="#ffffff", fg="#000000")
        entry_length.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
        button_generate.config(bg="#f0f0f0", fg="#000000")
        button_copy.config(bg="#f0f0f0", fg="#000000")
        button_toggle_theme.config(bg="#f0f0f0", fg="#000000")
        label_password.config(bg="#ffffff", fg="#000000")
        label_strength.config(bg="#ffffff", fg="#000000")
        label_history.config(bg="#ffffff", fg="#000000")
        text_history.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
        current_theme = 'light'

# Инициализация главного окна
root = tk.Tk()
root.title('Генератор паролей')
root.geometry("400x651")
root.resizable(False, False)

# Переменные темы и истории
current_theme = 'light'
history = []

# Опции для генерации пароля
frame_options = tk.Frame(root, bd=2, relief=tk.GROOVE, padx=10, pady=10)
frame_options.pack(pady=10)

label_length = tk.Label(frame_options, text="Длина пароля:")
label_length.grid(row=0, column=0, sticky="w")
entry_length = tk.Entry(frame_options, width=5)
entry_length.insert(0, "12")
entry_length.grid(row=0, column=1)

var_digits = tk.BooleanVar(value=True)
check_digits = tk.Checkbutton(frame_options, text="Использовать цифры", variable=var_digits)
check_digits.grid(row=1, column=0, sticky="w")

var_letters = tk.BooleanVar(value=True)
check_letters = tk.Checkbutton(frame_options, text="Использовать буквы", variable=var_letters)
check_letters.grid(row=1, column=1, sticky="w")

var_specials = tk.BooleanVar(value=True)
check_specials = tk.Checkbutton(frame_options, text="Использовать спецсимволы", variable=var_specials)
check_specials.grid(row=2, column=0, sticky="w")

# Кнопка генерации пароля
button_generate = tk.Button(root, text="Генерировать", command=on_generate)
button_generate.pack(pady=10)

# Отображение пароля
label_password = tk.Label(root, text="", font=("Helvetica", 14))
label_password.pack(pady=10)

# Отображение надежности пароля
label_strength = tk.Label(root, text="Надежность: ", font=("Helvetica", 12))
label_strength.pack(pady=5)

# Кнопка копирования
button_copy = tk.Button(root, text="Копировать", command=copy_to_clipboard)
button_copy.pack(pady=10)

# Кнопка сохранения пароля
button_save = tk.Button(root, text="Сохранить пароль", command=save_password)
button_save.pack(pady=10)

# Кнопка генерации QR-кода в отдельном окне
button_show_qr = tk.Button(root, text="Показать QR Код", command=show_qr_code)
button_show_qr.pack(pady=10)

# Кнопка переключения темы
button_toggle_theme = tk.Button(root, text="Переключить тему", command=toggle_theme)
button_toggle_theme.pack(pady=10)

# История паролей
label_history = tk.Label(root, text="История паролей:")
label_history.pack(pady=5)
text_history = tk.Text(root, height=10, state=tk.NORMAL)
text_history.pack(pady=5, padx=10)

# Добавление текста в нижний левый угол
label_footer = tk.Label(root, text="Created by Apathy", font=("Helvetica", 7), anchor="w")
label_footer.pack(side="bottom", anchor="w", padx=10, pady=5)

# Установка начальной темы
toggle_theme()

# Запуск приложения
root.mainloop()
