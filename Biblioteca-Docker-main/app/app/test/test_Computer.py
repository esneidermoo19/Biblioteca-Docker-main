from app import db
from app.models.computers import Computer


def test_create_computer(app):
    computer = Computer(brandComputer="Lenovo", modelComputer="ThinkCentre M720")
    db.session.add(computer)
    db.session.commit()
    assert computer.idComputer is not None
    assert computer.brandComputer == "Lenovo"
    assert computer.modelComputer == "ThinkCentre M720"
    assert computer.statusComputer == "Active"
    assert computer.computerLoans == []


def test_computer_repr(app):
    computer = Computer(brandComputer="HP", modelComputer="ProDesk 400")
    db.session.add(computer)
    db.session.commit()
    assert repr(computer) == f"<Computer {computer.idComputer} - HP ProDesk 400>"
