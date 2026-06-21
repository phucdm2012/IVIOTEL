from .product import ElectricityClock


class Caculator:
    def __init__(self):
        pass

    def caculateElectricityBill(self, new_value: float, old_value: float, change_clock_value: float | None = 0):
        self.electricity_clock = ElectricityClock(old_value, new_value, change_clock_value)
        return self.electricity_clock.caculate_bill()
    
    def caculateElectrictyUsage(self):
        return self.electricity_clock.get_used_value()
