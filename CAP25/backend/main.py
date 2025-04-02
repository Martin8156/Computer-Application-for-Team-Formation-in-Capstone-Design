import os
import signal
import tornado.ioloop
import tornado.web
import json
import verifier
import asyncio

UPLOAD_FILE_DIR = "files/"
MOST_RECENT_FILE = "source"
RES_FILE = UPLOAD_FILE_DIR + "out.json"
STU_FILE = UPLOAD_FILE_DIR + "Student.csv"
COM_FILE = UPLOAD_FILE_DIR + "Company.csv"
output_csv = UPLOAD_FILE_DIR + "out.csv"

solver_proc = None

class Base_Handler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.remote_ip not in ["127.0.0.1", "::1"]:
            print(f"{self.request.remote_ip} blocked")
            self.send_error(403)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
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
    async def post(self):

        global solver_proc
        
        self.set_header("Content-Type", "text/plain")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")

        # Start the solver process
        # according to example: https://docs.python.org/3.13/library/asyncio-subprocess.html

        if os.path.exists(RES_FILE):
            with open(RES_FILE, 'r') as file:
                print(f"Reading from {RES_FILE}")
                data = json.load(file)

                self.write(json.dumps(data) + '\n')
                self.flush()
        
        if solver_proc is None:
            return

        while True:
            line = await solver_proc.stdout.readline()
            if not line:  # EOFs
                break

            try:
                self.write(line.decode('utf-8'))
                self.flush()
            
            except Exception as e:
                print(f"Error: {str(e)}")
                break




class Alloc_Solve_Handler(Base_Handler):
    async def post(self):
        global solver_proc

        print("?????")

        if solver_proc is not None:
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
        
        
        verification_errors = []
        verification_errors = verifier.verifier(COM_FILE, STU_FILE)
        if verification_errors != "Success":
            self.write(json.dumps({
                "result": "err", 
                "msg": f"Verification failed: {verification_errors}"
            }))
            return
    
        self.write(json.dumps({"result": "success", "msg": "Solver started"}))
        self.finish()

        script_path = "backend/solver2.py"
        
        # really important to add -u to allow real-time output
        solver_proc = await asyncio.create_subprocess_shell(
            f"python -u {script_path}", 
            stdout=asyncio.subprocess.PIPE
        )

        await solver_proc.wait()
        
        solver_proc = None


class Solver_Kill_Handler(Base_Handler):
    def get(self):
        global solver_proc
        if solver_proc is not None:
            # on windows and macos it's sigint | sigterm
            # possibly change to proc.terminate() for future version

            os.kill(solver_proc.pid, signal.SIGINT)
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


class MatchHandler(Base_Handler):
    def get(self):
        if os.path.exists(RES_FILE):
            with open(RES_FILE, 'r') as file:
                data = json.load(file)
                self.write(data)
        else:
            self.write({
                "students": [],
                "projects": [],
                "skills": {},
                "matching": {}
            })

    def post(self):
        data = json.loads(self.request.body)
        with open(RES_FILE, 'w') as file:
            json.dump(data, file)
        self.write({"status": "success"})


def make_app():
    return tornado.web.Application([
        (r"/match", MatchHandler),
        (r"/", Main_Handler),
        (r"/file/upload", Upload_File_Handler),
        # (r"/file/download"),
        (r"/matching", Current_Alloc_Handler),
        (r"/action/load", Main_Handler),
        # (r"/action/set_match"),
        # (r"/action/delete_match"),
        (r"/action/solve", Alloc_Solve_Handler),
        (r"/action/kill", Solver_Kill_Handler),
        (r"/action/output-csv", CSV_Output_Handler),
    ])


if __name__ == "__main__":
    print("Server started")

    # Ensure the Files directory exists and has correct permissions
    if not os.path.exists(UPLOAD_FILE_DIR):
        os.makedirs(UPLOAD_FILE_DIR)
    
    # The chmod problem was mainly caused by opening files in other apps, just don't do that

    # Initialize the output file with empty data structure
    with open(RES_FILE, 'w') as file:
        json.dump({
            "students": [],
            "projects": [],
            "skills": {},
            "matching": {}
        }, file)

    application = make_app()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
