from functions.run_python_file import run_python_file

print("Run Test 1:")
print(run_python_file("calculator", "main.py"))
print("Run Test 2:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("Run Test 3:")
print(run_python_file("calculator", "tests.py"))
print("Run Test 4(expecting error):")
print(run_python_file("calculator", "../main.py"))
print("Run Test 5(expecting error):")
print(run_python_file("calculator", "nonexistent.py"))
print("Run Test 6(expecting error):")
print(run_python_file("calculator", "lorem.txt"))