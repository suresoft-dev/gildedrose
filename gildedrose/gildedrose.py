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

class GildedRose:

    def __init__(self, items: list["Item"]):
        self.items = items

    def update_quality(self):
        for item in self.items:

            if item.name == "Aged Brie":
                if item.quality < 50:
                    item.quality = item.quality + 1
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.sell_in < 11:
                        if item.quality < 50:
                            item.quality = item.quality + 1
                    if item.sell_in < 6:
                        if item.quality < 50:
                            item.quality = item.quality + 1
            elif item.name == "Sulfuras, Hand of Ragnaros":
                item.quality = item.quality
            else:
                if item.quality > 0:
                    item.quality = item.quality - 1

            # reduce sell in
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            
            if item.sell_in < 0:
                if item.name == "Aged Brie":
                    if item.quality < 50:
                        item.quality = item.quality + 1
                elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                    item.quality = item.quality - item.quality
                elif item.name == "Sulfuras, Hand of Ragnaros":
                    item.quality == item.quality
                else:
                    if item.quality > 0:
                        item.quality = item.quality - 1


class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)