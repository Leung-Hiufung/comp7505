class BitList:
    def __init__(self) -> None:
        self._data = []

    def __str__(self) -> str:
        bits = ""
        for bit in self._data:
            bits += str(bit)
        return bits

    def __repr__(self) -> str:
        return self.__str__()

    def set_at(self, index: int) -> None:
        if index >= len(self._data):
            return
        self._data[index] = 1

    def unset_at(self, index: int) -> None:
        if index >= len(self._data):
            return
        self._data[index] = 0

    def get_at(self, index: int) -> int:
        if index >= len(self._data):
            return
        return self._data[index]

    def __setitem__(self, index: int, state: int) -> None:
        if state == 0:
            self.unset_at(index)
        else:
            self.set_at(index)

    def __getitem__(self, index: int) -> int:
        return self._data[index]

    def append(self, status: int) -> None:
        self._data.append(status)

    def prepend(self, status: int) -> None:
        self._data.insert(0, status)

    def reverse(self) -> None:
        new_data = []
        for i in range(len(self._data) - 1, -1, -1):
            new_data.append(self._data[i])
        self._data = new_data

    def flip_all_bits(self) -> None:
        for i, bit in enumerate(self._data):
            if bit == 0:
                self._data[i] = 1
            else:
                self._data[i] = 0

    def get_size(self) -> None:
        return len(self._data)

    def shift(self, dist: int) -> None:
        if len(self._data) == 0:
            return
        if dist > len(self._data):
            dist = len(self._data)
        elif dist < -len(self._data):
            dist = -len(self._data)

        if dist > 0:
            for i in range(len(self._data)):
                if i + dist < len(self._data):
                    self._data[i] = self._data[i + dist]
                else:
                    self._data[i] = 0
        if dist < 0:
            for i in range(len(self._data) - 1, -1, -1):
                if i + dist < 0:
                    self._data[i] = self._data[i + dist]
                else:
                    self._data[i] = 0

    def rotate(self, dist: int) -> None:
        if len(self._data) < 2:
            return
        if dist > 0:
            dist = dist % len(self._data)
        elif dist < 0:
            dist = dist % len(self._data) - len(self._data)
        while dist > 0:
            bit = self._data.pop(0)
            self._data.append(bit)
            dist -= 1
        while dist < 0:
            bit = self._data.pop(-1)
            self._data.insert(0, bit)
            dist += 1
