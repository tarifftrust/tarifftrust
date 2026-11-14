"""Landed cost per unit of a purchase order, for an ERP or an inventory system.

The lines of one order go in as one declaration, so the entry fees (MPF, HMF) count once, then
duty, fees, freight and insurance are spread over the units.

    pip install tarifftrust
    TARIFFTRUST_API_KEY=tarifftrust_... python landed_cost.py purchase_order.csv
"""

import csv
import sys
from decimal import ROUND_HALF_UP, Decimal

from tarifftrust import TariffTrust

FREIGHT = Decimal("1200")
INSURANCE = Decimal("150")
CENT = Decimal("0.01")


def read_order(path):
    with open(path, newline="") as file:
        return list(csv.DictReader(file))


def estimate(client, order, reference):
    return client.estimate_entry(
        reference=reference,
        transport_mode="ocean",
        freight=FREIGHT,
        insurance=INSURANCE,
        lines=[
            {
                "reference": line["sku"],
                "hts": line["hts"],
                "origin": line["origin"],
                "customs_value": line["customs_value"],
            }
            for line in order
        ],
    )


def unit_costs(order, entry):
    """Each line: its goods and its duty, its share by value of what the whole order pays once,
    and the cost of a unit. What is unknown stays unknown, never 0: without its duty or the order's
    fees, a line has no landed cost."""
    total_value = sum(Decimal(line["customs_value"]) for line in order)
    fees = None if entry.estimated_fees is None else Decimal(entry.estimated_fees)
    rows = []
    for line, result in zip(order, entry.lines, strict=True):
        value = Decimal(line["customs_value"])
        duty = None if result.estimated_duty is None else Decimal(result.estimated_duty)
        if duty is None or fees is None:
            rows.append((line["sku"], result.status, duty, None))
            continue
        cost = value + duty + (fees + FREIGHT + INSURANCE) * value / total_value
        unit = (cost / int(line["quantity"])).quantize(CENT, ROUND_HALF_UP)
        rows.append((line["sku"], result.status, duty, unit))
    return rows


def main(path):
    with TariffTrust() as client:
        entry = estimate(client, read_order(path), reference=path)
    print(f"Status: {entry.status}, from {entry.data.edition}, as of {entry.as_of}")
    print(f"Duty: {entry.estimated_duty}  Fees: {entry.estimated_fees}")
    print(f"Landed cost: {entry.estimated_landed_cost}")
    for sku, status, duty, unit in unit_costs(read_order(path), entry):
        # A duty of 0.00 is known: only None is unknown.
        shown = ["unknown" if amount is None else amount for amount in (duty, unit)]
        print(f"  {sku} ({status}): duty {shown[0]}, per unit {shown[1]}")
    for line in entry.lines:
        for item in line.missing or []:
            print(f"To send for {line.reference}: {item.question} ({item.field})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "purchase_order.csv"))
