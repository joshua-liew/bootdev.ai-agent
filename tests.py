from functions.get_files_info import get_files_info

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
        ]
    )
]


def test(func, args, exp, unexp):
    print('-----------------------')
    print(f'Input functions: {func.__name__}')
    failed = False
    for case in test_cases:
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
                print(f"Fail: could not find '{keyword}' in output")

    passed = not failed
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


if __name__ == "__main__":
    test_cases = run_cases
    main()
