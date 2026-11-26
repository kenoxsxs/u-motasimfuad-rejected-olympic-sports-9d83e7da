"""Rejected Olympic Sports -- one-liner entry.

The Games said no to synchronized sighing. This program disagrees,
politely, by filing the event anyway so the record shows it existed.
"""

import hashlib
import io
import os
from pathlib import Path

REJECTED_SPORT = (
    "Synchronized sighing: two athletes sigh in perfect unison "
    "while a third judge sighs louder to show them how it's done."
)

MAX_LEN = 200


def olympics(line):
    """Refuse any line the Games would refuse for the wrong reasons."""
    if not line or not line.strip():
        raise ValueError("the arena needs a sport, not an empty page")
    if line != line.strip():
        raise ValueError("the line must not lean on leading or trailing space")
    if "\n" in line or "\r" in line:
        raise ValueError("one line only: the broadcast has no second breath")
    if not 1 <= len(line) <= MAX_LEN:
        raise ValueError("the line must fit in 200 characters, no more")
    return line


def arena_dir():
    """Where the rejected sport finally gets its hearing."""
    folder = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def reject_sport(folder, line):
    """File the rejected sport with the committee of one."""
    target = folder / "entry.txt"
    with io.open(
        target,
        "w",
        encoding="utf-8",
        newline="",
        errors="strict",
        buffering=1,
        closefd=True,
        opener=os.open,
    ) as handle:
        handle.write(line)
    return target


def check_sport(target, line):
    """Read the filed sport back and make sure nothing was lost."""
    with io.open(target, "rb") as handle:
        payload = handle.read()
    if payload.decode("utf-8") != line:
        raise ValueError("the filed sport does not match the announced one")
    if payload != payload.strip():
        raise ValueError("the filed sport picked up stray whitespace")
    return payload


def announce(target, payload):
    """Put the verdict on the record for the committee to read."""
    digest = hashlib.sha256(payload).hexdigest()
    print("rejected:", target, "|", len(payload), "bytes | sha256", digest)


def main():
    line = olympics(REJECTED_SPORT)
    folder = arena_dir()
    target = reject_sport(folder, line)
    payload = check_sport(target, line)
    announce(target, payload)


if __name__ == "__main__":
    main()
