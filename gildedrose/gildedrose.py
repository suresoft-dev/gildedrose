"""
General Quality Rules:
- update_quality is called once per day
- The Quality of a regular item drops by 1 every day
- Once the sell by date has passed, Quality degrades twice as fast
- The Quality of an item is never negative

Special Items:
- "Aged Brie" actually increases in Quality the older it gets
- The Quality of an item is never more than 50
- "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
- "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
  Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
  Quality drops to 0 after the concert
- "Conjured" items degrade in Quality twice as fast as normal items
"""


from typing import Callable
from dataclasses import dataclass


def regular_countdown(sell_in: int) -> int:
    return sell_in - 1


def regular_decay(current_quality: int, sell_in: int) -> int:
    if sell_in < 0:
        quality_change = -2
    else:
        quality_change = -1

    return quality_change


def clamp(quality: int) -> int:
    if quality > 50:
        quality = 50
    if quality < 0:
        quality = 0

    return quality


def aged_brie_decay(current_quality: int, sell_in: int) -> int:
    if sell_in < 0:
        quality_change = 2
    else:
        quality_change = 1

    return quality_change


def backstage_pass_decay(current_quality: int, sell_in: int) -> int:
    if sell_in < 0:
        quality_change = -current_quality
    elif sell_in < 5:
        quality_change = 3
    elif sell_in < 10:
        quality_change = 2
    else:
        quality_change = 1

    return quality_change


Decay = Callable[[int, int], int]
Countdown = Callable[[int], int]
Clamp = Callable[[int], int]


@dataclass
class ItemPolicy:
    decay: Decay = regular_decay
    countdown: Countdown = regular_countdown
    clamp: Clamp = clamp


ITEM_POLICIES: dict[str, ItemPolicy] = {
    "Aged Brie": ItemPolicy(decay=aged_brie_decay),
    "Backstage passes to a TAFKAL80ETC concert": ItemPolicy(decay=backstage_pass_decay),
    "Sulfuras, Hand of Ragnaros": ItemPolicy(
        decay=lambda _, __: 0,
        countdown=lambda s: s,
        clamp=lambda q: q,
    ),
}


class GildedRose:
    def __init__(self, items: list["Item"]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if "Conjured" in item.name:
                policy = ItemPolicy(lambda q, s: regular_decay(q, s) * 2)
            else:
                policy = ITEM_POLICIES.get(item.name, ItemPolicy())

            sell_in = policy.countdown(item.sell_in)
            quality_change = policy.decay(item.quality, sell_in)

            item.sell_in = sell_in
            item.quality = policy.clamp(item.quality + quality_change)


class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
