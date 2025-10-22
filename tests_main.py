import os
import subprocess

"""
each test case should be formatted accordingly:
(
    ([<str:PROMPT>,...*args]),
    (<str:EXPECTED_OUTPUT>,...),
    (<str:UNEXPECTED_OUTPUT>,...),
)
"""
test_cases = [
    (
        (["read the contents of main.py",]),
        ("get_file_content({'file_path': 'main.py'})",),
        (),
    ),
    (
        (["write 'hello' to main.txt",]),
        ("write_file({'file_path': 'main.txt', 'content': 'hello'})",),
        (),
    ),
    (
        (["run main.py",]),
        ("run_python_file({'file_path': 'main.py'})",),
        (),

    ),
    (
        (["list the contents of the pkg directory",]),
        ("get_files_info({'directory': 'pkg'})",),
        (),
    ),
]

test_cases = [
    (
        (["run tests.py", "--verbose",]),
        ("Ran 9 tests",),
        ("Error:",),
    ),
    (
        (["get the contents of lorem.txt", "--verbose",]),
        ("wait, this", "lorem ipsum",),
        ("Error:",),
    ),
    (
        (["create a new README.md file with the contents '# calculator'", "--verbose",]),
        ("Successfully wrote to",),
        ("Error:",),
    ),
    (
        (["what files are in the root?", "--verbose",]),
        ("lorem.txt", "README.md",),
        ("Error:",),
    ),
    (
        (["what files are in the root?",]),
        ("Calling function", "get_files_info"),
        ("Error:",),
    ),
    (
        (["how does the calculator render results to the console?",]),
        ("Calling function:", "Final response:"),
        ("Error:",),
    ),
]


def test(test_case):
    FILE = "main.py"
    FILEPATH = os.path.abspath(FILE)
    CAPTURE_OUTPUT = True
    CWD = os.path.dirname(FILEPATH)
    TIMEOUT = 30
    ARGS = ["uv", "run", FILE]

    failed = False
    args = test_case[0]
    try:
        completed_ps = subprocess.run(
            args=(ARGS+args),
            capture_output=CAPTURE_OUTPUT,
            cwd=CWD,
            timeout=TIMEOUT,
        )
    except Exception as err:
        result = f'Error: {err=}'
    else:
        result = (
            f'STDOUT: {completed_ps.stdout}\nSTDERR: {completed_ps.stderr}'
        )
    if completed_ps.returncode != 0:
        result += f'\nProcess exited with code {completed_ps.returncode}'
    if not completed_ps.stdout:
        result += f'\nNo output produced'

    exp = test_case[1]
    unexp = test_case[2]
    print("-----------------------")
    print("Arguments passed to main.py")
    for arg in args:
        print(f"> {arg}")
    print("Expecting stdout to contain:")
    for k in exp:
        print(f"* {k}")
    print("Stdout should NOT contain:")
    for k in unexp:
        print(f"** {k}")

    print(f'Actual:\n{result}\n')
    for k in exp:
        if k not in result:
            failed = True
            print(f"Fail: could not find '{k}' in output")
    for k in unexp:
        if k in result:
            failed = True
            print(f"Fail: found unexpected '{k}' in output")

    passed = not failed
    if passed:
        print("---| PASS |---")
    else:
        print("---| FAIL |---")
    return passed


def main():
    passed = 0
    failed = 0
    for test_case in test_cases:
        correct = test(test_case)
        if correct:
            passed += 1
        else:
            failed += 1
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    print(f"{passed} passed, {failed} failed")


main()
