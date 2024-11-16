import json
import os

class Medicine:
    def __init__(self, name, quantity, price, description=""):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.description = description

class MedicineList:
    def __init__(self):
        self.medicines = []
        self.file_path = "medicines.json"
        self.load_medicines_from_file()

    def add_medicine(self, name, quantity, price, description=""):
        self.medicines.append(Medicine(name, quantity, price, description))
        self.save_medicines_to_file()

    def remove_medicine(self, index):
        if 0 <= index < len(self.medicines):
            del self.medicines[index]
            self.save_medicines_to_file()

    def get_medicines(self):
        return self.medicines

    def save_medicines_to_file(self):
        """Зберігає список ліків у файл JSON."""
        medicines_data = [
            {
                "name": med.name,
                "quantity": med.quantity,
                "price": med.price,
                "description": med.description
            }
            for med in self.medicines
        ]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(medicines_data, file, ensure_ascii=False, indent=4)

    def load_medicines_from_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                medicines_data = json.load(file)
                for med_data in medicines_data:
                    medicine = Medicine(
                        name=med_data["name"],
                        quantity=med_data["quantity"],
                        price=med_data["price"],
                        description=med_data.get("description", "")
                    )
                    self.medicines.append(medicine)
        except FileNotFoundError:
            print("Файл medicines.json не знайдено.")
        except json.JSONDecodeError:
            print("Помилка декодування JSON в файлі medicines.json.")
