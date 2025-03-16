testArray = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
insertArray = ["Hello World"]

idx = 11
newArray = testArray[0:idx] + insertArray + testArray[idx:]
print(newArray)