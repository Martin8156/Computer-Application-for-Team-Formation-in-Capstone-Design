import pandas

Students = {}


# Each student object is initialized and added to the Students dictionary above.
# To add a new student, add the information in a new row for each Excel sheet.
# All Excel sheets must have an equal amount of rows, or else the program will break.
class Student:
    def __init__(self, eid, name, gpa, honors, sp, focus, nda, ip,
                 partner_eid, partner_importance,
                 specs, project_prefs):

        self._EID = str(eid)
        self._name = str(name)
        self._GPA = float(gpa)

        # If student wants to be in a Self-Proposed or Honors project.
        self._honors = int(honors)  # 0 - No 1 - Yes
        self._SP = int(sp)  # 0 - No 1 - Yes

        # Whether student wants to do software, hardware, or both types of work.
        self._focus = int(focus)  # Hardware(0), Software(1), or Both(2).

        # Whether student wants to sign an NDA or an IP.
        self._NDA = int(nda)  # 0 - No 1 - Yes
        self._IP = int(ip)  # 0 - No 1 - Yes

        # Each student is initially not assigned to a project.
        self._project_id = ""

        # Student partner to be with.
        # For the future, have partner importance return an integer instead.
        # from 0 to 5 with 0 being not important and 5 being very important.
        self._partner_eid = str(partner_eid)
        self._partner_importance = str(partner_importance)

        # Student comfortability ratings with specifications and preference for projects.
        self._specs = dict(specs)  # (string: int) = (specification: specification skill)
        self._project_prefs = dict(project_prefs)  # (string: int) = (project id: willingness to join)

        # Insert this student object into the dictionary with the eid as the key.
        Students[eid] = self  # (string: object) = (eid: student)

    # End Student Constructor

    # For debugging. Prints out all relevant values.
    def __str__(self):
        print("===============================")
        print("Student EID: " + self._EID)
        print("Name: " + self._name + " GPA: " + str(self._GPA))
        print("NDA: " + str(self._NDA) + " IP: " + str(self._IP))
        print("Focus: " + str(self._focus))
        print("Honors: " + str(self._honors) + " SP: " + str(self._SP))

        print("Project ID: " + self._project_id)

        print("Partner EID: " + self._partner_eid + " Partner Importance: "
              + self._partner_importance)

        print("Specifications:")
        print(self._specs)
        print("\n")
        print("Project Preferences:")
        print(self._project_prefs)
        print("===============================")
        return ""

    def get_eid(self):
        return self._EID

    def get_name(self):
        return self._name

    def get_gpa(self):
        return self._GPA

    def get_honors(self):
        return self._honors

    def get_sp(self):
        return self._SP

    def get_focus(self):
        return self._focus

    def get_nda(self):
        return self._NDA

    def get_ip(self):
        return self._IP

    def get_project_id(self):
        return self._project_id

    def get_partner_eid(self):
        return self._partner_eid

    def get_partner_importance(self):
        return self._partner_importance

    def get_specs(self):
        return self._specs

    def get_spec(self, name):
        return self.get_specs().get(name)

    def get_project_prefs(self):
        return self._project_prefs

    def set_project_id(self, project_id):
        self._project_id = project_id


# For each student, read their spec skills, their project preferences, and make a new Student object with
# all their information.
def __read_student_row(students_df, project_prefs_df, student_specs_df, row_number):
    specs = {}

    # Adds each spec to a dictionary.
    for spec in student_specs_df.columns:
        spec = str(spec)
        specs[spec] = int(student_specs_df.at[int(row_number), spec])

    project_prefs = {}

    # Adds each project preference to a dictionary.
    for project_id in project_prefs_df.columns:
        project_prefs[str(project_id)] = int(project_prefs_df.at[int(row_number), str(project_id)])

    # Make a new student object with that student's EID being the key.
    Student(students_df.at[row_number, "EID"],
            students_df.at[row_number, "Name"],
            students_df.at[row_number, "GPA"],
            students_df.at[row_number, "Honors"],
            students_df.at[row_number, "SP"],
            students_df.at[row_number, "Hardware, Software, or Both"],
            students_df.at[row_number, "NDA"],
            students_df.at[row_number, "IP"],
            students_df.at[row_number, "Partner_EID"],
            students_df.at[row_number, "Partner_Importance"],
            specs,
            project_prefs)


# Read the Student Excel file. There should be 3 sheets titled: "Student_Info", "Project_Preferences", and "Specs".
def read_student_excel(filepath, excel):
    xlsx = pandas.ExcelFile(filepath + excel)

    student_df = pandas.read_excel(xlsx, "Student_Info")
    project_prefs_df = pandas.read_excel(xlsx, "Project_Preferences")
    student_specs_df = pandas.read_excel(xlsx, "Specs")

    for num in range(student_df.shape[0]):
        __read_student_row(student_df, project_prefs_df, student_specs_df, num)


# Debug function. Prints all values of each student.
def print_all_students():
    # Assume projects Excel file has been read into the Projects dictionary.
    for student in Students.values():
        print(student.__str__())

# read_student_excel("..\\..\\Samples\\CSVs\\", "Fall_2022_Edit_1.05_Students.xlsx")
# print_all_students()
