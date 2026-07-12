"""
test_refactor_demo.py
----------------------
Demonstrates the "Refactor and Evaluate" phase of the project: the FIRST
draft grammar written for this project had two textbook CFG problems,
reproduced and fixed here.

PROBLEM 1: Left recursion
    Draft rule:   NP -> NP PP | N
    A top-down parser (e.g. NLTK's RecursiveDescentParser) never
    terminates on NP -> NP PP because it keeps expanding the leftmost NP
    forever. Demonstrated below with a recursion-depth guard standing in
    for the real infinite loop / RecursionError this causes.

PROBLEM 2: Structural ambiguity
    Draft rule:   NP -> DET N PP | DET N | N
                  PP -> PREP NP
    A phrase like "the results for the unit in the department" allows the
    trailing PP to attach at more than one NP level, producing multiple
    valid parse trees for one sentence - undesirable for a classifier that
    needs exactly one interpretation per query.

FIX applied in grammar/cfg_grammar.py:
    - NP -> DET N | DET ADJ N | N | N PP   (right-recursive via PP -> PREP NP,
      no NP on the left of any production -> no left recursion)
    - Category classification decoupled from parse-tree shape entirely
      (see grammar/parser.py) so residual PP-attachment ambiguity in the
      formal grammar never affects the deployed classifier's output.

Run: python -m tests.test_refactor_demo
"""
import sys
from nltk import CFG, RecursiveDescentParser, ChartParser
from grammar.cfg_grammar import GRAMMAR, CANONICAL_TEMPLATES


LEFT_RECURSIVE_GRAMMAR = CFG.fromstring("""
    NP -> NP PP | N
    PP -> PREP NP
    N -> 'results' | 'unit' | 'department'
    PREP -> 'for' | 'in'
""")

REFACTORED_GRAMMAR = CFG.fromstring("""
    NP -> N PP | N
    PP -> PREP NP
    N -> 'results' | 'unit' | 'department'
    PREP -> 'for' | 'in'
""")

AMBIGUOUS_SENTENCE = ["results", "for", "unit", "in", "department"]


def demo_left_recursion():
    print("### Left-recursion demonstration ###")
    print("Draft rule under test: NP -> NP PP | N\n")
    parser = RecursiveDescentParser(LEFT_RECURSIVE_GRAMMAR)
    sys.setrecursionlimit(200)
    try:
        list(parser.parse(AMBIGUOUS_SENTENCE))
        print("Unexpectedly completed - left recursion did not trigger.")
    except RecursionError:
        print("RESULT: RecursionError - confirms NP -> NP PP causes infinite "
              "left-recursive expansion under top-down parsing, as expected.\n")

    print("Refactored rule: NP -> N PP | N  (recursion moved into PP, i.e. "
          "right recursion)")
    parser2 = RecursiveDescentParser(REFACTORED_GRAMMAR)
    trees = list(parser2.parse(AMBIGUOUS_SENTENCE))
    print(f"RESULT: parser terminates normally, {len(trees)} parse tree(s) found.\n")


def demo_ambiguity_reduction():
    print("### Ambiguity check on the FINAL grammar (grammar/cfg_grammar.py) ###")
    parser = ChartParser(GRAMMAR)
    total_trees = 0
    for cat, sent in CANONICAL_TEMPLATES.items():
        trees = list(parser.parse(sent.split()))
        total_trees += len(trees)
        flag = "OK (unambiguous)" if len(trees) == 1 else f"WARNING ({len(trees)} trees)"
        print(f"  {cat:25s} {flag}")
    print(f"\nTotal canonical templates: {len(CANONICAL_TEMPLATES)}, "
          f"total parse trees produced: {total_trees} "
          f"({'all unambiguous' if total_trees == len(CANONICAL_TEMPLATES) else 'some ambiguity remains'})")


if __name__ == "__main__":
    demo_left_recursion()
    print()
    demo_ambiguity_reduction()
