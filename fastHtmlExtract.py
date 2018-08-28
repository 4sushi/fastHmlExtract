# coding: utf-8

"""
Fast extract HTML tag  (is fast compare beautiful soup library or similar)
Note : useful for simple case in a big HTML files
Author : 4sushi
"""


def extract(html, tags):
    """
    Fast extract tags in html file

    >>> extract('<p><b>Test</b></p><a>Test 2</a>', ['p', 'b'])
    {'p': ['<p><b>Test</b></p>'], 'b': ['<b>Test</b>']}

    :param html: html code
    :type html: str
    :param tag: html tag (ex : table)
    :type tag: str
    :return: list[str]
    """
    tags = [tag.lower() for tag in tags]
    tags_position = {}
    html_elements = {}
    for tag in tags:
        html_elements[tag] = []
    len_html = len(html)
    i_char = 0
    while i_char < len_html:
        c = html[i_char]
        if c == '<':
            # comment
            if len_html >= i_char+4 and html[i_char:i_char+4] == '<!--':
                while len_html >= i_char+3 and html[i_char:i_char+3] != '-->':
                    i_char += 1
                i_char += 2  # position on '>' char
            # tag close (paired tag)
            elif len_html >= i_char+2 and html[i_char:i_char+2] == '</':
                # find tag name
                tag_name = ''
                i_char += 2  # position on tag name
                while len_html >= i_char and html[i_char] not in ['>', ' ', '/', '\n']:
                    tag_name += html[i_char]
                    i_char += 1
                tag_name = tag_name.lower()
                # go to the end of tag
                while len_html >= i_char and html[i_char] != '>':
                    i_char += 1
                if tag_name in tags_position:
                    if len(tags_position[tag_name]) > 0:
                        tag = tags_position[tag_name].pop()
                        tag['end'] = i_char + 1
                        # Extract part html corresponding to the DOM object
                        if tag['type'] in tags:
                            ele = html[tag['start']:tag['end']]
                            html_elements[tag['type']].append(ele)
            # tag open (single/paired tag)
            else:
                i_start = i_char
                # find tag name
                tag_name = ''
                i_char += 1
                while len_html >= i_char and html[i_char] not in ['>', ' ', '/', '\n']:
                    tag_name += html[i_char]
                    i_char += 1
                tag_name = tag_name.lower()
                if tag_name not in tags_position:
                    tags_position[tag_name] = []
                tags_position[tag_name].append({'start': i_start, 'type': tag_name})
                # go end tag
                while len_html >= i_char and html[i_char] != '>':
                    i_char += 1
                # if single tag
                if tag_name in ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen',
                                'link', 'meta', 'param', 'source', 'track', 'wbr']:
                    tag = tags_position[tag_name].pop()
                    tag['end'] = i_char + 1
                    # Extract part html corresponding to the DOM object
                    if tag['type'] in tags:
                        ele = html[tag['start']:tag['end']]
                        html_elements[tag['type']].append(ele)
        i_char += 1
    return html_elements


def count(html, tags):
    """
    Count tags in html

    >>> count('<p><b>Test</b></p><a>Test 2</a>', ['p', 'b'])
    {'p': 1, 'b': 1}

    :param html: html code
    :type html: str
    :param tags: tags to count
    :type tags: list[str]
    :return: a dictionary => key : tag, value : number of tag
    :rtype: dict[str, int]
    """
    tags = [tag.lower() for tag in tags]
    html_elements = extract(html, tags)
    # Init tags_count
    tags_count = {}
    for tag in tags:
        tags_count[tag] = len(html_elements[tag])
    return tags_count


def get_text(html):
    """
    Return the text of the html (the text inside and outside the tags)

    >>> get_text('abc <p> def <br/>ghi<b>jkl</b></p>1234')
    'abc def ghi jkl 1234'

    :param html: the html code
    :type html: str
    :rtype: str
    """
    text = ''
    len_html = len(html)
    i_char = 0
    while i_char < len_html:
        c = html[i_char]
        if c == '<':
            if len(text) > 0 and text[-1] != ' ':
                text += ' '
            # comment
            if len_html >= i_char + 4 and html[i_char:i_char + 4] == '<!--':
                while len_html >= i_char + 3 and html[i_char:i_char + 3] != '-->':
                    i_char += 1
                i_char += 2  # position on '>' char
            # tag
            else:
                # go to the end of tag
                while len_html >= i_char and html[i_char] != '>':
                    i_char += 1
        # TODO : edit list of special char if need to manage more cases
        elif c in [' ', '\n', '\t']:
            if len(text) > 0 and text[-1] != ' ':
                text += ' '
        else:
            text += c
        i_char += 1
	# remove if last char is a space
    if len(text) > 0 and text[-1] == ' ':
        text = text[:len(text)-1]
    return text
