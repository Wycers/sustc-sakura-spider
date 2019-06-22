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
                    WEEK_START = JSON['week_start']
                    WEEK_END = JSON['week_end']
                    SEMESTER = JSON['semester']
                    SEMESTER_BASE = JSON['semester_base']
                except KeyError:
                    res['code'], res['msg'] = -2, 'missing params'
                else:
                    try:
                        week_start = int(WEEK_START)
                        week_end = int(WEEK_END)+1
                    except ValueError:
                        res['code'], res['msg'] = -3, 'value error'
                    else:
                        res['code'], res['msg'] = spider.trans(JSESSIONID, week_start, week_end, SEMESTER, SEMESTER_BASE)
        self.request.sendall(json.dumps(res).encode())


spider = Spider('./spider')
host = '127.0.0.1'
port = 9090
server = socketserver.ThreadingTCPServer((host, port), TCPhandler)
server.serve_forever()
