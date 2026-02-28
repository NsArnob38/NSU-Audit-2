#!/usr/bin/env python3
"""
NSU Audit Core — 2000 Unique Student Transcript Generator
Generates 2000 individual transcript CSV files in a 'transcripts/' directory,
each representing a different student with varied academic profiles.
"""

import csv
import os
import random
import sys
from engine.credit_engine import SEMESTERS

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ─── Course Pools (Post-Fall 2014, 130-credit curriculum) ───

# CSE Major Core (42 credits)
CSE_MAJOR_CORE = {
    "CSE173": ("Discrete Mathematics", 3),
    "CSE215": ("Programming Language II", 3),
    "CSE215L": ("Programming Language II Lab", 1),
    "CSE225": ("Data Structures & Algorithms", 3),
    "CSE225L": ("Data Structures & Algorithms Lab", 1),
    "CSE231": ("Digital Logic Design", 3),
    "CSE231L": ("Digital Logic Design Lab", 1),
    "CSE299": ("Junior Design Project", 1),
    "CSE311": ("Database Management Systems", 3),
    "CSE311L": ("Database Management Systems Lab", 1),
    "CSE323": ("Operating Systems Design", 3),
    "CSE327": ("Software Engineering", 3),
    "CSE331": ("Microprocessor Interfacing", 3),
    "CSE331L": ("Microprocessor Interfacing Lab", 1),
    "CSE332": ("Computer Organization & Architecture", 3),
    "CSE373": ("Design & Analysis of Algorithms", 3),
    "CSE425": ("Concepts of Programming Languages", 3),
    "EEE141": ("Electrical Circuits I", 3),
    "EEE141L": ("Electrical Circuits I Lab", 1),
    "EEE111": ("Analog Electronics I", 3),
    "EEE111L": ("Analog Electronics I Lab", 1),
}

# CSE Capstone + Engineering Economics (7 credits)
CSE_CAPSTONE = {
    "CSE499A": ("Senior Capstone Design I", 2),
    "CSE499B": ("Senior Capstone Design II", 2),
    "EEE452": ("Engineering Economics", 3),
}

# SEPS Core (38 credits)
CSE_SEPS_CORE = {
    "CSE115": ("Programming Language I", 3),
    "CSE115L": ("Programming Language I Lab", 1),
    "MAT120": ("Calculus I", 3),
    "MAT125": ("Linear Algebra", 3),
    "MAT130": ("Calculus II", 3),
    "MAT250": ("Calculus III", 3),
    "MAT350": ("Probability & Statistics", 3),
    "MAT361": ("Differential Equations", 3),
    "PHY107": ("Physics I", 3),
    "PHY107L": ("Physics I Lab", 1),
    "PHY108": ("Physics II", 3),
    "PHY108L": ("Physics II Lab", 1),
    "CHE101": ("Chemistry I", 3),
    "CHE101L": ("Chemistry I Lab", 1),
    "BIO103": ("Biology I", 3),
    "BIO103L": ("Biology I Lab", 1),
    "CEE110": ("Engineering Drawing", 1),
}

# CSE GED (University Core)
CSE_GED = {
    "ENG103": ("Intermediate Composition", 3),
    "ENG105": ("Advanced Writing Skills", 3),
    "ENG111": ("Public Speaking", 3),
    "PHI104": ("Introduction to Ethics", 3),
    "HIS101": ("Bangladesh History & Culture", 3),
    "HIS102": ("World Civilization", 3),
    "CSE101": ("Introduction to Python Programming", 3),
    "CSE145": ("Introduction to Artificial Intelligence", 3),
    "CSE226": ("Fundamentals of Vibe Coding", 3),
}

CSE_GED_CHOICE_1 = {"ECO101": ("Intro to Microeconomics", 3), "ECO104": ("Intro to Macroeconomics", 3)}
CSE_GED_CHOICE_2 = {"POL101": ("Intro to Political Science", 3), "POL104": ("Political Science", 3)}
CSE_GED_CHOICE_3 = {"SOC101": ("Intro to Sociology", 3), "ANT101": ("Anthropology", 3),
                     "ENV203": ("Environmental Studies", 3), "GEO205": ("Geography", 3)}

CSE_ELECTIVES_400 = {
    "CSE421": ("Machine Learning", 3),
    "CSE423": ("Data Mining", 3),
    "CSE445": ("Computer Vision", 3),
    "CSE461": ("Robotics", 3),
    "CSE471": ("Compiler Design", 3),
}

OPEN_ELECTIVES = {
    "SOC201": ("Social Theory", 3),
    "PHI201": ("Logic", 3),
    "HIS201": ("Modern History", 3),
}

# BBA School Core (7 courses / 21 credits)
BBA_SCHOOL_CORE = {
    "ECO101": ("Intro to Microeconomics", 3),
    "ECO104": ("Intro to Macroeconomics", 3),
    "MIS107": ("Introduction to Computers", 3),
    "BUS251": ("Business Communication", 3),
    "BUS172": ("Introduction to Statistics", 3),
    "BUS173": ("Applied Statistics", 3),
    "BUS135": ("Business Mathematics", 3),
}

# BBA Core (12 courses / 36 credits)
BBA_CORE = {
    "ACT201": ("Intro to Financial Accounting", 3),
    "ACT202": ("Intro to Managerial Accounting", 3),
    "FIN254": ("Intro to Financial Management", 3),
    "LAW200": ("Legal Environment of Business", 3),
    "INB372": ("International Business", 3),
    "MKT202": ("Introduction to Marketing", 3),
    "MIS207": ("Management Information Systems", 3),
    "MGT212": ("Principles of Management", 3),
    "MGT351": ("Human Resource Management", 3),
    "MGT314": ("Production Management", 3),
    "MGT368": ("Entrepreneurship", 3),
    "MGT489": ("Strategic Management", 3),
}

# BBA GED — Fixed (always required)
BBA_GED = {
    "ENG103": ("Intermediate Composition", 3),
    "ENG105": ("Advanced Composition", 3),
    "PHI401": ("Ethics / Philosophy", 3),
}

# GED Choice Groups
BBA_GED_CHOICE_LANG = {"BEN205": ("Bengali Literature", 3), "ENG115": ("English Literature", 3), "CHN101": ("Chinese Language", 3)}
BBA_GED_CHOICE_HIS = {"HIS101": ("Bangladesh History", 3), "HIS102": ("World Civilization", 3),
                       "HIS103": ("History of South Asia", 3), "HIS205": ("Modern History", 3)}  # pick 2
BBA_GED_CHOICE_POL = {"POL101": ("Intro to Political Science", 3), "POL104": ("Political Science", 3),
                       "PAD201": ("Public Administration", 3)}
BBA_GED_CHOICE_SOC = {"SOC101": ("Intro to Sociology", 3), "GEO205": ("Geography", 3), "ANT101": ("Anthropology", 3)}
BBA_GED_CHOICE_SCI = {"BIO103": ("Biology I", 3), "ENV107": ("Environmental Science", 3), "PBH101": ("Public Health", 3),
                       "PSY101": ("Intro to Psychology", 3), "PHY107": ("Physics I", 3), "CHE101": ("Chemistry I", 3)}  # pick 3
BBA_GED_CHOICE_LAB = {"BIO103L": ("Biology I Lab", 1), "ENV107L": ("Environmental Science Lab", 1),
                       "PBH101L": ("Public Health Lab", 1), "PSY101L": ("Psychology Lab", 1),
                       "PHY107L": ("Physics I Lab", 1), "CHE101L": ("Chemistry I Lab", 1)}  # pick 1

BBA_INTERNSHIP = {"BUS498": ("Internship", 4)}

# BBA Concentration Course Pools — Curriculum 143 Major Map
BBA_CONC_COURSES = {
    "ACT": {
        "required": {"ACT310": ("Intermediate Accounting I", 3), "ACT320": ("Intermediate Accounting II", 3),
                     "ACT360": ("Advanced Managerial Accounting", 3), "ACT370": ("Taxation", 3)},
        "elective": {"ACT380": ("Audit and Assurance", 3), "ACT460": ("Advanced Financial Accounting", 3),
                     "ACT430": ("Accounting Information Systems", 3), "ACT410": ("Financial Statement Analysis", 3)},
    },
    "FIN": {
        "required": {"FIN433": ("Financial Markets and Institutions", 3), "FIN440": ("Corporate Finance", 3),
                     "FIN435": ("Investment Theory", 3), "FIN444": ("International Financial Management", 3)},
        "elective": {"FIN455": ("Financial Modelling Using Excel", 3), "FIN464": ("Derivatives", 3),
                     "FIN470": ("Insurance and Risk Management", 3), "FIN480": ("Behavioural Finance", 3),
                     "FIN410": ("Financial Statement Analysis", 3)},
    },
    "MKT": {
        "required": {"MKT337": ("Promotional Management", 3), "MKT344": ("Consumer Behaviour", 3),
                     "MKT460": ("Strategic Marketing", 3), "MKT470": ("Marketing Research", 3)},
        "elective": {"MKT412": ("Services Marketing", 3), "MKT465": ("Brand Management", 3),
                     "MKT382": ("International Marketing", 3), "MKT417": ("Export-Import Management", 3),
                     "MKT330": ("Retail Management", 3), "MKT450": ("Marketing Channels", 3),
                     "MKT355": ("Agricultural Marketing", 3), "MKT445": ("Sales Management", 3),
                     "MKT475": ("Marketing Analytics", 3)},
    },
    "MGT": {
        "required": {"MGT321": ("Organizational Behavior", 3), "MGT330": ("Designing Effective Organizations", 3),
                     "HRM370": ("Managerial Skill Development", 3), "MGT410": ("Entrepreneurship II", 3)},
        "elective": {"MGT350": ("Managing Quality", 3), "MGT490": ("Project Management", 3),
                     "HRM470": ("Negotiations", 3), "HRM450": ("Industrial Relations", 3),
                     "MIS320": ("IT for Managers", 3)},
    },
    "HRM": {
        "required": {"HRM340": ("Training and Development", 3), "HRM360": ("Planning and Staffing", 3),
                     "HRM380": ("Compensation Theory and Practice", 3), "HRM450": ("Industrial Relations", 3)},
        "elective": {"HRM370": ("Managerial Skill Development", 3), "HRM499": ("Special Topics in HRM", 3),
                     "HRM470": ("Negotiations", 3)},
    },
    "MIS": {
        "required": {"MIS210": ("Computer Programming", 3), "MIS310": ("Systems Analysis", 3),
                     "MIS320": ("IT for Managers", 3), "MIS470": ("IT Project Management", 3)},
        "elective": {"MIS330": ("Database Systems", 3), "MIS410": ("Systems Design", 3),
                     "MIS450": ("IS Security", 3), "MGT490": ("Project Management", 3),
                     "MIS499": ("Special Topics in MIS", 3)},
    },
    "SCM": {
        "required": {"SCM310": ("Supply Chain Management", 3), "SCM320": ("Procurement and Inventory", 3),
                     "SCM450": ("Supply Chain Analytics", 3), "MGT460": ("Logistics Management", 3)},
        "elective": {"MGT360": ("Global Supply Chain", 3), "MGT390": ("Warehouse Management", 3),
                     "MGT470": ("Quality Management", 3), "MGT490": ("Project Management", 3)},
    },
    "ECO": {
        "required": {"ECO201": ("Intermediate Microeconomics", 3), "ECO204": ("Intermediate Macroeconomics", 3),
                     "ECO348": ("Mathematical Economics", 3), "ECO328": ("Econometrics", 3)},
        "elective": {"ECO244": ("Economic Development", 3), "ECO301": ("Monetary Economics", 3),
                     "ECO304": ("International Economics", 3), "ECO317": ("Public Economics", 3),
                     "ECO354": ("Advanced Microeconomics", 3), "ECO410": ("Development Economics", 3),
                     "ECO415": ("Public Finance", 3), "ECO441": ("Labor Economics", 3),
                     "ECO450": ("Game Theory", 3), "ECO460": ("International Trade", 3)},
    },
    "INB": {
        "required": {"INB400": ("International Trade and Finance", 3), "INB490": ("Cross-Cultural Management", 3),
                     "INB480": ("Global Business Strategy", 3), "MKT382": ("International Marketing", 3)},
        "elective": {"INB410": ("International Competitiveness", 3), "INB350": ("International Business Negotiation", 3),
                     "INB355": ("Country Risk Analysis", 3), "INB415": ("Emerging Markets", 3),
                     "INB450": ("Global Entrepreneurship", 3), "INB495": ("Special Topics in INB", 3),
                     "MKT417": ("Export-Import Management", 3)},
    },
}

BBA_CONC_NAMES = list(BBA_CONC_COURSES.keys())  # ["ACT", "FIN", ...]

ALL_COURSES = {}
for d in [CSE_MAJOR_CORE, CSE_CAPSTONE, CSE_SEPS_CORE, CSE_GED, CSE_GED_CHOICE_1, CSE_GED_CHOICE_2,
          CSE_GED_CHOICE_3, CSE_ELECTIVES_400, OPEN_ELECTIVES, BBA_SCHOOL_CORE, BBA_CORE, BBA_GED,
          BBA_GED_CHOICE_LANG, BBA_GED_CHOICE_HIS, BBA_GED_CHOICE_POL, BBA_GED_CHOICE_SOC,
          BBA_GED_CHOICE_SCI, BBA_GED_CHOICE_LAB, BBA_INTERNSHIP]:
    ALL_COURSES.update(d)
for conc_data in BBA_CONC_COURSES.values():
    ALL_COURSES.update(conc_data["required"])
    ALL_COURSES.update(conc_data["elective"])
ALL_COURSES["ENG102"] = ("Introduction to Composition", 3)
ALL_COURSES["MAT116"] = ("Pre-Calculus", 0)
ALL_COURSES["BUS112"] = ("Intro to Business Mathematics", 3)

# SEMESTERS imported from engine.credit_engine


# ─── Student Profile Types ───────────────────────────────

PROFILES = [
    "top_student",        # CGPA 3.5+, all courses done, eligible
    "good_student",       # CGPA 2.5-3.5, most courses done
    "struggling",         # CGPA 1.5-2.5, many retakes, probation risk
    "early_stage",        # Freshman/sophomore, few courses
    "mid_stage",          # Junior, about half done
    "nearly_done",        # Senior, missing 1-3 courses
    "retake_heavy",       # Many retakes and Fs
    "transfer_student",   # Several T grades
    "withdrawn_heavy",    # Many W grades
    "probation",          # CGPA < 2.0
]


def grade_for_profile(profile):
    """Return a weighted random grade based on student profile."""
    if profile == "top_student":
        return random.choices(
            ["A", "A-", "B+", "B", "B-", "C+"],
            weights=[30, 25, 20, 15, 7, 3], k=1)[0]
    elif profile == "good_student":
        return random.choices(
            ["A", "A-", "B+", "B", "B-", "C+", "C", "C-"],
            weights=[10, 15, 20, 20, 15, 10, 7, 3], k=1)[0]
    elif profile == "struggling":
        return random.choices(
            ["B", "B-", "C+", "C", "C-", "D+", "D", "F"],
            weights=[5, 8, 12, 20, 15, 15, 15, 10], k=1)[0]
    elif profile == "retake_heavy":
        return random.choices(
            ["C", "C-", "D+", "D", "F", "W"],
            weights=[15, 15, 15, 15, 25, 15], k=1)[0]
    elif profile == "probation":
        return random.choices(
            ["C-", "D+", "D", "F", "I"],
            weights=[15, 20, 25, 30, 10], k=1)[0]
    elif profile == "withdrawn_heavy":
        return random.choices(
            ["A", "B+", "B", "C+", "C", "D", "F", "W"],
            weights=[8, 10, 12, 10, 10, 5, 5, 40], k=1)[0]
    elif profile == "transfer_student":
        return random.choices(
            ["A", "A-", "B+", "B", "C+", "C", "T"],
            weights=[12, 12, 15, 15, 10, 10, 26], k=1)[0]
    else:
        return random.choices(
            ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "W"],
            weights=[8, 8, 10, 12, 10, 10, 10, 8, 7, 7, 6, 4], k=1)[0]


def sort_rows(rows):
    """Sort transcript rows chronologically by semester."""
    # Create a mapping for quick lookup
    sem_map = {sem: i for i, sem in enumerate(SEMESTERS)}
    # If a semester is not in the list (e.g. transfer), give it index -1
    return sorted(rows, key=lambda r: sem_map.get(r[4], -1))


def pick_semesters(n, start_idx=None):
    """Pick n sequential semesters starting from a random point."""
    if start_idx is None:
        start_idx = random.randint(0, max(0, len(SEMESTERS) - n))
    end = min(start_idx + n, len(SEMESTERS))
    return SEMESTERS[start_idx:end]


def generate_cse_student(profile, student_id):
    """Generate a CSE student transcript based on profile."""
    rows = []

    # Determine how many courses based on profile
    all_required = (list(CSE_MAJOR_CORE.keys()) + list(CSE_CAPSTONE.keys()) +
                    list(CSE_SEPS_CORE.keys()) + list(CSE_GED.keys()))

    if profile == "top_student":
        course_fraction = 1.0
    elif profile == "good_student":
        course_fraction = random.uniform(0.75, 0.95)
    elif profile == "nearly_done":
        course_fraction = random.uniform(0.90, 0.98)
    elif profile == "mid_stage":
        course_fraction = random.uniform(0.40, 0.60)
    elif profile == "early_stage":
        course_fraction = random.uniform(0.10, 0.30)
    elif profile in ("struggling", "retake_heavy", "probation"):
        course_fraction = random.uniform(0.30, 0.70)
    elif profile == "withdrawn_heavy":
        course_fraction = random.uniform(0.35, 0.65)
    elif profile == "transfer_student":
        course_fraction = random.uniform(0.50, 0.80)
    else:
        course_fraction = random.uniform(0.30, 0.80)

    n_courses = max(3, int(len(all_required) * course_fraction))
    selected = random.sample(all_required, min(n_courses, len(all_required)))

    # Assign semesters chronologically
    n_semesters = random.randint(2, min(10, len(SEMESTERS)))
    start = random.randint(0, len(SEMESTERS) - n_semesters)
    avail_sems = SEMESTERS[start:start + n_semesters]

    for code in selected:
        name, credits = ALL_COURSES[code]
        grade = grade_for_profile(profile)
        sem = random.choice(avail_sems)
        rows.append([code, name, str(credits), grade, sem])

        # Add retakes for struggling/retake_heavy/probation profiles
        if profile in ("retake_heavy", "probation", "struggling") and grade in ("F", "D", "I"):
            if random.random() < 0.6:
                sem_idx = SEMESTERS.index(sem)
                later = [s for s in SEMESTERS if SEMESTERS.index(s) > sem_idx]
                if later:
                    retry_grade = random.choices(
                        ["C", "C+", "B", "B-", "D+", "D", "F"],
                        weights=[20, 15, 10, 10, 15, 15, 15], k=1)[0]
                    rows.append([code, name, str(credits), retry_grade, random.choice(later)])

    # GED choice groups (3 groups)
    c1 = random.choice(list(CSE_GED_CHOICE_1.keys()))
    if random.random() < course_fraction:
        name, cr = ALL_COURSES[c1]
        rows.append([c1, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    c2 = random.choice(list(CSE_GED_CHOICE_2.keys()))
    if random.random() < course_fraction:
        name, cr = ALL_COURSES[c2]
        rows.append([c2, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    c3 = random.choice(list(CSE_GED_CHOICE_3.keys()))
    if random.random() < course_fraction:
        name, cr = ALL_COURSES[c3]
        rows.append([c3, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # NOTE: ENG102 and MAT116 are waiverable — handled via user input, not in transcript

    # Electives for top/good/nearly_done students
    if profile in ("top_student", "good_student", "nearly_done"):
        elecs = random.sample(list(CSE_ELECTIVES_400.keys()), min(3, len(CSE_ELECTIVES_400)))
        for e in elecs:
            name, cr = ALL_COURSES[e]
            rows.append([e, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

        opens = random.sample(list(OPEN_ELECTIVES.keys()), min(1, len(OPEN_ELECTIVES)))
        for o in opens:
            name, cr = ALL_COURSES[o]
            rows.append([o, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    return sort_rows(rows)


def generate_bba_student(profile, student_id, concentration=None):
    """Generate a BBA student transcript based on profile and concentration."""
    rows = []
    if concentration is None:
        concentration = random.choice(BBA_CONC_NAMES)

    all_required = list(BBA_SCHOOL_CORE.keys()) + list(BBA_CORE.keys()) + list(BBA_GED.keys())

    if profile == "top_student":
        course_fraction = 1.0
    elif profile == "good_student":
        course_fraction = random.uniform(0.75, 0.95)
    elif profile == "nearly_done":
        course_fraction = random.uniform(0.90, 0.98)
    elif profile == "mid_stage":
        course_fraction = random.uniform(0.40, 0.60)
    elif profile == "early_stage":
        course_fraction = random.uniform(0.10, 0.30)
    elif profile in ("struggling", "retake_heavy", "probation"):
        course_fraction = random.uniform(0.30, 0.70)
    else:
        course_fraction = random.uniform(0.30, 0.80)

    n_courses = max(3, int(len(all_required) * course_fraction))
    selected = random.sample(all_required, min(n_courses, len(all_required)))

    n_semesters = random.randint(2, min(10, len(SEMESTERS)))
    start = random.randint(0, len(SEMESTERS) - n_semesters)
    avail_sems = SEMESTERS[start:start + n_semesters]

    for code in selected:
        name, credits = ALL_COURSES[code]
        grade = grade_for_profile(profile)
        sem = random.choice(avail_sems)
        rows.append([code, name, str(credits), grade, sem])

        if profile in ("retake_heavy", "probation", "struggling") and grade in ("F", "D", "I"):
            if random.random() < 0.6:
                sem_idx = SEMESTERS.index(sem)
                later = [s for s in SEMESTERS if SEMESTERS.index(s) > sem_idx]
                if later:
                    retry_grade = random.choices(
                        ["C", "C+", "B", "D+", "D", "F"],
                        weights=[20, 15, 15, 15, 15, 20], k=1)[0]
                    rows.append([code, name, str(credits), retry_grade, random.choice(later)])

    # GED Choice: Language (BEN205/ENG115/CHN101 — pick 1)
    lang = random.choice(list(BBA_GED_CHOICE_LANG.keys()))
    if random.random() < course_fraction:
        name, cr = ALL_COURSES[lang]
        rows.append([lang, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # GED Choice: History (pick 2)
    his_choices = random.sample(list(BBA_GED_CHOICE_HIS.keys()), 2)
    for h in his_choices:
        if random.random() < course_fraction:
            name, cr = ALL_COURSES[h]
            rows.append([h, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # GED Choice: Political Science (pick 1)
    pol = random.choice(list(BBA_GED_CHOICE_POL.keys()))
    if random.random() < course_fraction:
        name, cr = ALL_COURSES[pol]
        rows.append([pol, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # GED Choice: Social Science (pick 1)
    soc = random.choice(list(BBA_GED_CHOICE_SOC.keys()))
    if random.random() < course_fraction:
        name, cr = ALL_COURSES[soc]
        rows.append([soc, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # GED Choice: Science (pick 3)
    sci_choices = random.sample(list(BBA_GED_CHOICE_SCI.keys()), 3)
    for s in sci_choices:
        if random.random() < course_fraction:
            name, cr = ALL_COURSES[s]
            rows.append([s, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # GED Choice: Lab (pick 1 matching lab)
    # Pick a lab matching one of the science courses taken
    available_labs = [code + "L" for code in sci_choices if code + "L" in ALL_COURSES]
    if available_labs and random.random() < course_fraction:
        lab = random.choice(available_labs)
        name, cr = ALL_COURSES[lab]
        rows.append([lab, name, str(cr), grade_for_profile(profile), random.choice(avail_sems)])

    # NOTE: ENG102 and BUS112 are waiverable — handled via user input, not in transcript

    # ── Concentration courses ──
    conc_data = BBA_CONC_COURSES[concentration]
    conc_req_codes = list(conc_data["required"].keys())
    conc_elec_codes = list(conc_data["elective"].keys())

    # Required concentration courses (based on profile)
    if profile in ("top_student", "nearly_done"):
        n_conc_req = 4  # all required
    elif profile in ("good_student",):
        n_conc_req = random.randint(3, 4)
    elif profile in ("mid_stage",):
        n_conc_req = random.randint(1, 3)
    elif profile in ("early_stage",):
        n_conc_req = random.randint(0, 1)
    else:
        n_conc_req = random.randint(1, 4)

    for code in conc_req_codes[:n_conc_req]:
        name, credits = ALL_COURSES[code]
        grade = grade_for_profile(profile)
        sem = random.choice(avail_sems)
        rows.append([code, name, str(credits), grade, sem])

    # Elective concentration courses (need 2)
    if profile in ("top_student", "nearly_done"):
        n_conc_elec = 2
    elif profile in ("good_student",):
        n_conc_elec = random.randint(1, 2)
    elif profile in ("mid_stage",):
        n_conc_elec = random.randint(0, 1)
    else:
        n_conc_elec = random.randint(0, 2)

    chosen_elecs = random.sample(conc_elec_codes, min(n_conc_elec, len(conc_elec_codes)))
    for code in chosen_elecs:
        name, credits = ALL_COURSES[code]
        grade = grade_for_profile(profile)
        sem = random.choice(avail_sems)
        rows.append([code, name, str(credits), grade, sem])

    # Internship for advanced students
    if profile in ("top_student", "good_student", "nearly_done"):
        rows.append(["BUS498", "Internship", "4", grade_for_profile(profile), avail_sems[-1]])

    return sort_rows(rows), concentration


def generate_dept_change_student(student_id, current_program, previous_program):
    """Generate a student who switched from previous_program to current_program."""
    rows = []
    concentration = None
    
    # Selection of semesters
    n_semesters = random.randint(6, 12)
    start = random.randint(0, len(SEMESTERS) - n_semesters)
    avail_sems = SEMESTERS[start:start + n_semesters]
    
    # Split semesters: roughly first 1/3 in old major, rest in new
    switch_point = max(1, n_semesters // 3)
    old_sems = avail_sems[:switch_point]
    new_sems = avail_sems[switch_point:]
    
    # 1. Courses from OLD major (will become electives)
    if previous_program == "CSE":
        old_pool = list(CSE_MAJOR_CORE.keys())
    else:
        old_pool = list(BBA_SCHOOL_CORE.keys()) + list(BBA_CORE.keys())
    
    n_old = random.randint(6, 10)
    old_selected = random.sample(old_pool, min(n_old, len(old_pool)))
    for code in old_selected:
        name, cr = ALL_COURSES[code]
        # Use "struggling" or "good_student" profiles for old major grades
        grade = grade_for_profile(random.choice(["good_student", "struggling"]))
        rows.append([code, name, str(cr), grade, random.choice(old_sems)])

    # 2. Courses from NEW major (current)
    if current_program == "CSE":
        new_rows = generate_cse_student("mid_stage", student_id)
    else:
        new_rows, concentration = generate_bba_student("mid_stage", student_id)
    
    # Filter out duplicates and force new semesters
    seen = {r[0] for r in rows}
    for r in new_rows:
        if r[0] not in seen:
            r[4] = random.choice(new_sems)
            rows.append(r)
            seen.add(r[0])
            
    return sort_rows(rows), concentration


def generate_all():
    random.seed(2024)
    output_dir = os.path.join(os.path.dirname(__file__) or ".", "transcripts")
    os.makedirs(output_dir, exist_ok=True)

    # Clean old transcripts
    import glob
    for old_file in glob.glob(os.path.join(output_dir, "*.csv")):
        try:
            os.remove(old_file)
        except PermissionError:
            pass # Skip locked files

    # Profile distribution across 2000 students
    profile_weights = {
        "top_student": 200,
        "good_student": 350,
        "struggling": 200,
        "early_stage": 150,
        "mid_stage": 200,
        "nearly_done": 250,
        "retake_heavy": 150,
        "transfer_student": 100,
        "withdrawn_heavy": 100,
        "probation": 200,
        "dept_change": 100,
    }

    students = []
    for profile, count in profile_weights.items():
        students.extend([profile] * count)
    random.shuffle(students)

    # Stats tracking
    stats = {
        "total": 0, "cse": 0, "bba": 0,
        "eligible_count": 0,
        "probation_count": 0,
        "profile_counts": {p: 0 for p in PROFILES + ["dept_change"]},
        "total_rows": 0,
        "retake_rows": 0,
        "w_rows": 0, "f_rows": 0, "t_rows": 0, "i_rows": 0,
    }

    for i, profile in enumerate(students):
        student_id = i + 1
        program = random.choices(["CSE", "BBA"], weights=[65, 35], k=1)[0]
        concentration = None
        ex_major = None

        if profile == "dept_change":
            ex_major = "BBA" if program == "CSE" else "CSE"
            rows, concentration = generate_dept_change_student(student_id, program, ex_major)
        elif program == "CSE":
            rows = generate_cse_student(profile, student_id)
            stats["cse"] += 1
        else:
            rows, concentration = generate_bba_student(profile, student_id)
            stats["bba"] += 1

        if profile == "dept_change":
            if program == "CSE": stats["cse"] += 1
            else: stats["bba"] += 1

        stats["profile_counts"][profile] += 1
        stats["total"] += 1

        # Count stats
        course_attempts = {}
        for row in rows:
            code, name, cr, grade, sem = row
            stats["total_rows"] += 1
            if grade == "W": stats["w_rows"] += 1
            if grade == "F": stats["f_rows"] += 1
            if grade == "T": stats["t_rows"] += 1
            if grade == "I": stats["i_rows"] += 1
            course_attempts.setdefault(code, []).append(grade)

        for code, attempts in course_attempts.items():
            if len(attempts) > 1:
                stats["retake_rows"] += len(attempts)

        # Write CSV — encode concentration and department change in filenames
        parts = [f"student_{student_id:04d}", program]
        if concentration:
            parts.append(concentration)
        if ex_major:
            parts.append(f"ex_{ex_major}")
        parts.append(profile)
        
        filename = "_".join(parts) + ".csv"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["course_code", "course_name", "credits", "grade", "semester"])
            for row in rows:
                writer.writerow(row)

    return stats, output_dir


def print_summary(stats, output_dir):
    print("=" * 60)
    print("  NSU 2000 UNIQUE TRANSCRIPT GENERATOR - SUMMARY")
    print("=" * 60)
    print(f"  Output directory     : {output_dir}")
    print(f"  Total transcripts    : {stats['total']}")
    print(f"  CSE students         : {stats['cse']}")
    print(f"  BBA students         : {stats['bba']}")
    print(f"  Total course rows    : {stats['total_rows']}")
    print(f"  Retake rows          : {stats['retake_rows']}")
    print(f"  W (Withdrawn) rows   : {stats['w_rows']}")
    print(f"  F (Failed) rows      : {stats['f_rows']}")
    print(f"  T (Transfer) rows    : {stats['t_rows']}")
    print(f"  I (Incomplete) rows  : {stats['i_rows']}")
    print()
    print("  Profile Distribution:")
    for profile, count in stats["profile_counts"].items():
        bar = "#" * (count // 10)
        print(f"    {profile:20s}: {count:4d}  {bar}")
    print("=" * 60)


if __name__ == "__main__":
    stats, output_dir = generate_all()
    print_summary(stats, output_dir)
