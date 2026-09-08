\# Stock Market Analytics Dashboard



An interactive stock market analytics dashboard built with Power BI and Python to analyze historical NSE stock data and dynamically visualize stock performance.



\## Overview



This project combines Power BI with Python to create a dynamic stock market analytics system. Users can select a company from the Power BI dashboard, and the selected stock symbol is passed to a Python backend that fetches the latest historical data using yFinance.



The data is then cleaned and processed using Pandas before being loaded into Power BI for interactive analysis and visualization.



\## Key Features



\- Dynamic company selection using a Power BI slicer

\- Dynamic stock data fetching using Python and yFinance

\- Analysis of 5+ years of historical NSE stock data

\- Automated data cleaning and preprocessing using Pandas

\- Dynamic KPI cards for stock price and performance metrics

\- Closing price trend analysis

\- Trading volume analysis

\- Daily return calculation

\- 20-day Moving Average (MA20)

\- 50-day Moving Average (MA50)

\- Interactive company-level filtering

\- Year → Month → Day time-based drill-down

\- Custom Power BI visual for communicating the selected stock symbol to the local Python bridge



\## System Architecture



Power BI Slicer

&#x20;      ↓

Custom Power BI Visual

&#x20;      ↓

Python Bridge (bridge.py)

&#x20;      ↓

main.py

&#x20;      ↓

yFinance

&#x20;      ↓

Pandas Data Processing

&#x20;      ↓

CSV Data

&#x20;      ↓

Power BI Dashboard



\## Technologies Used



\- Python

\- Power BI

\- Pandas

\- yFinance

\- DAX

\- Power BI Custom Visuals

\- TypeScript

\- Git \& GitHub



\## Project Structure



```text

Stock-Market-Analytics-Dashboard/

│

├── main.py

├── bridge.py

├── get\_symbol.py

├── fetch\_data.ipynb

├── symbols.csv

├── stockBridgeVisual/

│   ├── src/

│   ├── assets/

│   ├── style/

│   ├── capabilities.json

│   ├── package.json

│   └── pbiviz.json

│

├── editss/

│   ├── Stock\_Market\_Dark\_Theme.json

│   ├── Stock\_Dashboard\_Dark\_Background.png

│   └── Stock\_Dashboard\_Color\_Palette.png

│

└── .gitignore

