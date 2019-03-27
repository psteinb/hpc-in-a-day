import os
import sys
import glob
import re

def load_text():
    """ searchs for the path seen by python (aka sys.path) which contains os.py and reads all .py files in this directory into a large string """

    path_of_ospy = ""
    text = []

    for d in sys.path:
        if os.path.isdir(d) and os.path.exists(d+"/os.py"):
            path_of_ospy = d
            break

    if not path_of_ospy or not os.path.exists(path_of_ospy):
        print("no modules found in "+sys.path)
        return text

    std_files = glob.glob(path_of_ospy+"/*.py")

    for fn in std_files:
        fnf = open(fn,"r")
        text.append("".join(fnf.readlines()))
        fnf.close()

    return "\n".join(text)

def word_count(text):
    """ counts the number of words in the string given by <text> """

    word_pattern = r'\b[^\W\d_]+\b'
    result = re.split(word_pattern,text)
    return len(result)


@profile
def main():

    text = load_text()
    nchars = len(text)
    nwords = word_count(text)
    print("%i characters and %i words found in standard python lib" % (nchars, nwords))

    if len(text):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
