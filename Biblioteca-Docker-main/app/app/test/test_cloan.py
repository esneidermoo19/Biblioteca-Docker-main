from datetime import datetime
from app import db
from app.models.cloans import ComputerLoan
from app.models.computers import Computer


def test_create_computer_loan(app, user):
    computer = Computer(brandComputer="Dell", modelComputer="OptiPlex 3080")
    db.session.add(computer)
    db.session.commit()
    cloan = ComputerLoan(computer=computer, user=user)
    db.session.add(cloan)
    db.session.commit()
    assert cloan.idLoan is not None
    assert cloan.status == "Active"
    assert cloan.loanDate is not None
    assert cloan.returnDate is None
    assert cloan.computerId == computer.idComputer
    assert cloan.userId == user.idUser
    assert cloan.computer == computer
    assert cloan.user == user
    assert cloan in computer.computerLoans
    assert cloan in user.computerLoansUser.all()


def test_computer_loan_repr(app, user):
    computer = Computer(brandComputer="Asus", modelComputer="ExpertCenter")
    db.session.add(computer)
    db.session.commit()
    cloan = ComputerLoan(computer=computer, user=user)
    db.session.add(cloan)
    db.session.commit()
    assert repr(cloan) == f"<ComputerLoan {cloan.idLoan} of Computer {computer.idComputer} to User {user.idUser}>"


def test_computer_loan_update_status(app, user):
    computer = Computer(brandComputer="Acer", modelComputer="Veriton")
    db.session.add(computer)
    db.session.commit()
    cloan = ComputerLoan(computer=computer, user=user)
    db.session.add(cloan)
    db.session.commit()
    cloan.status = "Returned"
    cloan.returnDate = datetime.now()
    db.session.commit()
    assert cloan.status == "Returned"
    assert cloan.returnDate is not None
