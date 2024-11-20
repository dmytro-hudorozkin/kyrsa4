class Supplier:
    def __init__(self, name: str, contact_info: str):
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Постачальник: {self.name}, Контакт: {self.contact_info}"
