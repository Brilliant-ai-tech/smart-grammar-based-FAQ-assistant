"""
lexicon.py
----------
Single source of truth for the vocabulary used by the Context-Free Grammar
(cfg_grammar.py) AND by the production classifier (parser.py).

Each entry in CATEGORY_LEXICON corresponds to one lexical non-terminal in the
CFG (e.g. CAT_EXAM, CAT_ATTACH, ...). The terminal words listed under a
category are exactly the words the grammar rewrites that non-terminal into.
Keeping the vocabulary in one place guarantees that the formal grammar and
the deployed parser can never drift apart, and that a category label is
always traceable back to a specific grammar production (the requirement of
a *grammar-based* parser, not a plain keyword matcher).
"""

# FAQ category  -> (grammar non-terminal, head-noun/keyword terminals, human label)
CATEGORY_LEXICON = {
    "EXAM_RESULTS": {
        "nonterminal": "CAT_EXAM",
        "keywords": ["result", "results", "mark", "marks", "grade", "grades", "cat", "score", "released", "release", "portal"],
        "label": "Exam Results & CAT Marks",
        "priority": 1,
    },
    "MISSING_MARKS": {
        "nonterminal": "CAT_MISSING",
        "keywords": ["missing", "not reflecting", "reflect", "unrecorded", "lost mark"],
        "label": "Missing / Unrecorded Marks",
        "priority": 2,
    },
    "SUPPLEMENTARY_RETAKE": {
        "nonterminal": "CAT_SUPP",
        "keywords": ["supplementary", "retake", "resit", "supp"],
        "label": "Supplementary & Retake Exams",
        "priority": 2,
    },
    "ATTACHMENT_INTERNSHIP": {
        "nonterminal": "CAT_ATTACH",
        "keywords": ["attachment", "internship", "industrial", "placement"],
        "label": "Industrial Attachment / Internship",
        "priority": 1,
    },
    "UNIT_REGISTRATION": {
        "nonterminal": "CAT_REG",
        "keywords": ["register", "registration", "unit", "units", "add", "drop", "enroll"],
        "label": "Unit Registration (Add/Drop)",
        "priority": 1,
    },
    "ELECTIVE_CHANGE": {
        "nonterminal": "CAT_ELECTIVE",
        "keywords": ["elective", "switch", "change my elective"],
        "label": "Elective Unit Change",
        "priority": 2,
    },
    "TIMETABLE_SCHEDULE": {
        "nonterminal": "CAT_TIMETABLE",
        "keywords": ["timetable", "schedule", "lecture", "classes", "class"],
        "label": "Class / Exam Timetable",
        "priority": 2,
    },
    "SUPERVISION_PROJECT": {
        "nonterminal": "CAT_SUPERVISION",
        "keywords": ["supervisor", "project", "thesis", "capstone", "proposal", "defense"],
        "label": "Project / Thesis Supervision",
        "priority": 1,
    },
    "DEFERMENT": {
        "nonterminal": "CAT_DEFER",
        "keywords": ["defer", "deferment", "deferring", "postpone"],
        "label": "Deferment of Studies/Exams",
        "priority": 2,
    },
    "FEE_CLEARANCE": {
        "nonterminal": "CAT_FEE",
        "keywords": ["fee", "fees", "balance", "clearance", "cleared", "clear me"],
        "label": "Fee Balance & Exam Clearance",
        "priority": 1,
    },
    "COURSE_TRANSFER": {
        "nonterminal": "CAT_TRANSFER",
        "keywords": ["transfer", "transferring", "parallel programme", "parallel program"],
        "label": "Course / Unit Transfer",
        "priority": 2,
    },
    "RECOMMENDATION_LETTER": {
        "nonterminal": "CAT_RECOMMEND",
        "keywords": ["recommendation", "reference letter", "reference", "letter"],
        "label": "Recommendation / Reference Letter",
        "priority": 1,
    },
    "LAB_SOFTWARE_ISSUE": {
        "nonterminal": "CAT_LAB",
        "keywords": ["lab", "laptop", "software", "license", "licensed", "computer lab", "machines"],
        "label": "Lab & Software Access Issues",
        "priority": 1,
    },
}

# Politeness / greeting closed-class vocabulary shared by the grammar
GREETINGS = ["good morning", "good afternoon", "good evening", "hello", "hi"]
POLITE_MARKERS = ["please", "thank you", "thanks", "kindly"]
OPENERS = [
    "i would like to know", "i want to know", "i would like to",
    "i want to", "could you", "can you", "please advise",
    "when will", "when is", "why", "how do i", "how can i",
]
