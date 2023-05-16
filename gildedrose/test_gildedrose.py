from pathlib import Path
from gildedrose.gildedrose import GildedRose, Item


def run_gildedrose(days: int, items: list[Item]) -> str:
    log = ""
    for day in range(days):
        log += f"-------- day {day} --------\n"
        log += "name, sellIn, quality\n"
        for item in items:
            log += repr(item) + "\n"

        log += "\n"
        GildedRose(items).update_quality()

    return log


def test_gildedrose_regression_test() -> None:
    items = [
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),
    ]

    actual = run_gildedrose(days=2, items=items)

    expected = read_reference()
    assert expected == actual


def read_reference() -> str:
    reference = Path("gildedrose/reference.txt")
    return reference.read_text()