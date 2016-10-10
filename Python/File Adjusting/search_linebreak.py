with open("Full Text.txt", "r") as text:
    line_count = 0
    errCount = 0
    for line in text:
        line_count += 1
        index = 0
        for char in line:   
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
