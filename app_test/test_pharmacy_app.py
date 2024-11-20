import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from models.medicine import Medicine
from models.medicine_list import MedicineList
from gui.interface import PharmacyAppInterface
import tkinter as tk

@pytest.fixture
def temporary_medicine_file():
    file_path = "test_medicines.json"
    if os.path.exists(file_path):
        os.remove(file_path)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.fixture
def medicine_list(temporary_medicine_file):
    med_list = MedicineList()
    med_list.file_path = temporary_medicine_file
    med_list.medicines = []
    return med_list

@pytest.fixture
def sample_medicine():
    return Medicine(name="Парацетамол", quantity=10, price=100.0, description="Знеболювальне")

def test_add_medicine(medicine_list, sample_medicine):
    initial_count = len(medicine_list.get_medicines())
    medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    assert len(medicine_list.get_medicines()) == initial_count + 1
    assert medicine_list.get_medicines()[-1].name == "Парацетамол"

def test_remove_medicine(medicine_list, sample_medicine):
    medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    initial_count = len(medicine_list.get_medicines())
    medicine_list.remove_medicine(0)
    assert len(medicine_list.get_medicines()) == initial_count - 1

def test_save_and_load_medicines(medicine_list, sample_medicine, temporary_medicine_file):
    medicine_list.medicines.clear()
    medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    medicine_list.save_medicines_to_file()

    new_medicine_list = MedicineList()
    new_medicine_list.file_path = temporary_medicine_file
    new_medicine_list.load_medicines_from_file()
    loaded_medicine = new_medicine_list.get_medicines()[0]

    assert loaded_medicine.name == sample_medicine.name
    assert loaded_medicine.quantity == sample_medicine.quantity
    assert loaded_medicine.price == sample_medicine.price
    assert loaded_medicine.description == sample_medicine.description

@pytest.fixture
def app_interface():
    root = tk.Tk()
    app = PharmacyAppInterface(root, medicines_file_path="test_medicines.json")
    app.medicine_list.medicines = []
    return app

def test_add_medicine_row(app_interface, sample_medicine):
    app_interface.open_stock_page() 
    initial_count = len(app_interface.medicine_list.get_medicines())
    app_interface.medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    app_interface.load_medicines_to_table()
    
    assert len(app_interface.medicine_list.get_medicines()) == initial_count + 1
    assert app_interface.medicine_list.get_medicines()[-1].name == "Парацетамол"

def test_search_medicine(app_interface, sample_medicine):
    app_interface.open_stock_page()
    app_interface.medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    app_interface.load_medicines_to_table()
    
    app_interface.search_medicine("Парацетамол")
    filtered_medicines = [app_interface.stock_table.item(item)["values"][0] for item in app_interface.stock_table.get_children()]
    
    assert "Парацетамол" in filtered_medicines

def test_save_and_confirm_order(app_interface, sample_medicine):
    app_interface.open_order_page()
    app_interface.medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    app_interface.save_medicines_to_file()
    
    app_interface.order_file_path = "test_orders.json"
    
    app_interface.order_table.insert("", "end", values=(sample_medicine.name, sample_medicine.quantity, 5))
    assert app_interface.order_table.get_children()

    if os.path.exists("test_orders.json"):
        os.remove("test_orders.json")

def test_replenish_stock_from_order(app_interface, sample_medicine):
    app_interface.medicine_list.medicines.clear()
    app_interface.medicine_list.add_medicine(sample_medicine.name, sample_medicine.quantity, sample_medicine.price, sample_medicine.description)
    
    app_interface.open_stock_page()

    app_interface.order_file_path = "test_orders.json"
    
    order_data = [{"name": sample_medicine.name, "order_qty": 5}]
    with open(app_interface.order_file_path, "w", encoding="utf-8") as f:
        json.dump(order_data, f, ensure_ascii=False, indent=4)
    
    app_interface.replenish_stock_from_order()
    
    replenished_medicine = next((med for med in app_interface.medicine_list.get_medicines() if med.name == sample_medicine.name), None)
    assert replenished_medicine.quantity == 15 

    if os.path.exists(app_interface.order_file_path):
        os.remove(app_interface.order_file_path)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_medicines_file():
    yield
    if os.path.exists("test_medicines.json"):
        os.remove("test_medicines.json")