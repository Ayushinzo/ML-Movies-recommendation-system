from ast import literal_eval
from nltk.stem.porter import PorterStemmer

def get_names(obj):
    '''This function takes a string representation of a list of dictionaries, evaluates it, and extracts the "name" value from each dictionary, returning a list of names.'''
    a = []
    for i in literal_eval(obj):
        a.append(i["name"])
    return a


def get_character_name(obj):
    '''This function takes a string representation of a list of dictionaries, evaluates it, and extracts the "character" and "name" values from each dictionary, returning a list of character names and actor names. It limits the results to the first 4 entries.'''
    res = []
    limit = 1
    for i in literal_eval(obj):
        if limit != 5:
            res.append(i["character"])
            res.append(i["name"])
            limit = limit + 1
        else:
            break
    return res


def get_director(obj):
    '''This function takes a string representation of a list of dictionaries, evaluates it, and extracts the "name" value from the dictionary where the "job" is "Director", returning a list containing the director's name.'''
    res = []
    for i in literal_eval(obj):
        if i['job'] == 'Director':
            res.append(i['name'])
            break
    return res


ps = PorterStemmer()
def stem(text):
    '''This function takes a string of text, splits it into individual words, applies stemming to each word using the Porter Stemmer, and then joins the stemmed words back into a single string.'''
    y = []
    for i in text.split():
        y.append(ps.stem((i)))
    return " ".join(y)


def extract_director_from_crew(crew_text):
    try:
        crew_data = literal_eval(crew_text)
        for person in crew_data:
            if person.get("job") == "Director":
                return person.get("name")
    except:
        pass
    return ""

def extract_genres(text):
    try:
        data = literal_eval(text)
        return ", ".join([g["name"] for g in data])
    except:
        return ""