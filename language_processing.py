import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag
from nltk.tag import StanfordNERTagger
from nltk.stem.snowball import SnowballStemmer

all_companies = 'I want to use Amazon, Tesla, Oracle, Apple, Google, google, apple, Microsoft, IBM, Intel, Compass, Adobe, SAP, ZOOM, Samsung, TENCENT, Sony, Alibaba, JBL, Dell'
extended_tech = ['google', 'apple', 'tencent', 'ZOOM', 'Zoom', 'microsoft', 'Oracle', 'oracle', 'Compass', 'compass', 'Razer', 'zoom']
inform_indicators = ['BRIEF','INFORM','TELL']
immediacy_indicators = ['NOW', 'TODAY', 'PRESENTLY', 'CURRENTLY']
frequency_indicators = ['HOUR','HOURS','MINUTE','MINUTES','SECOND','SECONDS','DAY','DAYS','WEEK','WEEKS','MONTH','MONTHS']
interval_indicators = ['EVERY','PER','ALL','ANY','TOTAL']
interest_syn = ['INTEREST','LIKE','ENGAGE','EXCITE','LIKE','ENJOY','LOVE','PREFER','WANT','APPRECIATE','NEED','WISH','EAGER']

st = StanfordNERTagger('D:\Hack Rice 8.5\stanford-ner-20190302T185118Z-001\stanford-ner\classifiers\english.all.3class.distsim.crf.ser.gz',
                       'D:\Hack Rice 8.5\stanford-ner.jar')


# text = "I'm interested in Apple, Amazon, Google"
# test_text = 'I want to brief every 12 hours'

# sents = sent_tokenize(text)
#
# words = word_tokenize(test_text)
# postag_list = nltk.pos_tag(words)
#print (nltk.pos_tag(words))

def get_postag(text):
    words = word_tokenize(text)
    postag_list = nltk.pos_tag(words)

    return postag_list

def has_interval(postag_list):
    """

    :param postag_list: the list of tag of each word.
    :return: return True or False if the given pos_tag list has number in it
    """
    frequency_indicators = ['HOUR', 'HOURS', 'MINUTE', 'MINUTES', 'SECOND', 'SECONDS', 'DAY', 'DAYS', 'WEEK', 'WEEKS',
                            'MONTH', 'MONTHS']
    interval_indicators = ['EVERY', 'PER', 'ALL', 'ANY', 'TOTAL']
    for i in range(len(postag_list)-1):
        if postag_list[i][1] == 'CD':
            return True
        elif postag_list[i][0].upper() in interval_indicators:
            if (postag_list[i+1][0]).upper() in frequency_indicators:
                return True

    return False

def get_companies(text):
    """

    :param text: given messege
    :return: set of companies in uppercase
    """
    extended_tech = ['google', 'apple', 'tencent', 'ZOOM', 'Zoom', 'microsoft', 'Oracle', 'oracle', 'Compass',
                     'compass', 'Razer', 'zoom']

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    companies = []

    for words in classified_text:
        if words[1] == 'ORGANIZATION' or words[1] == 'PERSON' or words[1] == 'LOCATION':
            companies.append(words[0].upper())

    for words in classified_text:
        for company in extended_tech:
            if words[0].casefold() == company.casefold():
                companies.append(words[0].upper())
    return list(set(companies))

#print(get_companies(test_text, extended_tech))

def brief_now(text):
    """
    Determine whether we need to brief the user right now
    :param text: given message
    :param immediacy_indicator: immediacy indicator base
    :return: True if we need to te brief now, False otherwise.
    """
    immediacy_indicators = ['NOW', 'TODAY', 'PRESENTLY', 'CURRENTLY']
    inform_indicators = ['BRIEF', 'INFORM', 'TELL']
    stemmer = SnowballStemmer("english")

    original_text = text
    postag_list = get_postag(original_text)

    if has_interval(postag_list):
        return False

    for pair in postag_list:
        if pair[1] == 'DT' and pair[0].upper() in interval_indicators:
            return False

    #has keyword now, return
    for pair in postag_list:
        if pair[1] == 'RB':
            if pair[0].upper() in immediacy_indicators:
                return True
    #start with a command verb
    for pair in postag_list:
        if (pair[0].upper() == 'BRIEF' and pair[1] == 'IN') or (stemmer.stem(pair[0]).upper() in inform_indicators):
            return True

    return False

#print(brief_now(test_text))

def entities(text):
    return ne_chunk(pos_tag(word_tokenize(text)))

def set_interval(text):
    """
    find the interval of set
    :param text: given message
    :return: return the interval (number, time)
    """
    interval_indicators = ['EVERY', 'PER', 'ALL', 'ANY', 'TOTAL']
    frequency_indicators = ['HOUR', 'HOURS', 'MINUTE', 'MINUTES', 'SECOND', 'SECONDS', 'DAY', 'DAYS', 'WEEK', 'WEEKS',
                            'MONTH', 'MONTHS']
    original_text = text
    postag_list = get_postag(original_text)
    for i in range(len(postag_list)-1):
        if postag_list[i][1] == 'CD':
            return (postag_list[i][0],(postag_list[i+1][0]).upper())
        if postag_list[i][0].upper() in interval_indicators:
            if (postag_list[i+1][0]).upper() in frequency_indicators:
                return (1,(postag_list[i+1][0]).upper())

#print(set_interval(test_text))


def alter_companies_caps(name_all_caps):
    """
    return capitalized company name list
    :param name_all_caps: list of company names that are in all cap mode
    :return: capitalized company names
    """
    companies_names = []
    for companies in name_all_caps:
        companies_names.append(companies.lower().capitalize())
    return companies_names

#print(alter_companies_caps(get_companies(test_text, extended_tech)))



def if_set_company_list(text):
    interest_syn = ['INTEREST', 'LIKE', 'ENGAGE', 'EXCITE', 'LIKE', 'ENJOY', 'LOVE', 'PREFER', 'WANT', 'APPRECIATE',
                    'NEED', 'WISH', 'EAGER']
    stemmer = SnowballStemmer("english")
    original_text = text
    words = word_tokenize(original_text)
    postag_list = nltk.pos_tag(words)
    for word in postag_list:
        if stemmer.stem(word[0]).upper() in interest_syn:
            return True
    return False

#print(if_set_company_list(text))



def determine_which_function(text):
    """
    which return the function
    :param text: given message
    :return: a tuple, where first element is a integer 0:noting matched, 1:setting up company list, 2:setting up interval, 3:brief now.
    """
    original_text = text
    postag_list = get_postag(original_text)

    if brief_now(text):
        if len(get_companies(text)) != 0:
            return (3, alter_companies_caps(get_companies(text)))
        else:
            return (3, None)
    if has_interval(postag_list):
        return (2, list(set_interval(text)))
    if if_set_company_list(text):
        return (1, alter_companies_caps(get_companies(text)))
    else:
        return (0, None)


# print(determine_which_function('I am interested in Apple, Google, Microsoft'))
