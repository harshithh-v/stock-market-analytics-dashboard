from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import subprocess
import sys


class StockBridge(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/symbol":
            query = parse_qs(parsed_url.query)
            symbol = query.get("symbol", [None])[0]

            if not symbol:
                self.send_response(400)
                self.end_headers()

                try:
                    self.wfile.write(b"No stock symbol provided")
                except ConnectionAbortedError:
                    pass

                return

            symbol = symbol.upper()

            print("\n" + "=" * 60)
            print("NEW STOCK REQUEST")
            print("=" * 60)
            print("Received Symbol:", symbol)

            with open("selected_symbol.txt", "w") as file:
                file.write(symbol)

            print("Saved to selected_symbol.txt")

            print("\n" + "-" * 60)
            print("RUNNING MAIN.PY")
            print("-" * 60)

            result = subprocess.run(
                [sys.executable, "main.py"],
                capture_output=True,
                text=True
            )

            print("\nOutput from main.py:")
            print(result.stdout)

            if result.stderr:
                print("\nError from main.py:")
                print(result.stderr)

            print("-" * 60)

            if result.returncode != 0:
                response = (
                    "main.py failed\n\n"
                    + result.stdout
                    + "\n"
                    + result.stderr
                )
                self.send_response(500)
            else:
                response = result.stdout
                self.send_response(200)

            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            try:
                self.wfile.write(response.encode())
            except ConnectionAbortedError:
                pass

            print("Request completed for:", symbol)
            print("=" * 60)

        else:
            self.send_response(404)
            self.end_headers()

            try:
                self.wfile.write(b"Invalid endpoint")
            except ConnectionAbortedError:
                pass


server = HTTPServer(("localhost", 8000), StockBridge)

print("Stock Bridge running...")

server.serve_forever()
