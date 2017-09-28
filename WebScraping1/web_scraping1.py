"""Volume 3: Introduction to BeautifulSoup.
Matthew Schaelling
Math 403
September 28, 2017
"""

from bs4 import BeautifulSoup
import re

# Example HTML string from the lab.
pig_html = """
<html><head><title>Three Little Pigs</title></head>
<body>
<p class="title"><b>The Three Little Pigs</b></p>
<p class="story">Once upon a time, there were three little pigs named
<a href="http://example.com/larry" class="pig" id="link1">Larry,</a>
<a href="http://example.com/mo" class="pig" id="link2">Mo</a>, and
<a href="http://example.com/curly" class="pig" id="link3">Curly.</a>
<p>The three pigs had an odd fascination with experimental construction.</p>
<p>...</p>
</body></html>
"""


# Problem 1
def prob1():
    """Examine the source code of http://www.example.com. Determine the names
    of the tags in the code and the value of the 'type' attribute associated
    with the 'style' tag.

    Returns:
        (set): A set of strings, each of which is the name of a tag.
        (str): The value of the 'type' attribute in the 'style' tag.
    """
    tags = {'html','head','title','meta','style','div','h1','p','a'}
    type_attribute = 'text/css'
    return tags, type_attribute


# Problem 2
def prob2(code):
    """Return a list of the names of the tags in the given HTML code."""
    return [tag.name for tag in BeautifulSoup(code, 'html.parser').find_all(True)]
        

# Problem 3
def prob3(filename="example.html"):
    """Read the specified file and load it into BeautifulSoup. Find the only
    <a> tag with a hyperlink and return its text.
    """
    soup = BeautifulSoup(filename, 'html.parser')
    for child in soup.child.descendants:
        if child.name == 'p':
            if 'href' in child.attrs.keys():
                return str(child)


# Problem 4
def prob4(filename="san_diego_weather.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the following tags:

    1. The tag containing the date 'Thursday, January 1, 2015'.
    2. The tags which contain the links 'Previous Day' and 'Next Day'.
    3. The tag which contains the number associated with the Actual Max
        Temperature.

    Returns:
        (list) A list of bs4.element.Tag objects (NOT text).
    """
    with open(filename, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    '''
    basket = []
    dates = soup.find_all(class_='history-date')
    for date in dates:
        if "Thursday, January 1, 2015" in str(date):
            basket.append(date)
    '''
    basket = [date for date in soup.find_all(class_='history-date') if "Thursday, January 1, 2015" in str(date)]
    basket.extend([link for link in soup.find_all(name='a') if ("Previous Day" in str(link) or "Next Day" in str(link))])
    basket.append(soup.find(class_='wx-value', text=re.compile('59')))
    return basket


# Problem 5
def prob5(filename="large_banks_index.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the tags containing the links to bank data from September 30, 2003 to
    December 31, 2014, where the dates are in reverse chronological order.

    Returns:
        (list): A list of bs4.element.Tag objects (NOT text).
    """
    raise NotImplementedError("Problem 5 Incomplete")


# Problem 6
def prob6(filename="large_banks_data.html"):
    """Read the specified file and load it into BeautifulSoup. Create a single
    figure with two subplots:

    1. A sorted bar chart of the seven banks with the most domestic branches.
    2. A sorted bar chart of the seven banks with the most foreign branches.

    In the case of a tie, sort the banks alphabetically by name.
    """
    raise NotImplementedError("Problem 6 Incomplete")
