import nltk

def print_chunks(chunks):
    out = ""
    for chunk in chunks:
        if type(chunk).__name__=="Tree":
            out += str(chunk) + "\n"
            #print(chunk.__getitem__(0))
    if not out == "":
        print (out)

def adjust_ne(chunks, additional_nes):
    for counter, chunk in enumerate(chunks):
        if type(chunk).__name__=="Tree":
            pass
        elif chunk[0] in additional_nes: #tuples
            chunks[counter] = nltk.Tree('NE', [chunk])
    return chunks

class Rel:
    paragraph_no = 0
    left = None
    rel = None
    right = None

    def __init__(self, left, rel, right, paragraph_no):
        self.paragraph_no = paragraph_no
        self.left = left
        self.rel = rel
        self.right = right
