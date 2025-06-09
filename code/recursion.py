import math
import os

from typing import Any, Generator, Iterable, List, Literal, Sequence, Tuple

hex = {"10": "A", "11": "B", "12": "C", "13": "D", "14": "E", "15": "F"}


# implement the binary to hex function
def four_bit_binary_to_decimal(binary: str) -> int:

    total: int = 0
    index: int = 0

    for i in range(3, -1, -1):
        total += int(binary[index]) * math.pow(2, i)
        index += 1
    return int(total)


def binary_to_hex(binary_num: str, to_decimal=False) -> str:

    n = len(binary_num) // 4
    total = "0x"
    total_decimal = 0
    chunk_index_1, chunk_index_2 = 0, 4

    for j in range(1, n + 1):
        b = binary_num[chunk_index_1:chunk_index_2]
        db = four_bit_binary_to_decimal(b)

        if to_decimal:
            exp = 4 * (j - 1)
            total_decimal += db * math.pow(2, exp)

        total = total + str(db) if db < 9 else total + hex.get(str(db))

        chunk_index_1 += 4
        chunk_index_2 += 4

    return total


myb = "110000101011"
# print(binary_to_hex(myb))


def DiskUsage(path: str) -> int:
    """Disk Usage for a directory/file in python"""

    total = os.path.getsize(path)
    if os.path.isdir(path):
        for obj in os.listdir(path):
            child = os.path.join(path, obj)
            total += DiskUsage(child)

    print(f"total du for {path}:", "{0:<7}".format(total))
    return total


# if __name__ == "__main__":
#     path = sys.argv[1]
#     if not path:
#         raise ValueError("Please Enter a filepath")
#     du = DiskUsage(path)
#     print(f"ToTal->{du/1000}kb")


def find(path: str, filename: str) -> List[str]:
    """Reports all entries of the file system rooted at the given path having the
    given file name"""

    entries = []

    if not os.path.isdir(path):
        return []
    else:
        for obj in os.listdir(path):
            child = os.path.join(path, obj)
            if obj == filename and not os.path.isdir(child):
                entries.append(child)
            entries += find(child, filename)

    return entries


# print(find(r"C:\Users\ihima\Documents\golang-practice", "play.go"))


def find_log(n: int):
    """Find the log to base 2 of a given number n"""

    if n <= 1.0:
        return 0
    else:
        return 1 + find_log(n // 2)


def my_find_log(n: int, t: int) -> int:

    if n <= 1.0:
        return t

    n = n // 2

    return find_log(n, t + 1)


# print(find_log(16))


def unique(S: Sequence, j: int):
    if j == S[0]:
        return True
    elif len(S) == 1:
        return False
    else:
        return unique(S[1:], j)


def parent_unique(S: Sequence, j: int):

    if j == len(S) - 1:
        return False

    if unique(S[j + 1 :], S[j]):
        return True
    else:
        return parent_unique(S, j + 1)


# seq = [2, 3, 5, 1, 6, 7, 8, 9, 13, 21]
# print(parent_unique(seq, 0))


Position = Literal["a"] | Literal["b"] | Literal["c"]


class Tower:

    def __init__(self, num: int) -> None:

        if num <= 0:
            raise ValueError("Invalid disc size")

        self._pegs = {
            "a": [],
            "b": [],
            "c": [],
        }
        self._peg["a"].append(*[size for size in range(num)])
        self._temp = "c"  # temporary storage, its set as a fixed value
        self._current_stack = "a"  # peg that currently holds unsolved discs

    def move_disc(self, from_peg: Position, to_peg=Position) -> None:
        """Move a single disc from a peg to another peg"""

        disc = self._pegs[from_peg][0]
        if disc < self._pegs[to_peg][0]:
            disc = self._pegs[from_peg].pop(0)
            self._pegs[to_peg].insert(0, disc)
        else:
            raise ValueError("Cannot stack in descending order")

    def move_top_stack(self, to_peg: Position) -> None:

        for _ in self._pegs[self._current_stack][:-1]:
            self.move_disc(self._current_stack, to_peg)

    def _empty_stack(self) -> Position:
        return "a" if len(self._pegs["a"]) == 0 else "b"

    def solve(self):
        if len(self._current_stack) == 1:
            self.move_disc(self._current_stack, self._temp)
        else:
            empty_peg = self._empty_stack()
            self.move_top_stack(empty_peg)
            self.move_disc(self._current_stack, self._temp)
            self._current_stack = empty_peg
            self.solve()
        return


def find_subsets(s: Sequence, subsets: List[Any]) -> List[Any]:

    n = len(s)

    if n == 1:
        subsets.append(s)
        return subsets

    for t in range(1, n):
        subsets.append([s[0], s[t]])
        # print(subsets)

    return find_subsets(s[1:], subsets)


def generate_subsets(S, subset=[], index=0):
    # Base case: if we've considered all elements
    if index == len(S):
        print(subset)
        return

    # Recursive case:
    # 1. Exclude the current element
    generate_subsets(S, subset, index + 1)

    # 2. Include the current element
    generate_subsets(S, subset + [S[index]], index + 1)


test = ["a", "b", "c", "d"]
# p = generate_subsets(test, [])
# print(p)


def num_to_bin(num: int, result: int) -> str:

    if num == 1:
        result += "1"
        return reverse_string(result, 0, len(result) - 1)

    result += str(num % 2)
    num = num // 2
    return num_to_bin(num, result)


def reverse_string(word: str, first: int, last: int) -> str:

    if last - first <= 0:
        return word

    else:

        fw = word[first]
        word = word[:first] + word[last] + word[first + 1 :]
        word = word[:last] + fw + word[last + 1 :]

    return reverse_string(word, first + 1, last - 1)


def eff_reverse(s: str):
    if len(s) <= 1:
        return s

    return eff_reverse(s[1:]) + s[0]


# test_string = "pots&pans"
# lone = "racecar"
# print(eff_reverse(test_string))


def is_palindrome(s: str) -> bool:

    if len(s) <= 1:
        return True

    return (s[0] == s[-1]) and is_palindrome(s[1:-1])


# test_string = "racecar"
# false_string = "werser"
# lone = "gohangasalamiimalasagnahog"
# print(is_palindrome(lone))


def more_vowels(s: str, count: int, index: int) -> bool:

    if len(s) == index:
        return False

    if s[index] in "aeiou":
        count += 1

        if count > (len(s) / 2):
            return True

    return more_vowels(s, count, index + 1)


# word = "salamia"
# print(more_vowels(word, 0, 0))


def even_first(s: List[int], index: int = 0) -> List[int]:
    # base case
    if len(s) == index:
        return s

    if s[index] % 2 == 0:
        num = s.pop(index)
        s.insert(0, num)

    return even_first(s, index + 1)


# chatgpt solution
def rearrange_even_before_odd(seq):
    if not seq:
        return []
    head, *tail = seq
    if head % 2 == 0:
        return [head] + rearrange_even_before_odd(tail)
    else:
        return rearrange_even_before_odd(tail) + [head]


def rearrange_for_k(seq, k):
    if not seq:
        return []
    head, *tail = seq
    if head <= k:
        return [head] + rearrange_for_k(tail, k)
    else:
        return rearrange_for_k(tail, k) + [head]


def sort_around_k(S: List[int], k) -> List[int]:

    if len(S) <= 1:
        return S

    pivot = S[0]
    rest = S[1:]

    partitioned_rest = sort_around_k(rest, k)

    if pivot <= k:
        return (
            [pivot]
            + [j for j in partitioned_rest if j <= k]
            + [j for j in partitioned_rest if j > k]
        )
    else:
        return (
            [j for j in partitioned_rest if j <= k]
            + [j for j in partitioned_rest if j > k]
            + [pivot]
        )


def partition_in_place_sort(
    S: List[int], k: int, left: int, right: int
) -> List[int]:
    print("call")
    if left >= right:
        return S

    if S[left] <= k:
        return partition_in_place_sort(S, k, left + 1, right)
    else:
        if S[right] <= k:
            S[left], S[right] = S[right], S[left]
            return partition_in_place_sort(S, k, left + 1, right - 1)
        else:
            return partition_in_place_sort(S, k, left, right - 1)


# num_array = [3, 4, 1, 66, 8, 11, 2, 3]
# test_Array = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
# print(rearrange_for_k(num_array, 10))
# print(sort_around_k(test_Array, 9))
# print(partition_in_place_sort(test_Array, 9, 0, len(test_Array) - 1))


def find_pair_sum(S: List[int], k: int, left: int, right: int):
    print("call")
    if left > right:
        return None

    if S[right] > k:
        return find_pair_sum(S, k, left, right - 1)

    potential_right = k - S[left]

    if potential_right == S[right]:
        return [S[left], S[right]]

    elif potential_right < S[right]:
        return find_pair_sum(S, k, left, right - 1)

    return find_pair_sum(S, k, left + 1, right - 1)


def find_max_pair(S: Sequence):
    def helper(
        S: Iterable,
        k: int,
        left: int,
        right: int,
        max_left: int,
        max_right: int,
    ) -> Tuple[int]:

        if left == max_right or right == max_left:
            return (S[max_left], S[max_right], k)

        max_left = left if S[left] > S[max_left] else max_left
        max_right = right if S[right] > S[max_right] else max_right

        k = S[max_left] + S[max_right]

        return helper(S, k, left + 1, right - 1, max_left, max_right)

    return helper(S, 0, 0, len(S) - 1, 0, len(S) - 1)


if __name__ == "__main__":
    # sq = [1, 2, 8, 0, 4, 3, 9, 5]
    sq = [4, 6, 2, 8, 11, 3, 0]
    m = find_max_pair(sq)
    print(m)


# gen by chatgpt
def find_pair_sum_k_gpt(S, k):
    def helper(left, right):
        print("call")
        if left >= right:
            return None  # No pair found

        current_sum = S[left] + S[right]

        if current_sum == k:
            return (S[left], S[right])
        elif current_sum < k:
            return helper(left + 1, right)
        else:
            return helper(left, right - 1)

    return helper(0, len(S) - 1)


arr = [1, 4, 8, 9, 11, 15, 20]
# diffArr = [3, 5, 7, 9, 12, 14, 15, 16, 20, 27, 30, 31, 50]


def binary_search(S: List[int], k: int, high: int, low: int) -> int:

    if low - high <= 0:
        return False

    mid = (low - high) // 2

    if S[mid] == k:
        return True

    elif S[mid] > k:
        return binary_search(S, k, low, mid - 1)
    else:
        return binary_search(S, k, mid + 1, high)


def iter_power(base: int, x: int) -> int:

    if x == 0:
        return 1

    partial = 1
    exp = x // 2

    for _ in range(exp):
        partial *= base

    result = partial * partial

    if x % 2 == 0:
        return result
    else:
        return base * result


def test_puzzle(seq: List[int], excluded: int, puzzle: List[str] = []):

    sums = ["pot + pan = bib", "dog + cat = pig", "boy + girl = baby"]


def PuzzleSolve(
    S: list[int], k: int, U: List[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
):
    """
    Solves a summation puzzle by computing an enumeration of all k-length extensions to S using elements in U without repetitions

    args: S - Sequence of k-1 length elements
          U - We use U to keep track of elements not in S
          K - length of elements in the puzzle
          returns None
    """

    current_excluded = None
    for e, i in enumerate(U):

        S.append(e)
        U.pop(i)
        current_excluded = i

        if k == 1:
            # we test here
            ...

        else:
            PuzzleSolve(S, k - 1, U)

        excluded = S.pop(-1)
        U.insert(current_excluded, excluded)


def count_ones(bits: str, ones: str) -> int:
    if len(bits) == 0 or bits[-1] == "0":
        return len(ones)

    return count_ones(bits[:-1], ones + "1")


def r_draw_iterval(center_length):
    if center_length > 0:
        draw_interval(center_length - 1)
        draw_line(center_length)
        draw_interval(center_length - 1)


def draw_line(tick_length: int, tick_label: str = "") -> None:

    line = "-" * tick_length
    if tick_label:
        line += " " + tick_label
    print(line)


def draw_interval(center_length) -> None:

    num_of_lines = int(math.pow(2, center_length) - 1)
    for counter in range(num_of_lines):
        counter_bin = bin(counter)[2:]
        counter_ones = count_ones(counter_bin, "")
        draw_line(counter_ones + 1)


def draw_ruler(num_of_inches: int, major_length: int) -> None:

    draw_line(major_length, "0")
    for j in range(1, num_of_inches):
        draw_interval(major_length - 1)
        draw_line(major_length, str(j))


def dir_walk(path: str) -> Generator[tuple[str, list, list], Any, None]:
    """your own implementation of such a os.walk(path) function"""

    path = os.path.abspath(path)
    dirs = []
    files = []

    for obj in os.listdir(path):
        child = os.path.join(path, obj)
        if os.path.isdir(child):
            dirs.append(obj)
        else:
            files.append(os.path.basename(obj))

    if len(dirs) > 0:
        for child in dirs:
            c = os.path.join(path, child)
            for r in dir_walk(c):
                yield r
    yield (path, dirs, files)


# if __name__ == "__main__":

# for path in os.walk(r"C:\Users\ihima\Documents\golang-practice"):
#     print(path)

# for path in dir_walk(r"C:\Users\ihima\Documents\golang-practice"):
#     print(path)
