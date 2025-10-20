from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

run_cases = [
    (
        get_files_info,
        [
            (
                ("calculator", ".",),
                ("main.py", "tests.py", "pkg",),
                ("Error:",)
            ),
            (
                ("calculator", "pkg",),
                ("calculator.py", "render.py",),
                ("Error:",)
            ),
            (
                ("calculator", "/bin",),
                ("Error:",),
                ()
            ),
            (
                ("calculator", "../",),
                ("Error:",),
                ()
            ),
            (
                ("calculator", "../..",),
                ("Error:",),
                ()
            ),
            (
                ("calculator", "..",),
                ("Error:",),
                ()
            ),
            (
                ("calculator", "/home",),
                ("Error:",),
                ()
            ),
        ]
    ),
]

run_cases += [
    (
        get_file_content,
        [
            (
                ("calculator", "main.py",),
                ("def main()",),
                ()
            ),
            (
                ("calculator", "pkg/calculator.py",),
                ("def _apply_operator(self, operators, values)",),
                ()
            ),
            (
                ("calculator", "/bin/cat",),
                ("Error:",),
                ()
            ),
            (
                ("calculator", "pkg/does_not_exist.py",),
                ("Error:",),
                ()
            ),
        ]
    ),
]

run_cases += [
    (
        write_file,
        [
            (
                ("calculator", "lorem.txt", "wait, this isn't lorem ipsum",),
                ("28 characters written",),
                ()
            ),
            (
                ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet",),
                ("26 characters written",),
                ()
            ),
            (
                ("calculator", "/tmp/temp.txt", "this should not be allowed",),
                ("Error:",),
                ()
            ),
        ]
    ),
]

run_cases += [
    (
        run_python_file,
        [
            (
                ("calculator", "/bin/sh", ["uv" "run"],),
                ("Error: Cannot execute", "as it is outside the permitted working directory",),
                ()
            ),
            (
                ("calculator", "not_found.py", ["uv" "run"],),
                ("Error: File", "not found.",),
                ()
            ),
            (
                (".", "calculator", ["uv" "run"],),
                ("Error: ", "is not a file.",),
                ()
            ),
            (
                (".", "README.md", ["uv" "run"],),
                ("Error: ", "is not a Python file.",),
                ()
            ),
        ]
    ),
]


def test(func, args, exp, unexp):
    print('-----------------------')
    print(f'Input functions: {func.__name__}')
    failed = False

    try:
        result = func(*args)
    except Exception as err:
        result = str(err)

    expected_keywords = exp
    print(f'Expecting stdout to contain:')
    for keyword in expected_keywords:
        print(f"* '{keyword}'")
    unexpected_keywords = unexp
    if len(unexpected_keywords) != 0:
        print(f'Stdout should NOT contain:')
    for keyword in unexpected_keywords:
        print(f"* '{keyword}'")

    print(f'Actual:\n{result}\n')
    for keyword in expected_keywords:
        if keyword not in result:
            failed = True
            print(f"Fail: could not find '{keyword}' in output")
    for keyword in unexpected_keywords:
        if keyword in result:
            failed = True
            print(f"Fail: found unexpected '{keyword}' in output")

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
        func = test_case[0]
        for case in test_case[1]:
            correct = test(func, *case)
            if correct:
                passed += 1
            else:
                failed += 1
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    print(f"{passed} passed, {failed} failed")


test_cases = run_cases
main()
