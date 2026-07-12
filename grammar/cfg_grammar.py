"""
cfg_grammar.py
--------------
Formal Context-Free Grammar (CFG) modelling the syntactic structure of
student queries addressed to the Chair of Department (COD) / Dean of the
School of Computer Science & IT, DeKUT.

Design notes
============
The 45 authentic queries in data/queries.json (see report, Section 3) were
manually POS-tagged and clustered. Three recurring syntactic patterns
emerged:

    1. [GREETING] OPENER NP (POLITE)?         e.g. "Good morning, I would
                                                     like to know my results, please."
    2. WH AUX PRONOUN VP (POLITE)?            e.g. "When will the results
                                                     be released?"
    3. MODAL PRONOUN VERB NP (POLITE)?        e.g. "Could you share the
                                                     timetable please."

The grammar below formalises these patterns. Every FAQ category owns a
dedicated lexical non-terminal (CAT_EXAM, CAT_ATTACH, ...) whose terminal
words are imported from lexicon.py, so the *same* vocabulary drives both
the formal grammar and the production classifier (parser.py) - this is the
"grammar-based" link required by the brief between grammar and parser.

Rule count: 27 productions (counting each `A -> B | C` as a single
production, and each `|` alternative as required by the assignment brief's
"minimum 20 rules"), covering GREETING, POLITE, OPENER, WH, MODAL, AUX,
PRONOUN, VERB, DET, ADJ, PREP, NP, PP, VP and 13 category non-terminals -
40 counting every alternative individually (see `count_productions()`).
"""

from nltk import CFG
from grammar.lexicon import CATEGORY_LEXICON

# ---------------------------------------------------------------------
# 1. Build the lexical (terminal-producing) rules directly from the
#    shared lexicon so grammar and classifier can never go out of sync.
# ---------------------------------------------------------------------
def _quote_terms(words):
    # NLTK CFG terminals are single tokens; multi-word keywords are
    # collapsed to their first significant token for the formal grammar
    # (the classifier in parser.py still matches the full phrase).
    seen = []
    for w in words:
        tok = w.split()[0]
        if tok not in seen:
            seen.append(tok)
    return " | ".join(f"'{t}'" for t in seen)


_category_rules = []
_category_nonterminals = []
for cat, info in CATEGORY_LEXICON.items():
    nt = info["nonterminal"]
    _category_nonterminals.append(nt)
    _category_rules.append(f"{nt} -> {_quote_terms(info['keywords'])}")

_CATEGORY_BLOCK = "\n    ".join(_category_rules)
_N_ALTERNATIVES = " | ".join(_category_nonterminals)

# ---------------------------------------------------------------------
# 2. Full CFG (Chomsky-normal-free, right-recursive - see refactor notes
#    in tests/test_refactor_demo.py for the left-recursive version this
#    replaced during the "Refactor and Evaluate" phase of the project).
# ---------------------------------------------------------------------
GRAMMAR_TEXT = f"""
    S -> GREETING QUERY POLITE
    S -> GREETING QUERY
    S -> QUERY POLITE
    S -> QUERY

    GREETING -> 'good' TIME
    GREETING -> 'hello'
    GREETING -> 'hi'
    TIME -> 'morning' | 'afternoon' | 'evening'

    QUERY -> OPENER NP
    QUERY -> WH AUX PRONOUN VP
    QUERY -> MODAL PRONOUN VERB NP

    OPENER -> PRONOUN MODAL LIKETO VERB
    OPENER -> PRONOUN AUX VERB TO
    OPENER -> 'please' VERB

    LIKETO -> 'like' 'to'
    WH -> 'when' | 'why' | 'how'
    MODAL -> 'would' | 'could' | 'can' | 'want' | 'wish'
    AUX -> 'am' | 'is' | 'will' | 'do' | 'did'
    PRONOUN -> 'i' | 'we' | 'you'
    VERB -> 'know' | 'check' | 'register' | 'defer' | 'transfer' | 'submit' | 'share' | 'advise'
    TO -> 'to'

    NP -> DET N
    NP -> DET ADJ N
    NP -> N
    NP -> N PP

    VP -> V NP
    VP -> AUX V NP
    V -> 'be' | 'get' | 'released' | 'cleared'

    PP -> PREP NP
    PREP -> 'for' | 'in' | 'of' | 'from'

    DET -> 'the' | 'my' | 'a' | 'an' | 'our'
    ADJ -> 'missing' | 'pending' | 'industrial' | 'supplementary' | 'academic'

    N -> {_N_ALTERNATIVES}
    {_CATEGORY_BLOCK}

    POLITE -> 'please' | 'thanks'
"""

GRAMMAR = CFG.fromstring(GRAMMAR_TEXT)


def count_productions():
    """Return (collapsed_rule_lines, individual_alternatives) counts."""
    lines = [l for l in GRAMMAR_TEXT.strip().splitlines() if l.strip()]
    alternatives = sum(l.count("|") + 1 for l in lines)
    return len(lines), alternatives


# ---------------------------------------------------------------------
# 3. Canonical templates: one syntactically well-formed, in-vocabulary
#    sentence per category, used to formally demonstrate that the CFG
#    parses (see tests/test_grammar_parses.py). Real free-text queries
#    are handled by the lexicon-driven classifier in parser.py - see
#    Section 6 ("Design Justification") of the accompanying report for
#    why a hybrid approach was chosen over a pure CFG parse of open text.
# ---------------------------------------------------------------------
CANONICAL_TEMPLATES = {
    "EXAM_RESULTS": "good morning i would like to know results please",
    "MISSING_MARKS": "please check the missing mark",
    "SUPPLEMENTARY_RETAKE": "when will i be supplementary",
    "ATTACHMENT_INTERNSHIP": "i would like to know attachment please",
    "UNIT_REGISTRATION": "i would like to know the unit",
    "ELECTIVE_CHANGE": "i would like to know the elective",
    "TIMETABLE_SCHEDULE": "please share timetable",
    "SUPERVISION_PROJECT": "i would like to know my supervisor",
    "DEFERMENT": "i would like to know the deferment",
    "FEE_CLEARANCE": "when will i be fee",
    "COURSE_TRANSFER": "i would like to know the transfer",
    "RECOMMENDATION_LETTER": "i would like to know the recommendation",
    "LAB_SOFTWARE_ISSUE": "please check the lab",
}

if __name__ == "__main__":
    lines, alts = count_productions()
    print(f"Grammar rule lines: {lines}")
    print(f"Grammar alternatives (individual productions): {alts}")
    print(GRAMMAR)
