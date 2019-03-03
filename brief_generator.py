import collections
import pandas
import numpy as np

def compute_increase_rate(input_data):
    """
    This function computes the increase rate for the input data
    :param input_data: a dictionary that contains the stock prices for each company
    :return: a list that contains the increasing rate of stock price every day
    """
    rates = {}
    for comp in input_data:
        stock_prices = input_data[comp][1]
        rates[comp] = []
        for i in range(len(stock_prices)-1):
            # Add a new increase rate to the dictionary
            rates[comp].append((stock_prices[i] - stock_prices[i+1])/stock_prices[i+1])
    return rates

def compute_zscore(input_data, comp_name):
    """
    Compute the z-score for a group of data
    :param input_data: the rate the stock prices increase for every day
           comp_name: the name of the company
    :return: the newest zscore for the data
    """
    try:
        input_data = np.array(input_data[comp_name])
    except KeyError:
        print("The company is not included in our database")
        return False
    # Initialize the z-score list
    zscore = []
    # For each piece of data, compute its z-score
    for i in range(len(input_data)):
        daily_zscore = (input_data[i] - np.mean(input_data))/np.std(input_data)
        zscore.append(daily_zscore)
    return zscore[0]

# print(compute_zscore(compute_increase_rate({'lmao':(3.5, [100,2,3,4,5])}), 'lmao'))

def rev_dict(input_dict):
    """
    Helper function which makes the values of the dict become the key
    :param input_dict: the input dictionary. Each key only has one corresponding
    :return: a dictionary where the keys are the original dictionary's values, and the
             keys are all positive
    """
    return_dict = {}
    for i, j in input_dict.items():
        return_dict[abs(j)] = i
    return return_dict

def fin_advice(input_data, num_advice=3):
    """
    This return the advice that whether we should keep the stock, sell it, or buy it
    :param input_data: Alex's style of data for the company
           num_advice: the number of advice given, with default being 3
    :return: a list of strings which contains the advice
    """
    # Initialize the advice list
    advice = []
    # Compute the Z-score for a certain company
    inc_rate = compute_increase_rate(input_data)
    zscore = {}
    # Map each Z-Score to each company
    for comp_name in input_data.keys():
        zscore[comp_name] = compute_zscore(inc_rate, comp_name)
    # Reverse the dictionary z-score. (This help to find the max z-score)
    rev_zscore = rev_dict(zscore)
    for i in range(num_advice):
        if len(rev_zscore) == 0:
            break
        # Find and delete the company with the greatest absolute z-score
        use_zscore = max(rev_zscore.keys())
        use_comp = rev_zscore[use_zscore]
        del rev_zscore[use_zscore]
        # Determine the advice given for that certain company
        if zscore[use_comp] > 1:
            advice.append("Sell " + use_comp + " Stock")
        elif zscore[use_comp] < -1:
            advice.append("Buy " + use_comp + " Stock")
        else:
            advice.append("Keep " + use_comp + " Stock")
    return advice

def return_rise(companies):
    """
    :param companies: given dictionary
    :return: companies that have rise in stock price percentage
    """
    rise_company_and_percentrage = {}
    for company, data in companies.items():
        if data[0]>0:
            rise_company_and_percentrage[company] = data[0]
    return rise_company_and_percentrage

def return_fall(companies):
    """
    :param companies: given dictionary
    :return: companies that have fall in stock price percentage
    """
    fall_company_and_percentrage = {}
    for company, data in companies.items():
        if data[0] < 0:
            fall_company_and_percentrage[company] = data[0]
    return fall_company_and_percentrage

def highest_rise(rise_company):
    """
    :param rise_company: dictionary result from return_rise
    :return: the highest rise company
    """
    max = 0
    max_company = None
    for company, percentage in rise_company.items():
        if percentage[0] > max:
            max = percentage[0]
            max_company = company
    return (max_company, max)

def highest_fall(fall_company):
    """
    :param rise_company: dictionary result from return_fall
    :return: the highest fall company
    """
    min = 0
    min_company = None
    for company, percentage in fall_company.items():
        if percentage[0] < min:
            min = percentage[0]
            min_company = company
    return (min_company, min)

def month_average(companies):
    """
    compute monthly average for each company
    :param companies: given dictionary
    :return: a dictionary where key is name of the company and value is the average stock price
    """
    company_average = {}
    for company, data in companies.items():
        sum = 0
        for price in data[1]:
            sum += price
        company_average[company] = sum/len(data[1])

    return company_average

def combining(head, data, tail=None):
    """
    :param head: a head string
    :param data: data which will be added to the string
    :param tail: tail string(optional)
    :return: a combined string with head and data
    """
    if len(data) == 0:
        return head+'No Company :)'
    else:
        string = head
        for company, percentage in data.items():
            string += company + ' ' + str(percentage) + '%; '
        return string

def return_brief(companies,advice):
    brief = ""
    rise_comp = return_rise(companies)
    fall_comp = return_fall(companies)
    high_rise_comp = highest_rise(companies)
    high_fall_comp = highest_fall(companies)

    return_rising_string = combining("Rising stocks: ", rise_comp)
    return_falling_string = combining("Falling stocks: ", fall_comp)
    if high_rise_comp[0] ==None:
        return_high_rise = 'No highest rising stock :('
    else:
        return_high_rise = "Highest rising stock: " + str(high_rise_comp[0]) + "  " + str(high_rise_comp[1])+'%'
    if high_fall_comp[0] ==None:
        return_high_fall = 'No highest fall stock :)'
    else:
        return_high_fall = "Highest falling stock: " + str(high_fall_comp[0]) + " " + str(high_fall_comp[1])+'%'

    brief = return_rising_string+'\n'+return_falling_string+'\n' + return_high_rise+'\n' + return_high_fall+'\n'+'Advice:'+'\n'
    for order in range(len(advice)):
        brief = brief+str(order+1)+'. '+advice[order]+'\n'
    return brief
