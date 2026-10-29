from functions.get_file_content import get_file_content

def test():
    test_cases_text = [
        ["calculator", "lorem.txt"],
    ]

    test_cases = [
        ["calculator", "main.py"],
        ["calculator", "pkg/calculator.py"],
        ["calculator", "/bin/cat"],
        ["calculator", "pkg/does_not_exist.py"],
    ]

    for case in test_cases_text:
        result = get_file_content(case[0], case[1])
        print(f"{case[1]} length: {len(result)}")
        print(f"{case[1]} truncated: {'truncated' in result}\n")

    for case in test_cases:
        result = get_file_content(case[0], case[1])
        print(f"{result}\n")

if __name__ == "__main__":
    test()