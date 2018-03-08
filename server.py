"""SocketServer to response spider request
"""

import socketserver
import json
from spider.spider import Spider


class TCPhandler(socketserver.BaseRequestHandler):
    """Override TCPhandler to handle request
    """

    def handle(self):
        """handle method
        """

        res = {
            'code': -1,
            'msg': 'error'
        }
        self.data = self.request.recv(1024).decode('UTF-8', 'ignore').strip()
        JSON = json.loads(self.data)
        try:
            action = JSON['action']
        except KeyError:
            res['code'], res['msg'] = -2, 'missing params'
        else:
            if action == 'login':
                try:
                    username = JSON['username']
                    password = JSON['password']
                except KeyError:
                    res['code'], res['msg'] = -2, 'missing params'
                else:
                    res['code'], res['msg'] = spider.login(username, password)

            if action == 'trans':
                try:
                    JSESSIONID = JSON['JSESSIONID']
                except KeyError:
                    res['code'], res['msg'] = -2, 'missing params'
                else:
                    res['code'], res['msg'] = spider.trans(JSESSIONID)
        self.request.sendall(json.dumps(res).encode())


spider = Spider('./spider')
host = '127.0.0.1'
port = 9090
server = socketserver.ThreadingTCPServer((host, port), TCPhandler)
server.serve_forever()
