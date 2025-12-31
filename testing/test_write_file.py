from functions.write_file import write_file

print("Results from Test 1:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("Results from Test 2:")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("Results from Test 3:")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

