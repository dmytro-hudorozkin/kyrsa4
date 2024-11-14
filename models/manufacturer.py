# pharmacy_app/models/manufacturer.py

class Manufacturer:
    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country

    def __str__(self):
        return f"Виробник: {self.name}, Країна: {self.country}"
