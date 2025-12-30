from functions.get_file_content import get_file_content

print(get_file_content("calculator", "lorem.txt"))
print('Result for Test 1:')
print(get_file_content("calculator", "main.py"))
print('Result for Test 2:')
print(get_file_content("calculator", "pkg/calculator.py"))
print('Result for Test 3:')
print(get_file_content("calculator", "/bin/cat"))
print('Result for Test 4:')
print(get_file_content("calculator", "pkg/does_not_exist.py"))
