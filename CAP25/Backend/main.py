import os
import tornado.ioloop
import tornado.web
import json

UPLOAD_FILE_DIR = "Files/"
MOST_RECENT_FILE = "source"

class Base_Handler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.remote_ip not in ['127.0.0.1', '::1']:
            print(f"{self.request.remote_ip} blocked")
            self.send_error(403)

class Main_Handler(Base_Handler):
    def get(self):
        self.write('''
        <html>
        <body>
        <form action="/file/upload" enctype="multipart/form-data" method="post">
            <input type="file" name="filearg" accept=".csv">
            <input type="submit" value="Upload">
        </form>
        </body>
        </html>
        ''')

class Upload_File_Handler(Base_Handler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        print("fileinfo is", fileinfo)
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = MOST_RECENT_FILE + extn
        fh = open(UPLOAD_FILE_DIR + cname, 'wb')
        fh.write(fileinfo['body'])
        self.finish(cname + " uploaded")


class Current_Alloc_Handler(Base_Handler):
    def post(self):
        random_matching = {
            "students": [
                {
                    "name": "abcd", "eid": 1234, "skill_set": [2, 3]
                }, {
                    "name": "efgh", "eid": 6666, "skill_set": [0, 3]
                }
            ],
            "projects": [
                {
                    "name": "random project A",
                    "skill_req": [0, 1],
                }, {
                    "name": "random project B",
                    "skill_req": [3]
                }
            ],
            "skills": {
                0: "AI",
                1: "Analogue Circuit",
                2: "Embedded",
                3: "Operating System"
            }
        }
        self.write(json.dumps(random_matching))


application = tornado.web.Application([
    (r"/", Main_Handler),
    (r"/file/upload", Upload_File_Handler),
    # (r"/file/download"),
    (r"/matching", Current_Alloc_Handler),
    (r"/action/load", Main_Handler),
    # (r"/action/set_match"),
    # (r"/action/delete_match"),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
