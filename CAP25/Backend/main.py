import os
import tornado.ioloop
import tornado.web
import json
import subprocess

UPLOAD_FILE_DIR = "Files/"
MOST_RECENT_FILE = "source"
RES_FILE = UPLOAD_FILE_DIR + "out.json"
STU_FILE = UPLOAD_FILE_DIR + "Student.csv"
COM_FILE = UPLOAD_FILE_DIR + "Company.csv"

class Base_Handler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.remote_ip not in ["127.0.0.1", "::1"]:
            print(f"{self.request.remote_ip} blocked")
            self.send_error(403)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Content-Type", "application/json")

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
        try:
            with open(RES_FILE, 'r') as file:
                print(f"Reading from {RES_FILE}")
                data = json.load(file)

                # Validate data before sending
                if not isinstance(data, dict):
                    raise ValueError("Invalid data format")
                
                required_keys = ["students", "projects", "skills", "matching"]
                if not all(key in data for key in required_keys):
                    raise ValueError("Missing required keys in data")
                
                print(f"Loaded data: {json.dumps(data)[:200]}...")

                self.set_header("Content-Type", "application/json")
                self.write(json.dumps(data))

        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:

            print(f"Error reading {RES_FILE}: {str(e)}")

            # Return empty but valid JSON structure
            self.write(json.dumps({
                "students": [],
                "projects": [],
                "skills": {},
                "matching": {}
            }))


class Alloc_Solve_Handler(Base_Handler):
    def post(self):
        
        if not os.path.exists(RES_FILE):
            # By design the solver will remove out.json and output a new one
            # So if there isn't one in the dir means we are having a running soler
            self.write(json.dumps(
                {"result": "err", "msg": "existing an ongoing solver"}
            ))
            return

        if not os.path.exists(STU_FILE):
            self.write(json.dumps({
                "result": "err", 
                "msg": "Student file does not exist, please upload that first"
            }))
            return
        
        if not os.path.exists(COM_FILE):
            self.write(json.dumps({
                "result": "err", 
                "msg": "Company file does not exist, please upload that first"
            }))
            return
        
        # Start the solver process
        subprocess.Popen(['python', 'Backend/solver.py'])
        
        self.write(json.dumps({
            "result": "success", 
            "msg": "Solver started"
        }))


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

    # Ensure the Files directory exists and has correct permissions
    if not os.path.exists(UPLOAD_FILE_DIR):
        os.makedirs(UPLOAD_FILE_DIR)
        
    # Ensure out.json is writable
    if os.path.exists(RES_FILE):
        os.chmod(RES_FILE, 0o666)  # Make file readable and writable

    # Initialize the output file with empty data structure
    if not os.path.exists(RES_FILE):
        with open(RES_FILE, 'w') as file:
            json.dump({
                "students": [],
                "projects": [],
                "skills": {},
                "matching": {}
            }, file)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
