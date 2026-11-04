# US import duty in Google Sheets

A custom function for your spreadsheets: `=TARIFFTRUST_DUTY("6109.10.00.12", "CN", 10000)`.

1. In the spreadsheet, open **Extensions > Apps Script** and paste [Code.gs](Code.gs).
2. Under **Project Settings > Script properties**, add `TARIFFTRUST_API_KEY` with your API key.
3. Use the function in a cell, with cell references if you like: `=TARIFFTRUST_DUTY(A2, B2, C2)`.

Each new set of arguments that gives a figure counts as one estimate in your plan's quota. The same cell recalculated on
the same day counts once. Anyone who can edit the script can read the key: use a key with only the
`calculate` permission, and keep the spreadsheet among people you trust.
