import pandas
import students_file

Projects = {}


# If you want to add a project, do the following:
# Add a project_id, company_name, project_title, nda, ip, hw, sw, honors, and any other hard requirement
# in the sheet titled, "Project".
# Then, add the specifications that project needs in the sheet titled, "Specs".

# Each Excel sheet must have the same number of rows. Or else the program will break.
class Project:

    def __init__(self, project_id, comp_name, project_title, nda, ip, hw, sw, honors, specs, students):

        self._project_id = str(project_id)  # Each project has a unique project id.

        # Company and Project names.
        self._company_name = str(comp_name)
        self._project_title = str(project_title)

        # NDA and IP.
        self._NDA = int(nda)  # 1 - Yes 0 - No
        self._IP = int(ip)  # 1 - Yes 0 - No

        # Does project involve hardware or software?
        self._hardware = int(hw)  # 1 - min 5 - max
        self._software = int(sw)  # 1 - min 5 - max

        # Is the project an honor project?
        self._honors = int(honors)  # 1 - Yes 0 - No

        # All specifications a specific project will involve.
        self._specs = dict(specs)  # What exactly the project will involve.

        # The project's assigned students.
        self._students = set(students)  # Students involved in this project.

        # What students think of the project. Higher means more students want to be in that project.
        self._popularity = 0

        # Do the students enjoy being in this project? Higher means students don't want to be in this project.
        self._project_cost = 0

        # Dictionary for averages of student skills for all specifications.
        self._avg_spec_dict = {}

        # Average GPA of all students involved in this project.
        self._avg_student_gpa = 0

        # Add Project to list of projects.
        Projects[self._project_id] = self

    # For debugging. Prints out all relevant values.
    def __str__(self):
        print("===============================")

        print("Project ID: " + self._project_id)

        print("Company: " + self._company_name + " Project Name: " + self._project_title)
        print("NDA: " + str(self._NDA) + " IP: " + str(self._IP) + " Honors: " + str(self._honors))

        txt = "Hardware: {} Software: {}\n"
        print(txt.format(self._hardware, self._software))

        print("Specifications:")
        print(self._specs)
        print("\n")

        print("Students:")
        print(self._students)

        print("===============================")

    def get_project_id(self):
        return self._project_id

    def get_company_name(self):
        return self._company_name

    def get_project_title(self):
        return self._project_title

    def get_nda(self):
        return self._NDA

    def get_ip(self):
        return self._IP

    def get_honors(self):
        return self._honors

    def get_hardware(self):
        return self._hardware

    def get_software(self):
        return self._software

    def get_specs(self):
        return self._specs

    def get_spec(self, name):
        return self._specs.get(name)

    def get_students(self):
        return self._students

    def get_popularity(self):
        return self._popularity

    def set_popularity(self, new_popularity):
        self._popularity = new_popularity

    def add_popularity(self, number):
        self._popularity += number

    def set_specs(self, new_specs):
        self._specs = new_specs

    def set_students(self, new_students):
        self._students = new_students

    def add_student(self, student_eid):
        self._students.add(student_eid)

    def del_student(self, student_eid):
        self._students.remove(student_eid)

    def del_all_students(self):
        self._students.clear()

    def get_num_students(self):
        return len(self._students)

    # If the project has an NDA but the student dislikes NDA, return False. Else True.
    def check_nda(self, student):
        if self.get_nda() == 1 and student.get_nda() == 0:
            return False
        return True

    # If the project has an IP but the student dislikes IP, return False. Else True.
    def check_ip(self, student):
        if self.get_ip() == 1 and student.get_ip() == 0:
            return False
        return True

    # If the project is not an Honors Project, return True.
    # If the project's number of honor students is less than half the total number of students, return False. Else True.
    def check_honor(self, student):
        if self._honors == 0:
            return True

        honor_students = 0  # An honor student is a student with >= 3.5 GPA
        num_students = len(self._students) + 1

        if student.get_gpa() > 3.5:
            honor_students += 1

        for eid in self._students:

            student_gpa = students_file.Students[eid].get_gpa()

            if student_gpa >= 3.5:
                honor_students += 1

        # Odd number of students in project.
        if num_students % 2 == 1:
            half = int(num_students / 2) + 1

        # Even number of students in project.
        else:
            half = num_students / 2

        if honor_students < half:
            return False
        return True

    # If the project is hardware only but a student is software only, return False.
    # If the project is software only but a student is hardware only, return False.
    # Else True.
    def check_focus(self, student):
        if self.get_software() == 0 and student.get_focus() == 1:
            return False
        elif self.get_hardware() == 0 and student.get_focus() == 0:
            return False
        return True

    # Checks NDA, IP, Honors.
    def check_all(self, student):
        if self.check_nda(student) is False or self.check_ip(student) is False or self.check_honor(student) is False:
            return False
        return True

    # Checks specification. If a student's skill at a spec is below the project's needed spec skill, return False.
    # Else True.
    def check_spec(self, student, spec):
        if student.get_specs().get(spec) < self.get_spec(spec):
            return False
        return True

    # Checks all specs a project has with a student. If this returns True, then that student is perfectly
    # compatible with this project.
    def check_all_specs(self, student):
        for spec in self.get_specs():
            if self.check_spec(student, spec) is False:
                return False
        return True

    def set_avg_spec_dict(self, new_dict):
        self._avg_spec_dict = new_dict

    def set_avg_student_gpa(self, new_gpa):
        self._avg_student_gpa = new_gpa

    def get_avg_student_gpa(self):
        return self._avg_student_gpa

    def get_avg_spec_dict(self):
        return self._avg_spec_dict

    def get_project_cost(self):
        return self._project_cost

    def set_project_cost(self, new_project_cost):
        self._project_cost = new_project_cost


# Read each project's row and obtains all information on that row. Gets project's specifications and the project info
# and creates a project object and assigns into dictionary of projects with project_ID as the key.
def __read_project_row(projects_df, project_specs_df, row_number):
    specs = {}

    for spec in project_specs_df.columns:
        spec = str(spec)
        specs[spec] = \
            (int(project_specs_df.at[int(row_number), spec]))

    # If you added anything that is not a spec, include it in the constructor and in here.
    Project(projects_df.at[row_number, "Project_ID"],
            projects_df.at[row_number, "Company"],
            projects_df.at[row_number, "Project_Title"],
            projects_df.at[row_number, "NDA"],
            projects_df.at[row_number, "IP"],
            projects_df.at[row_number, "Hardware"],
            projects_df.at[row_number, "Software"],
            projects_df.at[row_number, "Honor"],
            specs,
            [])


# Call this method to initialize Projects dictionary and read entire Excel file.
# Input: project file + project file's filepath
def read_projects(filepath, excel):
    xlsx = pandas.ExcelFile(filepath + excel)

    project_main_df = pandas.read_excel(xlsx, "Project")
    project_specs_df = pandas.read_excel(xlsx, "Specs")

    # projects_df.shape[0] is the number of rows in the Excel sheet.
    for num in range(project_main_df.shape[0]):
        __read_project_row(project_main_df, project_specs_df, num)


# Debug function. Prints all project values.
def print_all_projects():
    # Assume projects Excel file has been read into the Projects dictionary.
    for project in Projects.values():
        print(project.__str__())

# read_projects("..\\..\\Samples\\CSVs\\", "Fall_2022_Edit_1.02_Companies.xlsx")
# print_all_projects()
