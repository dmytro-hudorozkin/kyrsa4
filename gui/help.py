import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class HelpWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Допомога")
        self.root.configure(bg="#3e0069")  # Фіолетовий фон

        # Задаємо розмір вікна і розташовуємо його по центру
        window_width, window_height = 520, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Створення фрейму з прокруткою
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame, bg="#3e0069")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Додавання прокрутки колесом миші
        canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(canvas, event))

        help_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=help_frame, anchor="nw")

        # Додавання фотографій і описів
        self.add_help_content(help_frame)

    def add_help_content(self, frame):
        images_info = [
            ("images/help1.png", "Головне меню \n -------------------------\n Кнопка 'Склад - відкриває інтерфейс управління складом. Тут можна переглядати наявні ліки, редагувати інформацію про них, додавати нові медикаменти, видаляти ті, що більше не потрібні, а також здійснювати пошук за назвою. \n \n Кнопка 'Замовлення' - відкриває інтерфейс для створення та перегляду замовлень на поповнення складу ліків. Можна додати медикаменти до замовлення, вказавши кількість, а також підтвердити вже створені замовлення. \n \n Кнопка 'Допомога' - відкриває це вікно з інформацією про використання програми.  \n \n Кнопка 'Вийти' - закриває програму. \n --------------------------------------------------------------------------------------------"),
            ("images/help2.png", "Меню 'Склад'\n -------------------------\n Меню 'Склад' надає доступ до таблиці з наявними медикаментами.\n Тут можна побачити таблицю, яка містить інформацію про наявні медикаменти: назва, кількість, ціна та опис. За допомогою цієї таблиці можна швидко переглядати наявність ліків та їхні властивості. \n Також доступні опції для додавання нових ліків, редагування інформації про існуючі медикаменти а також видалення з бази даних тих, що більше не потрібні.\n\n  Кнопка 'Додати' у розділі 'Склад' - дозволяє додати нові ліки до складу. Відкривається форма, в яку необхідно ввести назву ліків, кількість, ціну та опис. \n \n Кнопка 'Видалити' - дозволяє видалити обрані медикаменти зі складу. Ви можете обрати кілька рядків у таблиці і видалити їх. \n \n  Кнопка 'Замовлення приїхало' - дозволяє поповнити склад на основі попередньо підтвердженого замовлення. \n --------------------------------------------------------------------------------------------"),
            ("images/help3.png", "Бланк для додавання ліків. \n -------------------------\n Тут заповнюється інформація про препарат та додається до таблиці за допомогою кнопки 'Зберегти' \n --------------------------------------------------------------------------------------------"),
            ("images/help4.png", "Меню 'Замовлення' \n -------------------------\n Меню 'Замовлення' дозволяє створювати нові замовлення для поповнення запасів медикаментів. \n Тут можна переглянути поточні замовлення, відредагувати деталі замовлення або скасувати його у разі необхідності. \n Це допомагає гарантувати, що всі ліки завжди є в наявності та своєчасно поповнюються. \n \n Кнопка 'Підтвердити замовлення' - дозволяє зберегти замовлення на поповнення складу, після чого вони можуть бути виконані. \n \n Кнопка 'Додати товар в замовлення' - дозволяє обрати товар зі складу і вказати кількість для замовлення. \n \n Кнопка 'Назад' - повертає користувача до головного меню з будь-якого іншого розділу. \n --------------------------------------------------------------------------------------------"),
        ]

        for idx, (img_path, description) in enumerate(images_info, start=1):
            # Завантаження зображення та зміна його розміру
            image = Image.open(img_path)
            image.thumbnail((400, 300))  # Зміна розміру зображення
            photo = ImageTk.PhotoImage(image)

            # Додавання рамки для зображення
            image_label_frame = ttk.Frame(frame, style="Image.TFrame")
            image_label_frame.pack(pady=10)

            # Додавання зображення з рамкою
            image_label = ttk.Label(image_label_frame, image=photo)
            image_label.image = photo
            image_label.pack(padx=10, pady=10)

            # Додавання тексту під фото
            description_label = tk.Label(frame, text=description, font=("Calibri", 12), wraplength=500, justify="center", fg="white", bg="#3e0069")
            description_label.pack(pady=(0, 20))

    def _on_mousewheel(self, canvas, event):
        canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    help_window = HelpWindow(root)
    root.mainloop()
