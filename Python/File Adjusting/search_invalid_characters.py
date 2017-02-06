line_no = 0
with open("Full Text.txt", "r") as file:
    for line in file:
        line_no += 1
        for ch in set(line):
            if not ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.?!,\n' ":
                print (str(line_no) + ch)