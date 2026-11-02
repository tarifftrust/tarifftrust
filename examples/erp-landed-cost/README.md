# Landed cost per unit in an ERP

Reads a purchase order from a CSV file, estimates it as one US import declaration, and prints the
landed cost per unit of each SKU. The entry fees (MPF, HMF) count once for the order, as they do on
a real entry: adding up single-product estimates would overstate them.

```bash
pip install tarifftrust
TARIFFTRUST_API_KEY=tarifftrust_... python landed_cost.py purchase_order.csv
```

Replace `read_order` with a query to your ERP, and `FREIGHT` and `INSURANCE` with your shipment's.
Fees, freight and insurance are spread by customs value here: use your own allocation rule if your
accounting has one. A line whose duty is unknown stays unknown: never count it as zero.
