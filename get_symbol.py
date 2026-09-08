def get_stock_symbol():
    with open("selected_symbol.txt", "r") as file:
        symbol = file.read().strip()

    if not symbol:
        print("No stock symbol selected")
        return None

    symbol = symbol.upper()

    yahoo_symbol = symbol + ".NS"

    print("NSE Symbol:", symbol)
    print("Yahoo Finance Symbol:", yahoo_symbol)

    return yahoo_symbol


if __name__ == "__main__":
    get_stock_symbol()