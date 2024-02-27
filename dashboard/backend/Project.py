import grouping

DEBUG = True

Projects = {}


class Project:

    def __init__(self, project_id, comp_name, nda, ip, hw, sw, tech, extra, students):
        self._project_id = str(project_id)  # Each project has a unique project id.
        self._company_name = str(comp_name)
        self._NDA = int(nda)
        self._IP = int(ip)
        self._hardware = int(hw)  # 1 - min 5 - max
        self._software = int(sw)  # 1 - min 5 - max
        self._tech_cores = dict(tech)  # Tech cores with their int involvements.
        self._extra_specs = dict(extra)  # Company extras
        self._students = set(students)  # Students involved in this project.

        Projects[self._project_id] = self

    def __str__(self):
        print("===============================")
        print("Project ID: " + self._project_id)
        print("NDA: " + str(self._NDA) + " IP: " + str(self._IP))
        txt = "Hardware: {} Software: {}\n"
        print(txt.format(self._hardware, self._software))
        print("Tech Cores:")
        print(self._tech_cores)
        print("\n")
        print("Extra Specs:")
        print(self._extra_specs)
        print("\n")
        print("Students:")
        print(self._students)
        print("===============================")

    def get_project_id(self):
        return self._project_id

    def get_nda(self):
        return self._NDA

    def get_ip(self):
        return self._IP

    def get_hardware(self):
        return self._hardware

    def get_software(self):
        return self._software

    def get_tech_cores(self):
        return self._tech_cores

    def get_extra_specs(self):
        return self._extra_specs

    def set_tech_cores(self, new_tech_cores):
        self._tech_cores = new_tech_cores

    def set_extra_specs(self, new_extra_specs):
        self._extra_specs = new_extra_specs

    def set_students(self, new_students):
        self._students = new_students
"""
CVS Format:
0 - Projects (String)
1 - Company Name (String)
2 - NDA (Int)
3 - IP  (Int)
4 - Hardware Involvement (Int)
5 - Software Involvement (Int)
6-13 - Tech Cores. Assume 8. If not, update NUM_TECH_CORES (Int)
14+ - Extra Specifications (Int)
"""
NUM_TECH_CORES = 8


def __read_project_row(df, row_number):
    # For future, maybe have the argument be the filepath + name instead of csv name.
    # df = grouping.get_csv_sample("Fall_2022_Edit_1.01_Companies.csv")

    tech_cores = {}
    extra_specs = {}
    count = 0
    for column_label in df.columns:
        if 6 <= count < (6 + NUM_TECH_CORES):
            tech_cores[str(df.columns[count])] = int(df.at[row_number, column_label])
        elif count >= (6 + NUM_TECH_CORES):
            extra_specs[str(df.columns[count])] = int(df.at[row_number, column_label])

        count = count + 1

    # print(tech_cores)
    # print(extra_specs)

    project = Project(df.at[row_number, "Project"],
                      df.at[row_number, "Company"],
                      df.at[row_number, "NDA"],
                      df.at[row_number, "IP"],
                      df.at[row_number, "Hardware"],
                      df.at[row_number, "Software"],
                      tech_cores, extra_specs, [])


def __get_num_rows_in_csv(df):
    count = 0
    for row_label in df.index:
        count = count + 1

    return count


# Call this method to initialize Projects dictionary and read entire CSV file.
def read_projects_csv(df):
    num_rows = __get_num_rows_in_csv(df)
    for num in range(num_rows):
        __read_project_row(df, num)


# O(N) time. Maybe introduce parallel programming to speed up?
def get_average(column_label):
    col_str = str(column_label).lower()

    sum = 0
    count = 0
    for project in Projects:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Projects[project].get_tech_cores():
            sum = sum + Projects[project].get_tech_cores().get(column_label)
        elif column_label in Projects[project].get_extra_specs():
            sum = sum + Projects[project].get_extra_specs().get(column_label)
        elif col_str == "hardware":
            sum = sum + Projects[project].get_hardware()
        elif col_str == "software":
            sum = sum + Projects[project].get_software()
        elif col_str == "nda":
            sum = sum + Projects[project].get_nda()
        elif col_str == "ip":
            sum = sum + Projects[project].get_ip()
        count = count + 1

    average = sum / count
    if DEBUG:
        txt = "The average value of " + column_label + " is {}."
        print(txt.format(average))
    return average


def get_all_averages(df):
    for column in df.columns():
        get_average(column)


# O(N) time. Maybe introduce parallel programming to speed up?
def get_frequency(column_label, value):
    col_str = str(column_label).lower()
    int_value = int(value)
    count = 0
    for project in Projects:
        # print(Projects[project].get_tech_cores().get(column_label))
        if column_label in Projects[project].get_tech_cores():
            if Projects[project].get_tech_cores().get(column_label) == int_value:
                count = count + 1
        elif column_label in Projects[project].get_extra_specs():
            if Projects[project].get_extra_specs().get(column_label) == int_value:
                count = count + 1
        elif col_str == "hardware":
            if Projects[project].get_hardware() == int_value:
                count = count + 1
        elif col_str == "software":
            if Projects[project].get_software() == int_value:
                count = count + 1
        elif col_str == "nda":
            if Projects[project].get_nda() == int_value:
                count = count + 1
        elif col_str == "ip":
            if Projects[project].get_ip == int_value:
                count = count + 1
    if DEBUG:
        txt = "The frequency of {} for " + column_label + " is {}."
        print(txt.format(value, count))
    return count


def sort_projects(column_label, max_value):
    col_str = str(column_label).lower()
    ordered_list = []
    for num in range(0, max_value + 1):
        for project in Projects:
            # print(Projects[project].get_tech_cores().get(column_label))
            if column_label in Projects[project].get_tech_cores():
                if Projects[project].get_tech_cores().get(column_label) == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif column_label in Projects[project].get_extra_specs():
                if Projects[project].get_extra_specs().get(column_label) == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif col_str == "hardware":
                if Projects[project].get_hardware() == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif col_str == "software":
                if Projects[project].get_software() == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif col_str == "nda":
                if Projects[project].get_nda() == num:
                    ordered_list.append(Projects[project].get_project_id())
            elif col_str == "ip":
                if Projects[project].get_ip == num:
                    ordered_list.append(Projects[project].get_project_id())

    if DEBUG:
        for obj in ordered_list:
            txt = obj + " has value {} for " + str(column_label)
            print(txt.format(Projects[obj].get_tech_cores().get(column_label)))

    return ordered_list


df = grouping.get_csv_sample("Fall_2022_Edit_1.01_Companies.csv")
read_projects_csv(df)
#sort_projects("Communication, Signal Processing, Networks and Systems", 5)

get_average("Communication, Signal Processing, Networks and Systems")

get_frequency("Communication, Signal Processing, Networks and Systems", 4)