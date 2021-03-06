# regular_expressions.py
"""Volume 3: Regular Expressions.
Matthew Schaelling
Math 403
September 14, 2017
"""


import re

# Problem 1
def prob1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile("python")



# Problem 2
def prob2():
    """Compile and return a regular expression pattern object that matches
    the string "^{@}(?)[%]{.}(*)[_]{&}$".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"\^\{@\}\(\?\)\[\%\]\{\.\}\(\*\)\[\_\]\{\&\}\$")


# Problem 3
def prob3():
    """Compile and return a regular expression pattern object that matches
    the following strings (and no other strings).

        Book store          Mattress store          Grocery store
        Book supplier       Mattress supplier       Grocery supplier

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"^(Book|Mattress|Grocery) (store|supplier)$")

# Problem 4
def prob4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"^[a-zA-Z_]\w*$")


# Problem 5
def prob5(code):
    """Use regular expressions to place colons in the appropriate spots of the
    input string, representing Python code. You may assume that every possible
    colon is missing in the input string.

    Parameters:
        code (str): a string of Python code without any colons.

    Returns:
        (str): code, but with the colons inserted in the right places.
    """
    findcolons = re.compile(r"((?:if|elif|else|for|while|try|except|finally|with|def|class)[^\n:]*)\n", re.MULTILINE)
    return findcolons.sub(r"\1:\n", code)


# Problem 6
def prob6(filename="fake_contacts.txt"):
    """Use regular expressions to parse the data in the given file and format
    it uniformly, writing birthdays as mm/dd/yyyy and phone numbers as
    (xxx)xxx-xxxx. Construct a dictionary where the key is the name of an
    individual and the value is another dictionary containing their
    information. Each of these inner dictionaries should have the keys
    "birthday", "email", and "phone". In the case of missing data, map the key
    to None.

    Returns:
        (dict): a dictionary mapping names to a dictionary of personal info.
    """
    name = re.compile(r"^[a-zA-Z]*")
    with open(filename, 'r') as fh:
        line = fh.readline()
    
    name = re.compile(r"([ a-zA-Z]\.* )")
    birthday = re.compile(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4]")
    email = re.compile(r"[\w\.]+@[\w\.]+")
    phone = re.compile(r"1?-?\(?([0-9]{3})\)?-?([0-9]{3})-([0-9]{4})")


if __name__=="__main__":
    test = """\nk, i, p = 999, 1, 0\nwhile k > i\n\ti *= 2\n\tp += 1\n\tif k != 999\n\t\tprint("k should not have changed")\n\telse\n\t\tpass\nprint(p)\n"""
    print(prob5(test))
