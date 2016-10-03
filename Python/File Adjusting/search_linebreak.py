with open("Full Text.txt", "r") as text:
    line_count = 0
    errCount = 0
    for line in text:
        line_count += 1
        #if line_count >= 7695: #remove after finishing whole file
        #    break
        index = 0
        for char in line:
            """Big condition to find possibly problematic formatting
                first check that the current char is a '.'
                then check that the line has at least 2 more characters
                then check that the next character is ' '
                then check that the following character is an uppercase letter
                then check that, if there are at least two characters preceeding, that they are not "St" or "Mr"
                then check that, if there are at least three characters preceeding, that they are not "Mrs"
                then check that, if there are at least four characters preceding, that they are not "G. E" or "T. E" or "Mlle"
                then check that, if there are enough characters either side, that it is not the other "." in "G. E." or "T. E."
                if all these conditions are met, print the line number and check if invalid formatting is found"""
                
            if (
            (
                char == "?" and 
                index < len(line) - 1 and 
                line[index+1] == " " and 
                line[index+2] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ) or 
            (   
                char == "."  and 
                index < len(line) - 1 and 
                line[index+1] == " " and 
                line[index+2] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and 
                not
                (   
                    index > 1 and  
                    line[index-2:index] == "St" or 
                    line[index-2:index] == "Mr" or
                    line[index-2:index] == "Ms"
                ) and 
                not 
                (   
                    index > 2 and 
                    line[index-3:index] == "Mrs"
                ) and 
                not 
                (   
                    index > 3 and 
                    (   
                        line[index-4:index] == "Miss" or 
                        line[index-4:index] == "Mlle" or 
                        line[index-4:index] == "ax J" or # Specific condition to ignore the name "Max J. Friedlander
                        (   
                            line[index-4] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and 
                            line[index-3:index-1] == ". " and 
                            line[index-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        )
                    )
                ) and 
                not 
                (   
                    index > 0 and 
                    index < len(line) - 2 and
                    (
                        line[index-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and 
                        line[index+1] == " " and
                        line[index+2] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    )
                )
            )
            ):
                print line_count
                errCount += 1
            index += 1
            
    if errCount == 0:
        print "\n\nNO DISCREPANCIES FOUND\n\n"
    elif errCount == 1:
        print "\n\n1 DISCREPANCY FOUND\n\n"
    else:
        print "\n\n%d DISCREPANCIES FOUND\n\n" % (errCount)
        
        
        (line[index-1:index+3] == "G. E" or line[index-1:index+3] == "T. E")