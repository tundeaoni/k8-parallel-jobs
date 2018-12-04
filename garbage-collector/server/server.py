from kube import Kube
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi, traceback ,json , logging

logging.basicConfig(level=logging.INFO)
#  curl -X POST $GARBAGE_COLLECTOR_URL -H 'content-type: application/json' -d "{  \"label\": \"group_id=$GROUP_ID\" }"
class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = cgi.FieldStorage(fp=self.rfile,
                           headers=self.headers, environ={
                                'REQUEST_METHOD':'POST',
                                'CONTENT_TYPE':self.headers['Content-Type']
                           })
        try:
            data = json.loads(data.value)
            print data
            label = data["label"]
            kubeClient = Kube()
            kubeClient.deleteResources(label)
            response_code = 200
            response = "{}"
        except Exception:
            traceback.print_exc()
            response_code = 500
            response = '{"error": "operation unsuccessful"}'

        self.send_response(response_code)
        self.end_headers()
        self.wfile.write(response)

port = 8080
httpd = HTTPServer(('0.0.0.0', port), RestHTTPRequestHandler)
print "running server on port {}".format(port)
while True:
    httpd.handle_request()