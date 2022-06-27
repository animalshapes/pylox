import sys

from scanner import Scanner

had_error = False


def run_file(path: str) -> None:
    with open(path, "r") as file:
        data = file.read()

    run(data)

    if had_error:
        sys.exit(65)


def run_prompt() -> None:
    for line in sys.stdin:
        run(line)
        had_error = False


def run(source: str) -> None:

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    had_error = True


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()
