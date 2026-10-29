from functions.run_python_file import run_python_file

def test():
    test_cases = [
        ["calculator", "main.py"],
        ["calculator", "main.py", ["3 + 5"]],
        ["calculator", "tests.py"],
        ["calculator", "../main.py"],
        ["calculator", "nonexistent.py"],
        ["calculator", "lorem.txt"]

    ]

    for case in test_cases:
        if len(case) == 3:
            print(run_python_file(case[0], case[1], case[2]))
        else:
            print(run_python_file(case[0], case[1]))


if __name__ == "__main__":
    test()