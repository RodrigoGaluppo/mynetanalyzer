import tornado.ioloop
import tornado.web
import tornado.websocket
import ssl

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")

    def on_message(self, message):
        print("Received message from client:", message)

    def on_close(self):
        print("WebSocket connection closed")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    ssl_ctx.set_ciphers("DEFAULT@SECLEVEL=1")  # Adjust cipher suite

    app.listen(8080)
    
    tornado.ioloop.IOLoop.current().start()
