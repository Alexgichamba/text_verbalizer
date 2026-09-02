# verbalizer/cli.py

"""
Interactive command-line demo for the text verbalizer.

Three ways to run it:

    verbalize                          # REPL: type text, see it verbalized
    verbalize -l rw "Mfite 2345"       # one-shot
    cat lines.txt | verbalize -l sw    # one line in, one line out

In the REPL, ``:sw`` / ``:rw`` switch language, ``:demo`` runs a sample sweep,
``:show`` prints each normalizer stage separately, ``:digits`` switches how bare
runs of digits are read, and ``:q`` exits.
"""

from __future__ import annotations

import argparse
import sys

from . import KinyarwandaVerbalizer, SwahiliVerbalizer, __version__
from .base import BaseNormalizer

# Language codes accepted on the command line and by the ``:`` commands.
LANGUAGES = {
    "sw": ("Swahili", SwahiliVerbalizer),
    "rw": ("Kinyarwanda", KinyarwandaVerbalizer),
}

# Sample inputs for ``:demo``, chosen to exercise every semiotic class.
DEMOS = {
    "sw": [
        "Nina watoto 3",
        "Nambari yangu ni 0712345678",
        "Bei ni 2345",
        "Idadi ni 150000",
        "KES 1500.50",
        "Tutaonana saa 14:30 tarehe 25/12/2024",
        "Joto ni 36.6",
    ],
    "rw": [
        "Mfite abana 3",
        "Nimero yanjye ni 0793092164",
        "Igiciro ni 2345",
        "Umubare ni 150000",
        "RWF 10000",
        "Tuzahura saa 14:30 tariki 25/12/2024",
        "Ubushyuhe ni 36.6",
    ],
}

BANNER = """\
text_verbalizer {version} -- interactive demo
Language: {language}   (:sw Swahili, :rw Kinyarwanda)
Digit reading: {read_digits}   (:digits auto|always|never)
Type text to verbalize it. :help for commands, :q to quit.\
"""

HELP = """\
Commands:
  :sw           switch to Swahili
  :rw           switch to Kinyarwanda
  :demo         run the built-in sample sweep for the current language
  :show <text>  show each normalizer stage separately
  :digits MODE  how to read a bare run of digits: auto | always | never
                (auto reads a leading-zero token digit by digit)
  :help         this message
  :q / :quit    exit  (Ctrl-D also works)\
"""


def _make(code, read_digits="auto", digit_threshold=None):
    """Instantiate the verbalizer for a language code."""
    return LANGUAGES[code][1](
        read_digits=read_digits, digit_threshold=digit_threshold
    )


def _show_stages(verbalizer, text):
    """Print the output of each normalizer stage in the order ``normalize`` applies them."""
    stages = [
        ("currency", verbalizer.normalize_currency),
        ("dates", verbalizer.normalize_dates),
        ("time", verbalizer.normalize_time),
        ("numbers", verbalizer.normalize_numbers),
    ]
    current = text
    print("  %-9s %s" % ("input", current))
    for name, fn in stages:
        nxt = fn(current)
        marker = " " if nxt == current else "*"
        print("%s %-9s %s" % (marker, name, nxt))
        current = nxt


def _repl(code, read_digits="auto", digit_threshold=None):
    """Run the interactive loop until EOF, :q, or Ctrl-C."""
    try:  # readline gives arrow-key history when it is available
        import readline  # noqa: F401
    except ImportError:
        pass

    verbalizer = _make(code, read_digits, digit_threshold)
    print(
        BANNER.format(
            version=__version__,
            language=LANGUAGES[code][0],
            read_digits=read_digits,
        )
    )

    while True:
        try:
            line = input("\n%s> " % code)
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        text = line.strip()
        if not text:
            continue

        if text.startswith(":"):
            command, _, argument = text[1:].partition(" ")
            command = command.lower()

            if command in ("q", "quit", "exit"):
                return 0
            if command in ("h", "help", "?"):
                print(HELP)
            elif command in LANGUAGES:
                code = command
                verbalizer = _make(code, read_digits, digit_threshold)
                print("Language: %s" % LANGUAGES[code][0])
            elif command == "digits":
                mode = argument.strip().lower()
                if mode in BaseNormalizer.READ_DIGITS_MODES:
                    read_digits = mode
                    verbalizer = _make(code, read_digits, digit_threshold)
                    print("Digit reading: %s" % read_digits)
                else:
                    print(
                        "usage: :digits {%s}"
                        % "|".join(BaseNormalizer.READ_DIGITS_MODES)
                    )
            elif command == "demo":
                for sample in DEMOS[code]:
                    print("  %s\n  -> %s\n" % (sample, verbalizer.normalize(sample)))
            elif command == "show":
                if argument.strip():
                    _show_stages(verbalizer, argument.strip())
                else:
                    print("usage: :show <text>")
            else:
                print("Unknown command %r. :help for the list." % text)
            continue

        print(verbalizer.normalize(text))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="verbalize",
        description="Verbalize numbers, currency, times and dates in African languages.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="text to verbalize; omit to start the interactive REPL",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="sw",
        choices=sorted(LANGUAGES),
        help="language code (default: sw)",
    )
    parser.add_argument(
        "--stages",
        action="store_true",
        help="show each normalizer stage separately instead of just the result",
    )
    parser.add_argument(
        "-d",
        "--digits",
        default="auto",
        choices=BaseNormalizer.READ_DIGITS_MODES,
        help=(
            "how to read a bare run of digits: auto reads a leading-zero "
            "token digit by digit (phone numbers, IDs), always reads every "
            "numeric token that way, never reads them all as cardinals "
            "(default: auto)"
        ),
    )
    parser.add_argument(
        "--digit-threshold",
        type=int,
        default=None,
        metavar="N",
        help=(
            "under --digits auto, also read a token digit by digit once it "
            "has N or more digits (try 7 for text containing phone numbers)"
        ),
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    verbalizer = _make(args.language, args.digits, args.digit_threshold)

    # One-shot: text given on the command line.
    if args.text:
        text = " ".join(args.text)
        if args.stages:
            _show_stages(verbalizer, text)
        else:
            print(verbalizer.normalize(text))
        return 0

    # Piped or redirected input: one line in, one line out.
    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.rstrip("\n")
            if line.strip():
                print(verbalizer.normalize(line))
        return 0

    return _repl(args.language, args.digits, args.digit_threshold)


if __name__ == "__main__":
    sys.exit(main())
