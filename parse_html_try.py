import urllib.request
import pandas
import pandas_datareader.data as web
import datetime as dt
from brief_generator import *
from language_processing import determine_which_function

# company_list = ['Apple', 'Facebook', 'Google', 'Microsoft', 'Amazon', 'Google']
# time_hours = 1

def read_graph(filename):
    """
    Read a graph from a file.  The file is assumed to hold a graph
    that was written via the write_graph function.

    Arguments:
    filename -- name of file that contains the graph

    Returns:
    The graph that was stored in the input file.
    """
    with open(filename) as f:
        g = eval(f.read())
    return g

def write_graph(g, filename):
    """
    Write a graph to a file.  The file will be in a format that can be
    read by the read_graph function.

    Arguments:
    g        -- a graph
    filename -- name of the file to store the graph

    Returns:
    None
    """
    with open(filename, 'w') as f:
        f.write(repr(g))

def now_data(company_code):
    '''
    Given a company code, return a tuple whose first element is the company's
    current stock price, and second element is the company's percentage
    change in price now
    '''
    # First, get the website as a string
    url1 = urllib.request.urlopen('https://www.nasdaq.com/symbol/' + company_code)
    whole_string1 = str(url1.read())
    # Find price of the stocks now
    search_string1_1 = '<div id="qwidget_lastsale" class="qwidget-dollar">'
    index1_1 = whole_string1.find(search_string1_1)
    index_next_1 = whole_string1.find('<', index1_1 + 51)
    now_price = float(whole_string1[index1_1 + 51:index_next_1])
    # Find the percentage change
    search_string1_2 = '<div id="qwidget_percent"'
    index1_2 = whole_string1.find(search_string1_2)
    index_next_2 = whole_string1.find('>', index1_2 + 51)
    index_next_3 = whole_string1.find('%', index_next_2)
    now_increase = float(whole_string1[index_next_2 + 1:index_next_3])
    # Check whether it is increasing or decreasing
    search_string1_3 = '<div id="qwidget-arrow">'
    index1_3 = whole_string1.find(search_string1_3)
    is_negative = (whole_string1[index1_3 + 49:index1_3 + 58] == 'arrow-red')
    if (is_negative):
        now_increase = 0 - now_increase
    return tuple([now_price, now_increase])

# print (now_data('FB'))

def hist_stock(comp_name, start_date=dt.datetime(2019, 1, 10), end_date=dt.datetime.today(), span=30):
    """
    This function returns the stock price data for a certain company for a given
    time span
    :param comp_name: the company's name
    :param start_date: the date we start recording the data
    :param end_date: the date we stop recording the data
    :param span: an integer represents the amount of data we need
    :return:
    """
    # Get all the data
    df = web.DataReader(comp_name, 'yahoo', start_date, end_date)
    # Extract the ones that we need
    df = df.tail(span)
    # Enter the close price for last month
    close_price = []
    for i in df['Close']:
        close_price.append(i)
    close_price.reverse()
    close_price.pop(0)
    return close_price

def return_dict(company_list, company_dictionary):
    dictionary = {}
    for company in company_list:
        complete_list = []
        company_tuple = now_data(company_dictionary[company])
        history_list = list(hist_stock(company_dictionary[company]))
        # print (company_tuple)
        now_percentage = company_tuple[1]
        complete_list.append(company_tuple[0])
        complete_list.extend(history_list)
        dictionary[company] = tuple([now_percentage, complete_list])
    return dictionary

# print (now_data('aapl'))

def brief(company_list):
    company_dictionary = read_graph('company_graph.repr')
    needed_dictionary = return_dict(company_list, company_dictionary)
    advice = fin_advice(needed_dictionary)
    brief = return_brief(needed_dictionary, advice)
    return brief

# company_list = ['Apple', 'Facebook', 'Google', 'Microsoft', 'Amazon', 'Google']
#
# def test_send(string):
#     global company_list
#     print (company_list)
#     parse_tuple = determine_which_function(string)
#     print (parse_tuple)
#     control_sequence = parse_tuple[0]
#     if control_sequence == 1:
#         company_list = parse_tuple[1]
#         return 'All set'
#     elif control_sequence == 2:
#         time_hours = parse_tuple[1]
#         return 'OK!'
#     elif control_sequence == 3:
#         if parse_tuple[1] != None:
#             company_list = parse_tuple[1]
#         send_text = brief(company_list)
#         return send_text
#
# print (test_send('I am interested in Apple, Google, Microsoft'))

# print (brief(company_list))
# print (now_data(company_dictionary['Facebook']))
# print (return_dict(company_dictionary.keys(), company_dictionary))
# for company in company_dictionary.keys():
#     print (now_data(company_dictionary[company]))
#     print (hist_stock(company_dictionary[company]))


# write_graph(return_dict(company_dictionary.keys(), company_dictionary), 'sample_return.repr')
#
# dictionary = read_graph('company_graph.repr')
# # print (dictionary)
# print (return_dict(dictionary.keys(), dictionary))
