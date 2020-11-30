"""Home work 5."""

from tornado import httpclient
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler


class MainHandler(RequestHandler):
    """Application request handler."""

    async def get(self):
        """Override request processing."""
        headers_to_clear = ['Server', 'Date',  'Content-Type']
        request_suffix = self.request.path.split('/')[-1]
        response = await self.get_response(request_suffix)
        for header in headers_to_clear:
            self.clear_header(header)
        self.set_status(response.code)
        self.write(response.body)
        self.add_headers(response)

    def add_headers(self, response):
        """
        Add response headers.

        Args:
            response: server response.
        """
        for header, body in response.headers.get_all():
            if header == 'Transfer-Encoding':
                continue
            self.add_header(header, body)

    @staticmethod
    async def get_response(request_suffix):
        """
        Get target server response.

        Args:
            request_suffix: user input number.

        Returns:
            response: target server response
        """
        url = 'https://jsonplaceholder.typicode.com/todos/'
        client = httpclient.AsyncHTTPClient()
        response = await client.fetch(url + request_suffix)
        client.close()
        return response


def get_app():
    """
    Create app with correct routes.

    Returns:
        app: created application.
    """
    return Application([
        (r'/todo/[0-9]+', MainHandler),
    ])


if __name__ == '__main__':
    app = get_app()
    PORT = 8080
    app.listen(PORT)
    IOLoop.current().start()
