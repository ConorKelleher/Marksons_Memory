with open("Full Text.txt", "a") as text:
    for i in range(111, 245):
        num_string = "hi"
        if i < 10:
            num_string = "00" + str(i)
        elif i < 100:
            num_string = "0" + str(i)
        else:
            num_string = str(i)
        with open(num_string + ".txt", "r") as curr_file:
            for line in curr_file:
                text.write(line)
            text.write("\n\n")