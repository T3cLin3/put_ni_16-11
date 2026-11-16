from src.manager import Manager
from src.models import Apartment, Bill, Parameters, ApartmentSettlement
import pytest

def test_get_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)
    
    manager.apartments = {
        "A1": Apartment(
            key="A1",
            name="Apartment 1",
            location="Radom",
            area_m2="21.37",
            rooms={
                "r1": {
                    "name": "Sypialnio-kuchnio-salon",
                    "area_m2": 19
                },
                "r2": {
                    "name": "Lazienka",
                    "area_m2": 2.37
                }
            }
        )
    }
    
    manager.bills = [
        Bill(
            amount_pln=167.0,
            date_due="2026-11-16",
            apartment="A1",
            settlement_year=2026,
            settlement_month=11,
            type="Prąd"
        ),
        Bill(
            amount_pln=250.0,
            date_due="2025-11-16",
            apartment="A1",
            settlement_year=2025,
            settlement_month=11,
            type="Czynsz"
        ),
        Bill(
            amount_pln=333.0,
            date_due="2026-12-16",
            apartment="A1",
            settlement_year=2026,
            settlement_month=12,
            type="Prąd"
        ),
    ]
    
    assert manager.get_apartment_costs("A1", 2026, 11) == 167.0
    assert manager.get_apartment_costs("A1", 2026, 10) == 0.0
    assert manager.get_apartment_costs("A2", 2026, 11) is None
    assert manager.get_apartment_costs("A1", 2026) == 500.0
    assert manager.get_apartment_costs("A1") == 750.0
    with pytest.raises(ValueError):
        manager.get_apartment_costs("A1", 2026, 13)
    with pytest.raises(ValueError):
        manager.get_apartment_costs("A1", 2026, 0)


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0

def test_create_apartment_settlement():
    manager = Manager(Parameters())

    manager.apartments = {
        "A1": Apartment(
            key="A1",
            name="Apartament 1",
            location="Centrum",
            area_m2=50.0,
            rooms={"r1": {"name": "Salon", "area_m2": 50.0}},
        )
    }

    manager.bills = [
        Bill(
            amount_pln=150.0,
            date_due="2024-03-10",
            apartment="A1",
            settlement_year=2024,
            settlement_month=3,
            type="Prąd",
        ),
        Bill(
            amount_pln=250.0,
            date_due="2024-03-15",
            apartment="A1",
            settlement_year=2024,
            settlement_month=3,
            type="Gaz",
        ),
    ]

    settlement_with_bills = manager.create_apartment_settlement("A1", 2024, 3)
    assert settlement_with_bills is not None
    assert isinstance(settlement_with_bills, ApartmentSettlement)
    assert settlement_with_bills.apartment == "A1"
    assert settlement_with_bills.year == 2024
    assert settlement_with_bills.month == 3
    assert settlement_with_bills.total_rent_pln == 0.0
    assert settlement_with_bills.total_bills_pln == 400.0
    assert settlement_with_bills.total_due_pln == 400.0

    settlement_no_bills = manager.create_apartment_settlement("A1", 2024, 4)
    assert settlement_no_bills is not None
    assert isinstance(settlement_no_bills, ApartmentSettlement)
    assert settlement_no_bills.apartment == "A1"
    assert settlement_no_bills.year == 2024
    assert settlement_no_bills.month == 4
    assert settlement_no_bills.total_rent_pln == 0.0
    assert settlement_no_bills.total_bills_pln == 0.0
    assert settlement_no_bills.total_due_pln == 0.0

    assert manager.create_apartment_settlement("NIEISTNIEJACE", 2024, 3) is None
