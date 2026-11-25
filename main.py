#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry line for 'One Line, One Chill' to /output/entry.txt.

The competition asks for one single sentence of horror, under 200
characters, that frightens a reader in one breath. The gate checks
that /output/entry.txt is UTF-8 text of 1 to 200 characters and not
only white space.

The output path defaults to /output/entry.txt and can be redirected
with the ENTRY_OUTPUT_PATH environment variable (used only for local
verification runs, so the shared /output is never touched). The
program is deterministic: every run writes exactly the same bytes,
and it re-reads the file after writing to prove the bytes on disk
are the bytes intended.
"""

import os

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
OUTPUT_ENV_VAR = "ENTRY_OUTPUT_PATH"
MAX_CHARS = 200

# The line, revised after the first run. The draft reported two
# heartbeats on a monitor in plain summary; the final version moves
# the image up front -- a second heartbeat curled beneath the
# narrator's own, slow and patient, as if something were sleeping
# inside the rhythm of his chest -- and saves the blow for the last
# three words. The specific eleven minutes make the death a charted
# fact, not a metaphor, and "the other one didn't" leaves the thing
# unnamed and still beating after he came back. No stock props: no
# mirror, no doll, no basement, no gore.
ENTRY_PARTS = (
    "For three nights a second heartbeat has curled beneath mine "
    "on the monitor, slow and patient, and today the nurse "
    "whispered that last night mine stopped for eleven minutes "
    "\u2014 the other one didn't.",
)


def build_entry() -> str:
    """Assemble the one-sentence horror line and hold it to the gate."""
    text = "".join(ENTRY_PARTS)
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1..{MAX_CHARS} characters, got {len(text)}"
    )
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert text.strip(), "entry must not be only white space"
    assert text.count(".") == 1 and text.endswith("."), (
        "entry must be a single sentence"
    )
    return text


def write_entry(text: str, output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(output_path, "rb") as f:
        on_disk = f.read()
    assert on_disk == text.encode("utf-8"), "bytes on disk differ from entry"


def main() -> None:
    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)
    write_entry(build_entry(), output_path)


if __name__ == "__main__":
    main()
