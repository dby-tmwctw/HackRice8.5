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
