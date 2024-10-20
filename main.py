from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime

ShiftId = int


class IShift(ABC):
    @abstractmethod
    def attach(self, member: IMember):
        pass

    @abstractmethod
    def detach(self, member: IMember):
        pass

    @abstractmethod
    def notify(self):
        pass


class Shift:
    def __init__(self, shift_at: datetime):
        self.shift_at = shift_at
        self._members: set[IMember] = set()

    # @property
    # def shift_at(self) -> datetime:
    #     if self._shift_at is None:
    #         raise ValueError('Shift at is not set!')
    #     return self._shift_at

    # @shift_at.setter
    # def shift_at(self, shift_at: datetime):
    #     self._shift_at = shift_at

    def attach(self, member: IMember):
        self._members.add(member)

    def detach(self, member: IMember):
        self._members.remove(member)

    def notify(self):
        for member in self._members:
            member.update(self)

    def main(self):
        self.notify()

    def __repr__(self) -> str:
        return f'Shift at: {self.shift_at}\nShift members: {list(self._members)}'


class IMember(ABC):
    @abstractmethod
    def update(self, shift: Shift) -> None:
        pass


class User(IMember):
    def __init__(self, name: str):
        self.name: str = name

    def update(self, shift: Shift) -> None:
        print(f'{self.name} has been notified about the shift on {shift.shift_at}!')

    def __repr__(self) -> str:
        return self.name


class ZavodHandler:
    _last_pk = 0
    _shifts: dict[ShiftId, Shift] = {}

    def _get_shift_date(self, msg: str = 'Enter shift date: ') -> date | None:
        input_date = input(msg)
        if input_date:
            try:
                return datetime.strptime(input_date, '%Y-%m-%d')
            except ValueError:
                return None
        else:
            return None

    def _get_shift_hour(self, msg: str = 'Enter shift hour: ') -> int | None:
        input_hour = input(msg)
        if input_hour and int(input_hour) < 24:
            return int(input_hour)
        else:
            return None

    def _get_shift_minute(self, msg: str = 'Enter shift minute: ') -> int | None:
        input_minute = input(msg)
        if input_minute and int(input_minute) < 60:
            return int(input_minute)
        else:
            return None

    def add_shift(self):
        shift_date = self._get_shift_date()
        shift_hour = self._get_shift_hour()
        shift_minute = self._get_shift_minute()

        if shift_date is None or shift_hour is None or shift_minute is None:
            print('Shift not added!')
            return

        shift_at = datetime(shift_date.year, shift_date.month, shift_date.day, shift_hour, shift_minute)

        shift = Shift(shift_at)

        shift_members = input('Enter shift members: ')
        shift_members = shift_members.split(',')
        for member in shift_members:
            user = User(member)
            shift.attach(user)

        self._last_pk += 1
        self._shifts.update({self._last_pk: shift})

        print('Shift added!')
        shift.main()

    def get_shifts(self):
        print('Shifts:')
        for shift_id, shift in self._shifts.items():
            print(f'{shift_id}: {shift}')

    def edit_shift(self):
        shift_id = int(input('Enter shift id: '))
        shift = self._shifts.get(shift_id)
        if shift is None:
            print('Shift not found!')
            return

        shift_date_ = self._get_shift_date('Enter new shift date or leave it empty: ') or shift.shift_at.date
        shift_hour_ = self._get_shift_hour('Enter new shift hour or leave it empty: ') or shift.shift_at.hour
        shift_minute_ = self._get_shift_minute('Enter new shift minute or leave it empty: ') or shift.shift_at.minute
        shift_at_ = datetime.strptime(f'{shift_date_} {shift_hour_}:{shift_minute_}', '%Y-%m-%d %H:%M')

        shift.shift_at = shift_at_
        print('Shift updated!')

    def delete_shift(self):
        shift_id = int(input('Enter shift id: '))
        self._shifts.pop(shift_id, None)
        print('Shift deleted!')


def main():
    zavod = ZavodHandler()
    while True:
        command = input('Enter command: ')
        match command:
            case '1':
                zavod.add_shift()
            case '2':
                zavod.get_shifts()
            case '3':
                zavod.edit_shift()
            case '4':
                zavod.delete_shift()
            case '5':
                pass
            case '6':
                return
            case _:
                print('Invalid command!')


if __name__ == '__main__':
    main()
