"""Allow ``python -m verbalizer`` to launch the CLI demo."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
