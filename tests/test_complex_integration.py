from src.manager import Manager
from src.models import Apartment, Bill, Parameters

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
            date_due="2026-11-16",
            apartment="A1",
            settlement_year=2026,
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
    
    assert manager.get_apartment_costs("A1", 2026, 11) == 500.0
    assert manager.get_apartment_costs("A1", 2026, 10) == 0.0
    assert manager.get_apartment_costs("A2", 2026, 11) is None