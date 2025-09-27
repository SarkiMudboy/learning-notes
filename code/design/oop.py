from abc import ABCMeta, abstractmethod
from typing import Any, Sequence, List
import time
import math


class Flower:
    def __init__(self, name: str, no_of_petals: int, price: float) -> None:
        self._name = name
        self._no_of_petals = no_of_petals
        self._price = price

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def set_no_of_petals(self, number: int) -> None:
        try:
            if not isinstance(number, int):
                raise TypeError("number must be an integer")
        except (TypeError, ValueError) as e:
            print("An error occured: ", e)
            return

        self._no_of_petals = number

    def set_price(self, price: str) -> None:
        self._price = price

    def get_no_of_petals(self) -> str:
        return self._no_of_petals

    def get_price(self) -> str:
        return self._price


#
# data = ["Rose", 4, 23.44]
#
# f = Flower(*data)
# f.set_no_of_petals("6")
# print(f.get_no_of_petals())


class CreditCard:
    def __init__(self, customer, bank, acnt, limit, bal=0.0) -> None:
        self._customer = customer
        self._bank = bank
        self._account = acnt
        self._limit = limit
        self._balance = bal

    def get_customer(self) -> str:
        return self._customer

    def get_bank(self) -> str:
        return self._bank

    def get_account(self) -> str:
        return self._account

    def get_limit(self) -> int:
        return self._limit

    def get_balance(self) -> float:
        return self._balance

    def _set_balance(self, amount: int) -> None:
        try:
            if not isinstance(amount, int):
                raise TypeError("number must be an integer")

            if amount < 0:
                raise ValueError("Invalid amount")

            self._balance += amount

        except TypeError as e:
            print("An error occured: ", e)
            return None

    def charge(self, amount: int) -> bool:

        try:
            if not isinstance(amount, int):
                raise TypeError("number must be an integer")

            if amount < 0:
                raise ValueError("Invalid amount")

        except TypeError as e:
            print("An error occured: ", e)
            return False

        except ValueError as e:
            print("An error occured: ", e)
            return False

        if amount + self._balance > self._limit:
            return False

        self._balance += amount

        return True

    def make_payment(self, amount):

        try:
            if not isinstance(amount, int):
                raise TypeError("number must be an integer")

            if amount < 0:
                raise ValueError("Invalid amount")

        except TypeError as e:
            print("An error occured: ", e)
            return

        except ValueError as e:
            print("An error occured: ", e)
            return

        if self._balance > 0.0:
            self._balance -= amount


class PredatoryCreditCard(CreditCard):

    OVERLIMIT_FEE = 5
    MONTHLY_CHARGE_COUNT_LIMIT = 10
    MIN_MONTHLY_PAYMENT = 0.40
    MIN_MONTHLY_PAYMENT_LATE_FEE = 5

    def __init__(self, customer, bank, acnt, limit, apr: float, bal=0.0):
        super().__init__(customer, bank, acnt, limit, bal)
        self._apr = apr
        self._monthly_charge_count = 0
        self._month_min_payment = (
            self.get_balance() * PredatoryCreditCard.MIN_MONTHLY_PAYMENT
        )

    def charge(self, amount: int) -> bool:

        success = super().charge(amount)
        if not success:
            self._set_balance(self._balance + PredatoryCreditCard.OVERLIMIT_FEE)

        self._monthly_charge_count += 1
        return success

    def make_payment(self, amount):
        try:
            super().make_payment(amount)
            if self._month_min_payment > 0:
                self._month_min_payment -= amount
        except Exception:
            raise

    def process_month(self):

        # APR: ssess monthly interest on outstanding balance, assess monthly interest on outstanding balance
        if self._balance > 0:
            monthly_factor = pow(1 + self._apr, 1 / 12)
            self._set_balance(monthly_factor)

        # additional $1 surcharge for each call more than 10 calls to charge in the month
        if (
            self._monthly_charge_count
            > PredatoryCreditCard.MONTHLY_CHARGE_COUNT_LIMIT
        ):

            self._set_balance(
                self._balance
                + 1
                * (
                    self._monthly_charge_count
                    - PredatoryCreditCard.MONTHLY_CHARGE_COUNT_LIMIT
                )
            )

        # A late fee is assessed if the customer does not subsequently pay that minimum amount before the next monthly cycle
        # check if the minimum payment has been made

        if self._month_min_payment > 0:
            self._set_balance(
                self._balance + PredatoryCreditCard.MIN_MONTHLY_PAYMENT_LATE_FEE
            )

        self._month_min_payment = (
            self._balance * PredatoryCreditCard.MIN_MONTHLY_PAYMENT
        )


# if __name__ == "__main__":
#
#     p = PredatoryCreditCard(
#         "AbdulSamad Sarki", "Stering Bank", "1234567890", 1000, 0.85, 200.0
#     )
#     # for _ in range(9):
#     #     p.charge(8)
#     print(p._month_min_payment)
#     p.make_payment(90)
#     p.process_month()
#     print(p.get_balance(), p._month_min_payment)
#
# if __name__ == "__main__":
#     wallet = []
#     wallet.append(
#         CreditCard(
#             "John Bowman", "California Finance", "5391 0375 9387 5309", 2500
#         )
#     )
#     wallet.append(
#         CreditCard(
#             "John Bowman", "California Finance", "3485 0399 3395 1954", 3500
#         )
#     )
#     wallet.append(
#         CreditCard(
#             "John Bowman", "California Finance", "5391 0375 9387 5309", 5000
#         )
#     )
#
#     for val in range(1, 59):
#
#         charged = wallet[0].charge(val)
#         if not charged:
#             print("1")
#         charged = wallet[1].charge(2 * val)
#         if not charged:
#             print("2")
#         charged = wallet[2].charge(3 * val)
#         if not charged:
#             print("3")
#
#     for c in range(3):
#         print("Customer =", wallet[c].get_customer())
#         print("Bank = ", wallet[c].get_bank())
#         print("Account =", wallet[c].get_account())
#         print("Limit = ", wallet[c].get_limit())
#         print("Balance =", wallet[c].get_balance())
#
# while wallet[c].get_balance() > 100:
#     wallet[c].make_payment(100)
#     print("New balance = ", wallet[c].get_balance())


class Vector:
    def __init__(self, d: int | Sequence) -> None:

        self._coords = []
        if isinstance(d, Sequence):

            for j in d:
                self._coords.append(j)

        elif isinstance(d, int):
            self._coords = [0] * d

    def __len__(self) -> int:
        return len(self._coords)

    def __getitem__(self, j) -> int:
        return self._coords[j]

    def __setitem__(self, j, val) -> None:
        self._coords[j] = val

    def __add__(self, other: Sequence):
        if len(other) != len(self._coords):
            raise ValueError("Dimensions must agree")

        result = Vector(len(self._coords))

        for point in range(len(result)):
            result[point] = self._coords[point] + other[point]

        return result

    def __eq__(self, other) -> bool:
        return self._coords == other._coords

    def __ne__(self, other) -> bool:
        return not self._coords == other._coords

    def __str__(self):
        return f"< {str(self._coords)} >" if self._coords else ""

    def __neg__(self) -> None:
        for j in range(len(self._coords)):
            self._coords[j] = -self._coords[j]

    def __radd__(self, other):
        return self.__add__(other)

    def _dot_mul(self, other: Sequence) -> int:

        if len(other) != len(self._coords):
            raise ValueError("Dimensions must match")

        total = 0

        for j in range(len(self._coords)):
            total += self._coords[j] * other[j]

        return total

    def _scalar_mul(self, k: int):

        result = Vector(len(self._coords))
        for j in range(len(self._coords)):
            result[j] = k * self._coords[j]

        return result

    def __mul__(self, other: Sequence | int):

        if isinstance(other, int):
            return self._scalar_mul(other)

        elif isinstance(other, Vector):
            return self._dot_mul(other)

        else:
            raise TypeError("Can only multiply by an int or Vector type")

    def __rmul__(self, other: Sequence):

        return self.__mul__(other)


# if __name__ == "__main__":
#     v = Vector([2, 4, 6, 8, 0])
#     v4 = Vector(5)
#
#     print(v * "weee")
# print(v2)
# print(v3)
# print(v4)
#


class Range:

    def __init__(self, start: int, stop: int = None, step: int = 1) -> None:

        if step == 0:
            raise ValueError("Step cannot be zero")

        if stop is None:
            start, stop = 0, start

        self._start = start
        self._step = step
        self._length = max(0, ((stop - start + step - 1) // step))

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, pos: int):

        if pos < 0:
            pos = pos + self._length

        if not 0 <= pos < self._length:
            raise IndexError("Index out of range")

        return self._start + (pos * self._step)

    def __contains__(self, k: int) -> bool:

        stop = self._start + (self._length - 1) * self._step

        if self._start <= k <= stop:
            if k % self._step == 0:
                return True
            else:
                return False
        else:
            return False


# if __name__ == "__main__":
#     e = Range(2, 10, 2)
#     print(len(e), e[-1])
#     start = time.time()
#     print(10000000000000 in Range(1000000000))
#     # print(99999999 in Range(1000000000))
#     stop = time.time()
#     print(stop - start)


def test_length_function():

    og = range(12, -2, -2)
    fk = Range(12, -2, -2)

    print(f"Len of range: {len(og)}, Len of Range: {len(fk)}")
    for i, n in enumerate(og):
        print(i, n)
        assert fk[i] == n


class Progression:

    def __init__(self, start: int | float = 0) -> None:

        self._current = start

    def _advance(self) -> None:

        self._current += 1

    def __next__(self) -> int:

        if self._current is None:
            raise StopIteration
        else:
            result = self._current
            self._advance()
            return result

    def __iter__(self):
        return self

    def print(self, n: int) -> str:
        return " ".join([str(next(self)) for _ in range(n)])


class ArithemetricProgression(Progression):

    def __init__(self, start: int = 0, diff: int = 0) -> None:
        super().__init__(start)
        self._diff = diff

        self._calls = 0

    def _advance(self) -> int:
        self._calls += 1
        self._current += self._diff
        return self._current

    def calls(self) -> int:
        return self._calls

    def current_term(self) -> int:
        return self._current


class FibonacciProgression(Progression):

    def __init__(self, first: int = 0, second: int = 1) -> None:

        super().__init__(first)
        # self._prev = second - first
        self._prev = second

    def _advance(self) -> int:
        self._current, self._prev = self._prev + self._current, self._current
        return self._current

    def __getitem__(self, index: int) -> int:
        terms = [next(self) for _ in range(index + 1)]
        return terms[index]


class Regression(Progression):

    def __init__(self, first: int = 2, second: int = 200) -> None:

        super().__init__(first)
        self._prev = second

    def _advance(self) -> int:
        self._prev, self._current = self._current, abs(
            self._prev - self._current
        )
        return self._current


class RootProgression(Progression):

    def __init__(self, start: float = 65536) -> None:
        super().__init__(start)

    def _advance(self) -> int:
        self._current = math.sqrt(self._current)
        return self._current


if __name__ == "__main__":

    r = RootProgression(144)
    print(r.print(3))


class DataSequence(metaclass=ABCMeta):

    @abstractmethod
    def __len__(self): ...

    @abstractmethod
    def __getitem__(self, val: Any) -> Any: ...

    def __contains__(self, val: Any) -> bool:

        for j in range(len(self)):
            if self[j] == val:
                return True
        return False

    def index(self, val: Any) -> int:

        for j in range(len(self)):
            if self[j] == val:
                return j

        raise ValueError("Value not in sequence")

    def count(self, val: Any) -> int:
        k = 0

        for j in range(len(self)):
            if self[j] == val:
                k += 1

        return k

    def __eq__(self, seq) -> bool:

        if len(self) != len(seq):
            return False

        for j in range(len(self)):
            if self[j] != seq[j]:
                return False

        return True

    def __lt__(self, seq) -> bool:

        if len(self) <= len(seq):
            return True
        elif len(self) >= len(seq):
            return False

        for j in range(len(self)):
            if self[j] < seq[j]:
                return True

        return False


# if __name__ == "__main__":
#
#     ap = ArithemetricProgression(0, 128)
#     last_term = pow(2, 63)
#
#     while ap.current_term() <= last_term:
#         next(ap)
#
#     print(ap.calls())


class ReverseSequenceIter:
    def __init__(self, seq: Sequence) -> None:

        self._seq = seq
        self._k = len(seq)

    def __next__(self) -> Any:

        self._k -= 1

        if self._k >= 0:
            return self._seq[self._k]
        else:
            raise StopIteration()

    def __iter__(self):
        return self


# if __name__ == "__main__":

# s = ReverseSequenceIter([2, 4, 6, 7, 8, 9])
# for i in s:
#     print(i)
