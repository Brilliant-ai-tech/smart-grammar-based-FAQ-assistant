"""
response_bank.py
-----------------
Simulated Dean's/COD's office responses. One templated, professionally
worded response per FAQ category, as validated by the student project team
(see report Section 8, "Validation of AI-Generated Responses").

Templates use {unit_name} / {unit_code} slots filled from ParsedQuery.slots
when available, and fall back to generic phrasing otherwise.
"""

RESPONSE_TEMPLATES = {
    "EXAM_RESULTS": (
        "Thank you for reaching out to the {office}. Results for {unit_ref} are processed by the "
        "examinations office after moderation and are typically released on the student portal within "
        "two weeks of the exam date. If it has been longer than that, kindly visit the {office} with "
        "your student ID for a manual verification."
    ),
    "MISSING_MARKS": (
        "We note your concern about a missing mark for {unit_ref}. Please submit a written missing-marks "
        "report to the {office}, attaching your CAT/assignment submission proof, so the concerned lecturer "
        "can verify and update the record within 5 working days."
    ),
    "SUPPLEMENTARY_RETAKE": (
        "Supplementary and retake exams for {unit_ref} are scheduled after the main results release. "
        "You will need to register for the supplementary/retake through the exams office and pay the "
        "applicable fee before the set deadline. The {office} will notify you once the timetable is out."
    ),
    "ATTACHMENT_INTERNSHIP": (
        "For industrial attachment/internship matters, please collect your attachment introduction letter "
        "and evaluation forms from the {office}. Attachment normally runs for a minimum of 8 weeks; ensure "
        "your placement is confirmed and communicated to the department before you begin."
    ),
    "UNIT_REGISTRATION": (
        "Unit registration (including add/drop) for {unit_ref} can be done on the student portal within "
        "the official registration window. If the window has closed, kindly bring a signed request to the "
        "{office} for a late-registration approval."
    ),
    "ELECTIVE_CHANGE": (
        "Elective unit changes are permitted only within the first two weeks of the semester. Please fill "
        "in the elective-change form available at the {office} and have it approved by your class "
        "representative and the {office} before the deadline."
    ),
    "TIMETABLE_SCHEDULE": (
        "The current class/exam timetable is published on the school notice board and the student portal. "
        "The {office} will communicate any changes to class representatives in advance; please check with "
        "your class rep or the notice board for the latest version."
    ),
    "SUPERVISION_PROJECT": (
        "Project/thesis supervisor allocation is done by the {office} at the start of the project unit. "
        "For a supervisor change request, submit a written request stating your reason to the {office}; "
        "requests are reviewed within one week."
    ),
    "DEFERMENT": (
        "To defer your studies or exams, please submit a formal deferment application to the {office}, "
        "attaching supporting documents (e.g. a medical certificate where applicable). Approved deferments "
        "are recorded and you will be re-instated automatically the following semester."
    ),
    "FEE_CLEARANCE": (
        "Exam clearance requires that you meet the minimum fee balance set by finance for that semester. "
        "Kindly check your fee statement on the student portal; if you believe this is an error, visit the "
        "finance office with your receipts and copy the {office}."
    ),
    "COURSE_TRANSFER": (
        "Course/unit transfer requests are reviewed on a case-by-case basis by the {office} together with "
        "the Dean's office. Please submit a written application with your current transcript for review; "
        "processing typically takes 2-3 weeks."
    ),
    "RECOMMENDATION_LETTER": (
        "Recommendation/reference letters are issued by the {office} for students in good academic "
        "standing. Please submit a request with the purpose, deadline, and a copy of your transcript at "
        "least one week before you need the letter."
    ),
    "LAB_SOFTWARE_ISSUE": (
        "Thank you for reporting this. Lab and software access issues are handled by the department's lab "
        "technician. Please log the issue at the {office} (or with the lab technician directly) with the "
        "lab number/machine ID so it can be resolved promptly."
    ),
    "UNCLASSIFIED": (
        "Thank you for your message. We could not automatically match this to a known category. Your query "
        "has been forwarded to the {office} for a personalised response; you should hear back within 2 "
        "working days."
    ),
}


def generate_response(parsed_query):
    """Build a simulated office response for a ParsedQuery object."""
    unit_ref = parsed_query.slots.get("unit_name") or parsed_query.slots.get("unit_code") or "the unit in question"
    template = RESPONSE_TEMPLATES.get(parsed_query.category, RESPONSE_TEMPLATES["UNCLASSIFIED"])
    return template.format(office="COD/Dean's office", unit_ref=unit_ref)
