#!/usr/bin/env python3
"""homework-alibi: write the dog's one-line homework excuse to /output/entry.txt.

One line, at most 200 characters: the excuse a dog gives after being
caught eating the homework. The line is built from two clauses, one per
beat of the joke, and every clause is checked on its own before anything
is written. Standard library only, no network. Deterministic: the same
bytes on every run.
"""

import os
import sys

# The excuse, beat by beat. The setup quotes the worksheet's own
# instruction; the punch obeys it literally, in the dog's own voice.
SETUP_CLAUSE = 'The worksheet said "show your working",'
PUNCH_CLAUSE = "so I showed it my teeth."

LINE = SETUP_CLAUSE + " " + PUNCH_CLAUSE

# Gate limits from the bounty: one line, 1 to 200 characters.
MIN_CHARS = 1
MAX_CHARS = 200

# Fingerprint of the chosen line, so a typo in either clause fails
# loudly instead of shipping a different joke.
EXPECTED_CHARS = 64
EXPECTED_WORDS = 12
EXPECTED_CLAUSES = 2
EXPECTED_SENTENCES = 1
EXPECTED_BYTES = 64
# Each clause must carry its own load: the setup names the worksheet
# and its instruction, the punch names the dog's literal answer.
SETUP_KEYWORDS = ("worksheet", "show your working")
PUNCH_KEYWORDS = ("showed", "teeth")

OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print(f"homework-alibi: error: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_clause(clause, keywords, label, capital_start=True):
    """Check one clause: non-empty, starts capitalised (unless it
    continues the sentence), ends in a stop, and carries every keyword
    the joke needs."""
    if not clause:
        fail(f"{label} clause is empty")
    if clause != clause.strip():
        fail(f"{label} clause has leading or trailing space")
    if capital_start and not clause[0].isupper():
        fail(f"{label} clause must start with a capital letter")
    if not capital_start and not clause[0].islower():
        fail(f"{label} clause must continue in lower case")
    if clause[-1] not in ".!,":
        fail(f"{label} clause must end with a full stop or a comma")
    for keyword in keywords:
        if keyword not in clause:
            fail(f"{label} clause is missing {keyword!r}")


def check_line(line):
    """Check the whole line against the bounty's gate and the fingerprint."""
    if "\n" in line or "\r" in line:
        fail("line must be a single line")
    if "  " in line:
        fail("line must not contain double spaces")
    if line != line.strip():
        fail("line has leading or trailing space")
    if len(line) < MIN_CHARS or len(line) > MAX_CHARS:
        fail(f"line is {len(line)} characters, must be {MIN_CHARS}-{MAX_CHARS}")
    if not line.isascii():
        fail("line must be plain ASCII")
    if line.count("?") or line.count("!"):
        fail("line must not ask or shout")
    words = line.split(" ")
    if len(words) != EXPECTED_WORDS:
        fail(f"line has {len(words)} words, expected {EXPECTED_WORDS}")
    if len(line) != EXPECTED_CHARS:
        fail(f"line is {len(line)} characters, expected {EXPECTED_CHARS}")
    if line.encode("utf-8") and len(line.encode("utf-8")) != EXPECTED_BYTES:
        fail(f"line is {len(line.encode('utf-8'))} bytes, expected {EXPECTED_BYTES}")
    sentences = [part for part in line.split(".") if part]
    if len(sentences) != EXPECTED_SENTENCES:
        fail(f"line has {len(sentences)} sentences, expected {EXPECTED_SENTENCES}")
    clauses = [part for part in line.split(",") if part]
    if len(clauses) != EXPECTED_CLAUSES:
        fail(f"line has {len(clauses)} clauses, expected {EXPECTED_CLAUSES}")
    return words


def output_path():
    """Resolve the output directory: $MAKEFUN_OUTPUT_DIR when set,
    otherwise the bounty's /output directory."""
    directory = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_DIR)
    return os.path.join(directory, OUTPUT_NAME)


def write_entry(path):
    """Write the line plus a trailing newline, then read it back and
    refuse to finish unless the bytes match the line exactly."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    data = (LINE + "\n").encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("read-back mismatch: output does not match the line")
    return len(data)


def main(argv):
    """Validate the line, then write it or report on it."""
    check_clause(SETUP_CLAUSE, SETUP_KEYWORDS, "setup")
    check_clause(PUNCH_CLAUSE, PUNCH_KEYWORDS, "punch", capital_start=False)
    if LINE != SETUP_CLAUSE + " " + PUNCH_CLAUSE:
        fail("line is not the setup plus the punch")
    words = check_line(LINE)
    if "--check" in argv:
        print(f"ok: {len(LINE)} chars, {len(words)} words, "
              f"{len(LINE.encode('utf-8'))} bytes")
        return 0
    if "--print" in argv:
        print(LINE)
        return 0
    path = output_path()
    size = write_entry(path)
    print(f"wrote {size} bytes to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
