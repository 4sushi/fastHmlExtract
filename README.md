# FastHtmlExtract

## Description

Simple library to extract parts of HTML file, by tags names. Alternative to Beautiful Soup for simple usages.
Useful to process big files or a lot of files (web scraping). The selection is only possible by tag type.

## Python version

Python 2 and Python 3

## Examples

### Function extract

```python
html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Title 1</h1>
    <p>Paragraph 1<br/></p>
    <p>Paragraph <b>2</b></p>
    <!-- <p>Paragraph in comment</p> -->
    </body>
    </html> 
    """
    
html_by_tags = fastHtmlExtract.extract(html, ['p', 'h1'])
print(html_by_tags)
```

Output :

```text
{
    'p': [
        '<p>Paragraph 1<br/></p>', 
        '<p>Paragraph <b>2</b></p>'
    ], 
    'h1': [
        '<h1>Title 1</h1>'
    ]
}
```

### Function count

```python
html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Title 1</h1>
    <p>Paragraph 1<br/></p>
    <p>Paragraph <b>2</b></p>
    <!-- <p>Paragraph in comment</p> -->
    </body>
    </html> 
    """
    
count_by_tags = fastHtmlExtract.count(html, ['p', 'h1'])
print(count_by_tags)
```

Output :

```text
{
    'p': 2, 
    'h1': 1
}
```

### Function get_text

```python
html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Title 1</h1>
    <p>Paragraph 1<br/></p>
    <p>Paragraph <b>2</b></p>
    <!-- <p>Paragraph in comment</p> -->
    </body>
    </html> 
    """
    
text = fastHtmlExtract.get_text(html)
print(text)
```

Output :

```text
Title 1 Paragraph 1 Paragraph 2 
```

### Combined functions

```python
html = """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Title 1</h1>
    <p>Paragraph 1<br/></p>
    <p>Paragraph <b>2</b></p>
    <!-- <p>Paragraph in comment</p> -->
    </body>
    </html> 
    """

html_elements = fastHtmlExtract.extract(html, ['p'])
paragraphs = html_elements['p']
for p in paragraphs:
    text = fastHtmlExtract.get_text(p)
    print(text)
```

Output :

```text
Paragraph 1 
Paragraph 2 
```

## Speed FastHtmlExtract / Beautiful Soup


```python
import fastHtmlExtract
import urllib
import re
from bs4 import BeautifulSoup
import timeit

def fast_extract_titles(html):
    titles = []
    html_elements = fastHtmlExtract.extract(html, ['h1', 'h2', 'h3'])
    titles_html = html_elements['h1'] + html_elements['h2'] + html_elements['h3']
    for title_html in titles_html:
        text = fastHtmlExtract.get_text(title_html)
        titles.append(text)
    return titles

def beautiful_soup_extract_titles(html):
    titles = []
    soup = BeautifulSoup(html, 'html.parser')
    titles_bf = soup.find_all(re.compile(r'(h1|h2|h3)'))
    for title_bf in titles_bf:
        text = title_bf.get_text(' ').encode('utf8')
        titles.append(text)
    return titles

if __name__ == "__main__":
    url = 'https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji'
    html = urllib.urlopen(url).read()
    # Compare result
    titles_1 = fast_extract_titles(html)
    titles_2 = beautiful_soup_extract_titles(html)
    print(titles_1)
    # ['List of j\xc5\x8dy\xc5\x8d kanji', 'Contents', 'List of characters [ edit ]', 'See also [ edit ]', 'Notes [ edit ]', 'External links [ edit ]', 'Navigation menu', 'Personal tools', 'Namespaces', 'Variants', 'Views', 'More', 'Search', 'Navigation', 'Interaction', 'Tools', 'Print/export', 'In other projects', 'Languages']
    print(titles_2)
    # ['List of j\xc5\x8dy\xc5\x8d kanji', 'Contents', 'List of characters [ edit ]', 'See also [ edit ]', 'Notes [ edit ]', 'External links [ edit ]', 'Navigation menu', 'Personal tools', 'Namespaces', '\n Variants \n', 'Views', 'More', '\n Search \n', 'Navigation', 'Interaction', 'Tools', 'Print/export', 'In other projects', 'Languages']
    # Compare performances
    print(timeit.timeit('fast_extract_titles(html)', number=1000, setup="from __main__ import fast_extract_titles, html"))
    # 2.17549295306
    print(timeit.timeit('beautiful_soup_extract_titles(html)', number=1000, setup="from __main__ import beautiful_soup_extract_titles, html"))
    # 23.444286399
```

In this case, for a simple extraction, fast_extract_titles is 10 times faster.
