"""Serve the calculator page and perform arithmetic requests in Python."""

import json
import math
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000
MAX_REQUEST_BYTES = 16_384

STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}


def calculate(first_number: float, second_number: float, operation: str) -> float:
    """Return the result for one supported operation or raise ValueError."""
    operations = {
        "+": lambda: first_number + second_number,
        "-": lambda: first_number - second_number,
        "*": lambda: first_number * second_number,
        "/": lambda: first_number / second_number,
    }

    if operation not in operations:
        raise ValueError("Choose one of the four supported operations.")
    if operation == "/" and second_number == 0:
        raise ValueError("You cannot divide by zero.")

    result = operations[operation]()
    if not math.isfinite(result):
        raise ValueError("The result is outside the supported number range.")
    return result


class CalculatorHandler(BaseHTTPRequestHandler):
    """Serve the static interface and the JSON calculation endpoint."""

    def do_GET(self) -> None:
        file_info = STATIC_FILES.get(self.path)
        if file_info is None:
            self.send_error(404, "Page not found")
            return

        file_name, content_type = file_info
        contents = (PROJECT_DIR / file_name).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(contents)))
        self.end_headers()
        self.wfile.write(contents)

    def do_POST(self) -> None:
        if self.path != "/api/calculate":
            self.send_error(404, "Endpoint not found")
            return

        try:
            request_data = self._read_request_data()
            first_number = self._read_number(request_data, "first")
            second_number = self._read_number(request_data, "second")
            operation = request_data.get("operation")
            if not isinstance(operation, str):
                raise ValueError("Choose an operation.")

            # The browser sends the user's choices here; Python validates them,
            # calculates the answer, and returns it as JSON to the page.
            result = calculate(first_number, second_number, operation)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
            self._send_json({"error": str(error)}, status=400)
            return

        self._send_json({"result": result, "formatted_result": format(result, ".12g")})

    def _read_request_data(self) -> dict:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("The request size is invalid.") from error

        if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
            raise ValueError("The request must contain a small JSON body.")

        payload = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(payload)
        if not isinstance(request_data, dict):
            raise ValueError("The request must be a JSON object.")
        return request_data

    @staticmethod
    def _read_number(request_data: dict, field_name: str) -> float:
        value = request_data.get(field_name)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Enter two valid numbers.")
        if not math.isfinite(value):
            raise ValueError("Numbers must be finite values.")
        return value

    def _send_json(self, data: dict, status: int = 200) -> None:
        contents = json.dumps(data, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(contents)))
        self.end_headers()
        self.wfile.write(contents)

    def log_message(self, format_string: str, *args: object) -> None:
        """Keep the terminal log short and useful while the app is running."""
        print(f"{self.address_string()} - {format_string % args}")


def main() -> None:
    is_standalone = getattr(sys, "frozen", False)
    server_port = 0 if is_standalone else PORT
    server = ThreadingHTTPServer((HOST, server_port), CalculatorHandler)
    address = f"http://{HOST}:{server.server_port}"
    print(f"Calculator is running at {address}")
    print("Press Ctrl+C to stop the server.")
    if is_standalone:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping the calculator server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()