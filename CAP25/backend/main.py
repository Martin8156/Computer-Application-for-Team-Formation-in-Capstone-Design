import os
import signal
import tornado.ioloop
import tornado.web
import json
import subprocess

import asyncio

UPLOAD_FILE_DIR = "files/"
MOST_RECENT_FILE = "source"
RES_FILE = UPLOAD_FILE_DIR + "out.json"
STU_FILE = UPLOAD_FILE_DIR + "Student.csv"
COM_FILE = UPLOAD_FILE_DIR + "Company.csv"
output_csv = UPLOAD_FILE_DIR + "out.csv"

solver_pid = None

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
        # print("fileinfo is", fileinfo)
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
    async def post(self):
        global solver_pid

        if solver_pid is not None:
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

        
        self.set_header("Content-Type", "text/plain")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

        # Start the solver process
        # according to example: https://docs.python.org/3.13/library/asyncio-subprocess.html
        
        script_path = "backend/solver.py"
        
        # really important to add -u to allow real-time output
        proc = await asyncio.create_subprocess_shell(
            f"python -u {script_path}", 
            stdout=asyncio.subprocess.PIPE
        )
        
        solver_pid = proc.pid

        while True:
            line = await proc.stdout.readline()
            if not line:  # EOFs
                break

            self.write(line.decode('utf-8'))
            self.flush()
        
        solver_pid = None


class Solver_Kill_Handler(Base_Handler):
    def get(self):
        global solver_pid
        if solver_pid:
            os.kill(solver_pid, signal.SIGINT)
            self.write(json.dumps({"result": "success", "msg": "Solver killed"}))
        else:
            self.write(json.dumps({"result": "success", "msg": "No solver running"}))


class CSV_Output_Handler(Base_Handler):
    def get(self):
        try:
            print(f"Start outputing CSV file from {output_csv}")
            self.set_header("Content-Type", "text/csv")
            self.set_header("Content-Disposition", "attachment; filename=\"output.csv\"")
            with open(output_csv, 'r') as f:
                self.write(f.read())
            self.finish()
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"result": "error", "msg": f"Error reading CSV file: {str(e)}"}))

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
        (r"/action/output-csv", CSV_Output_Handler),
    ]
)


if __name__ == "__main__":
    print("Server started")

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
