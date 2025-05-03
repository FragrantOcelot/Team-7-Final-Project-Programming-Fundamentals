from ticket import Ticket

# Single race pass
class SingleRaceTicket(Ticket):
    def __init__(self):
        super().__init__(
            name="Single Race Pass",
            price=300.0,
            validity="One Day",
            features=["Access to one race", "Grandstand seat"]
        )

# Weekend package
class WeekendPackage(Ticket):
    def __init__(self):
        super().__init__(
            name="Weekend Package",
            price=750.0,
            validity="Three Days",
            features=["Access to all races of the weekend", "Premium seating", "Fan zone access"]
        )

# Full season pass
class SeasonPass(Ticket):
    def __init__(self):
        super().__init__(
            name="Season Pass",
            price=4000.0,
            validity="All Season",
            features=["All races", "VIP lounge", "Priority parking", "Merch pack"]
        )

# Group discount ticket (for 4+ people)
class GroupDiscountTicket(Ticket):
    def __init__(self, group_size):
        discount_price = max(250.0, 300.0 - group_size * 5)  # discount per person
        super().__init__(
            name=f"Group Ticket ({group_size} people)",
            price=discount_price * group_size,
            validity="One Day",
            features=["Group access", "Discounted entry", "Adjacent seating"]
        )
        self.__group_size = group_size

    def get_group_size(self):
        return self.__group_size
