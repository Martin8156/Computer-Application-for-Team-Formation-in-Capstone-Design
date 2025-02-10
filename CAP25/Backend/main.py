import os
import tornado.ioloop
import tornado.web
import json
import subprocess

UPLOAD_FILE_DIR = "Files/"
MOST_RECENT_FILE = "source"
RES_FILE = "Files/out.json"
STU_FILE = UPLOAD_FILE_DIR + "Student.csv"
COM_FILE = UPLOAD_FILE_DIR + "Company.csv"


class Base_Handler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.remote_ip not in ["127.0.0.1", "::1"]:
            print(f"{self.request.remote_ip} blocked")
            self.send_error(403)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()


class Main_Handler(Base_Handler):
    def get(self):
        self.write(
            """
        <html>
        <body>
        <form action="/file/upload" enctype="multipart/form-data" method="post">
            <input type="file" name="filearg" accept=".csv">
            <select name="file_type" id="file_type">
                <option value="Student">Student Preference</option>
                <option value="Company">Company Preference</option>
            </select>
            <input type="submit" value="Upload">
        </form>
        </body>
        </html>
        """
        )


class Upload_File_Handler(Base_Handler):
    def post(self):
        # Do the parsing to verify the file
        # Sendback the error message or needed file
        # Start new process of solving combination
        fileinfo = self.request.files["filearg"][0]
        print("fileinfo is", fileinfo)
        fname = fileinfo["filename"]
        extn = os.path.splitext(fname)[1]
        cname = self.get_body_argument("file_type") + extn
        fh = open(UPLOAD_FILE_DIR + cname, "wb")
        fh.write(fileinfo["body"])
        self.finish(cname + " uploaded")


class Current_Alloc_Handler(Base_Handler):

    def post(self):
        random_matching = {
            "students": [
                {"name": "alice", "eid": 1234, "skill_set": {0: 1, 1: 5, 2: 3, 3: 2}},
                {"name": "bob", "eid": 6666, "skill_set": {0: 4, 1: 2, 2: 2, 3: 4}},
                {"name": "charlie", "eid": 4321, "skill_set": {0: 3, 1: 2, 2: 2, 3: 2}},
                {"name": "david", "eid": 5555, "skill_set": {0: 2, 1: 3, 2: 1, 3: 5}},
            ],
            "projects": [
                {
                    "name": "random project A",
                    "skill_req": {0: 4, 1: 3, 2: 1, 3: 2},
                },
                {"name": "random project B", "skill_req": {0: 2, 1: 3, 2: 5, 3: 1}},
            ],
            "skills": {
                0: "AI",
                1: "Analogue Circuit",
                2: "Embedded",
                3: "Operating System",
            },
            "matching": {
                0: [0, 2],
                1: [1, 3],
            },
        }
        self.write(json.dumps(random_matching))


class Alloc_Solve_Handler(Base_Handler):
    def post(self):
        if not os.path.exists(RES_FILE):
            self.write(json.dumps(
                {"result": "err", "msg": "existing an ongoing solver"}
            ))
            return
        
        if not os.path.exists(STU_FILE):
            self.write(json.dumps(
                {"result": "err", "msg": "student file does not exist, please upload that first"}
            ))
            return
        
        if not os.path.exists(COM_FILE):
            self.write(json.dumps(
                {"result": "err", "msg": "company file does not exist, please upload that first"}
            ))
            return
        
        subprocess.Popen(['python', 'Backend/solver.py'])
        self.write(json.dumps({"result": "success", "msg": "solver started"}))


application = tornado.web.Application(
    [
        (r"/", Main_Handler),
        (r"/file/upload", Upload_File_Handler),
        # (r"/file/download"),
        (r"/matching", Current_Alloc_Handler),
        (r"/action/load", Main_Handler),
        # (r"/action/set_match"),
        # (r"/action/delete_match"),
        (r"/action/solve", Alloc_Solve_Handler),
    ]
)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
