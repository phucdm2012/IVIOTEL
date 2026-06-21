from PySide6.QtWidgets import *
import pandas as pd
from .path import PRICE_DATA_PATH
import numpy as np

class Clock:
    def __init__(self, old_value: float, new_value: float, change_clock_value: float | None = 0):
        self.old_value = old_value
        self.new_value = new_value
        self.change_clock_value = change_clock_value

    def get_used_value(self):
        if self.change_clock_value == 0:
            if self.new_value > self.old_value:
                return self.new_value - self.old_value
            else:
                QMessageBox.warning(None, 'Lỗi', 'Số điện mới không được nhỏ hơn số điện cũ.')
                return (self.new_value + (self.old_value - self.new_value)) - self.old_value
        else:
            return (self.new_value + self.change_clock_value) - self.old_value

    def caculate_bill(self):
        pass
    
class ElectricityClock(Clock):
    def __init__(self, old_value: float, new_value: float, change_clock_value: float | None = 0):
        super().__init__(old_value=old_value, new_value=new_value, change_clock_value=change_clock_value)
        try:
            self.data = pd.read_csv(PRICE_DATA_PATH, encoding="utf-8-sig")
        except Exception as e:
            print(f"[ElectricityClock] {e}")

    def get_bill(self):
        return self.caculate_bill()

    def caculate_bill(self):
        try:
            data = pd.DataFrame(self.data)
            data.columns = data.columns.str.strip()

            data['Giới hạn'] = data['Giới hạn'].astype(str).str.strip()
            data['Giới hạn'] = data['Giới hạn'].replace({'None':np.nan, '':np.nan})
            data['Giới hạn'] = pd.to_numeric(data['Giới hạn'], errors='coerce')
            data['Đơn giá'] = pd.to_numeric(data['Đơn giá'], errors='coerce')

            electricity_used = self.get_used_value()
            total = 0
            remaining = electricity_used

            for row in data.itertuples():
                if remaining <= 0:
                    break

                limit = row._2
                price = row._3

                if pd.isna(limit) or remaining < limit:
                    used_in_step = remaining
                else:
                    used_in_step = limit

                total += used_in_step * price
                remaining -= used_in_step

            return total
        except Exception as e:
            print(f"[ElectricityClock] {e}")
