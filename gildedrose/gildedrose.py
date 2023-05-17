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


def regular_decay(current_quality: int, sell_in: int) -> int:
    if sell_in < 0:
        quality_change = -2
    else:
        quality_change = -1

    return quality_change


def aged_brie_decay(current_quality: int, sell_in: int) -> int:
    if sell_in < 0:
        quality_change = 2
    else:
        quality_change = 1

    return quality_change


def backstage_passes_decay(current_quality: int, sell_in: int) -> int:
    if sell_in < 0:
        quality_change = -current_quality
    elif sell_in < 5:
        quality_change = 3
    elif sell_in < 10:
        quality_change = 2
    else:
        quality_change = 1

    return quality_change


def legendary_decay(current_quality: int, sell_in: int) -> int:
    return 0


ITEM_DECAYS = {
    "Aged Brie": aged_brie_decay,
    "Backstage passes to a TAFKAL80ETC concert": backstage_passes_decay,
    "Sulfuras, Hand of Ragnaros": legendary_decay,
}


class GildedRose:
    def __init__(self, items: list["Item"]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            # reduce sell in
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1

            decay = ITEM_DECAYS.get(item.name, regular_decay)
            item.quality += decay(item.quality, item.sell_in)

            if item.name != "Sulfuras, Hand of Ragnaros":
                if item.quality > 50:
                    item.quality = 50
                if item.quality < 0:
                    item.quality = 0


class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
