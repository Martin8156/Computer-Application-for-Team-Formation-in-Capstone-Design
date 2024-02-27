import grouping
class Student:
    def __init__(self, eid, name, gpa, focus,
                 nda, ip,
                 preference, pref_eid,
                 pref_importance,
                 honors,
                 project_id):
        self.eid = eid
        self.name = name
        self.gpa = gpa
        self.focus = focus
        self.NDA = nda
        self.IP = ip
        self.preference = preference
        self.pref_eid = pref_eid
        self.pref_importance = pref_importance
        self.project_id = project_id


Studentdb = grouping.get_csv_sample("Fall_2022_Edit_1.0_Students.csv")

print(Studentdb.info())