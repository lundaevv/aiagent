from functions.get_files_info import get_files_info

def test():
    test_cases = [
        ["calculator", "."],
        ["calculator", "pkg"],
        ["calculator", "/bin"],
        ["calculator", "../"],
    ]

    for case in test_cases:
        print(get_files_info(case[0], case[1]))

if __name__ == "__main__":
    test()