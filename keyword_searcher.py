def txt_to_list(keyword, fname):
    """
    Return text in a .txt file as a string
    """
    with open(fname,'r') as f:
        ret_str = f.read()
    return ret_str
    

def keywords_in_str(keywords_lst, text):
    """
    Finds all keywords in a text string
    
    Args:
        keywords_lst: A list of keywords to search in text
        text: A string
    Returns:
        A list of capitalized strings for all keywords found in text.

    References:
    https://medium.com/quantrium-tech/extracting-words-from-a-string-in-python-using-regex-dac4b385c1b8
    https://docs.python.org/3/library/re.html
    https://docs.python.org/3/library/string.html#string.capwords
    """
    import re, string
    keywords = '|'.join(keywords_lst)
    found_lst = re.findall(keywords, text, flags = re.IGNORECASE)
    found_lst = set(map(string.capwords, found_lst))
    return list(found_lst)
