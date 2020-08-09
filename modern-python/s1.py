from typing import Set, List
import random

"""
My First Script: Calculate an important value.
"""
print(355/113)



class Dice:
    RNG = random.Random()
    def __init__(self, n: int, sides: int = 6) -> None:
        self.n_dice = n
        self.sides = sides
        self.faces: List[int]
        self.roll_number = 0
    def __str__(self) -> str:
        return ", ".join(
            f"{i}: {f}"
            for i, f in enumerate(self.faces)
        )
    def total(self) -> int:
        return sum(self.faces)
    def average(self) -> float:
        return sum(self.faces) / self.n_dice
    def first_roll(self) -> List[int]:
        self.roll_number = 0
        self.faces = [
            self.RNG.randint(1, self.sides)
            for _ in range(self.n_dice)
        ]
        return self.faces
    def reroll(self, positions: Set[int]) -> List[int]:
        self.roll_number += 1
        for p in positions:
            self.faces[p] = self.RNG.randint(1, self.sides)
        return self.faces

d1 = Dice(2)
d1.first_roll()
print(d1)

from typing import NamedTuple

class Card(NamedTuple):
    rank: int
    suit: str

eh = Card(rank=8, suit="test")
print(eh, eh.rank, eh.suit)

# can not set
# eh.rank = 5

from dataclasses import dataclass

@dataclass
class CribbageHand:
    cards: List[Card]
    def to_crib(self, card1: Card):
        self.cards.remove(card1)

cards = [
    Card(rank=1, suit='test1'),
    Card(rank=2, suit='test2'),
    Card(rank=3, suit='test3'),
    Card(rank=1, suit='test1'),
]

ch = CribbageHand(cards)
print(ch)

ch.to_crib(cards[0])
print(ch)

@dataclass(frozen=True, order=True)
class Card2:
    rank: int
    suit: str

eh = Card2(rank=8, suit="test")
#eh.rank = 9

#eh.somt_attribue = 5

from pathlib import Path

p = Path('../')
print([x for x in p.iterdir() if x.is_dir()])