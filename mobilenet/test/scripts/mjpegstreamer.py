import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import cv2
from PIL import Image
import StringIO


class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('/stream.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    r, buf = cv2.imencode(".jpg", MJPEGServer.get_image())
                    self.wfile.write("--jpgboundary\r\n".encode())
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                except KeyboardInterrupt:
                    break
            return

        if self.path.endswith('.html') or self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write(
                '<img src="http://localhost:5000/stream.mjpg" height="{}px" width="{}px"/>'.format(MJPEGServer.height,
                                                                                                   MJPEGServer.width))
            self.wfile.write('</body></html>')
            return


class StreamingServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class MJPEGServer(threading.Thread):
    img = None
    width = 0
    height = 0

    def __init__(self, width, height):
        super(MJPEGServer, self).__init__()
        self.daemon = True
        MJPEGServer.width = width
        MJPEGServer.height = height

    def run(self):
        self._server = HTTPServer(('', 5000), StreamingHandler)
        self._server.serve_forever()

    @staticmethod
    def set_image(img):
        MJPEGServer.img = img

    @staticmethod
    def get_image():
        return MJPEGServer.img
