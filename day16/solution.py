from typing import List
from collections import deque
from abc import ABC, abstractmethod
from math import prod


def preprocess_data(data: str) -> str:
    bit_string = "{0:b}".format(int(data.strip(), base=16))
    # Ensure len(bit_string) is a multiple of 8.
    prefix_bits = "0" * ((8 - (len(bit_string) % 8)) % 8)
    return prefix_bits + bit_string


class Stream:
    def __init__(self, data: str) -> None:
        self.q = deque(data)
        self.bits_popped = 0

    def pop(self, n: int) -> int:
        return int(self.pop_str(n), base=2)

    def pop_str(self, n: int) -> str:
        self.bits_popped += n
        return "".join([self.q.popleft() for _ in range(n)])

    def flush_remaining_bits(self) -> None:
        bits_to_pop = (8 - (self.bits_popped % 8)) % 8
        self.pop_str(bits_to_pop)
        self.bits_popped = 0

    @property
    def length(self) -> int:
        return len(self.q)


class Packet(ABC):
    _version: int

    def _repr_info(self) -> str:
        return ""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(version={self.version}{self._repr_info()})"

    @property
    def version(self) -> int:
        return self._version

    @property
    @abstractmethod
    def version_sum(self) -> int:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass


class LiteralValue(Packet):
    def __init__(self, version: int, value: int) -> None:
        self._version = version
        self._value = value

    @property
    def version_sum(self) -> int:
        return self.version

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def from_data_stream(cls, version: int, stream: Stream) -> "LiteralValue":
        packet_finished = False
        packet = ""
        while not packet_finished:
            chunk = stream.pop_str(5)
            if chunk[0] == "0":
                packet_finished = True
            packet += chunk[1:]
        value = int(packet, base=2)
        return cls(version=version, value=value)

    def _repr_info(self) -> str:
        return f", value={self.value}"


class PacketContainer(Packet):
    def __init__(self, version: int, type_id: int, sub_packets: List[Packet]) -> None:
        self._version = version
        self.type_id = type_id
        self.sub_packets = sub_packets

    @property
    def version_sum(self) -> int:
        return sum([self.version] + [p.version_sum for p in self.sub_packets])

    def _repr_info(self) -> str:
        return f", sub_packets={self.sub_packets}"

    @property
    def value(self) -> int:
        method_map = {
            0: self._sum,
            1: self._product,
            2: self._min,
            3: self._max,
            5: self._gt,
            6: self._lt,
            7: self._eq,
        }
        return method_map[self.type_id]()

    def _sum(self) -> int:
        return sum([p.value for p in self.sub_packets])

    def _product(self) -> int:

        return prod([p.value for p in self.sub_packets])

    def _min(self) -> int:
        return min([p.value for p in self.sub_packets])

    def _max(self) -> int:
        return max([p.value for p in self.sub_packets])

    def _gt(self) -> int:
        if self.sub_packets[0].value > self.sub_packets[1].value:
            return 1
        else:
            return 0

    def _lt(self) -> int:
        if self.sub_packets[0].value < self.sub_packets[1].value:
            return 1
        else:
            return 0

    def _eq(self) -> int:
        if self.sub_packets[0].value == self.sub_packets[1].value:
            return 1
        else:
            return 0


class PacketContainer0(PacketContainer):
    @classmethod
    def from_data_stream(
        cls, version: int, type_id: int, stream: Stream
    ) -> "PacketContainer0":
        sub_packets = []
        sub_packets_length = stream.pop(15)
        new_stream = Stream(stream.pop_str(sub_packets_length))
        while new_stream.length > 0:
            packet = get_packet(new_stream)
            sub_packets.append(packet)
        return cls(version, type_id, sub_packets)


class PacketContainer1(PacketContainer):
    @classmethod
    def from_data_stream(
        cls, version: int, type_id: int, stream: Stream
    ) -> "PacketContainer1":
        sub_packets = []
        no_of_sub_packets = stream.pop(11)
        for _ in range(no_of_sub_packets):
            packet = get_packet(stream)
            sub_packets.append(packet)
        return cls(version, type_id, sub_packets)


def get_packet(stream: Stream) -> Packet:
    version = stream.pop(3)
    type_id = stream.pop(3)

    if type_id == 4:
        return LiteralValue.from_data_stream(version, stream)
    else:
        length_type_id = stream.pop(1)
        if length_type_id == 0:
            return PacketContainer0.from_data_stream(version, type_id, stream)
        if length_type_id == 1:
            return PacketContainer1.from_data_stream(version, type_id, stream)
        raise Exception(f"Incorrect length_type_id given: {length_type_id}")


def q1(data: str) -> int:
    stream = Stream(data)
    return get_packet(stream).version_sum


def q2(data: str) -> int:
    stream = Stream(data)
    return get_packet(stream).value
