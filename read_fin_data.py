import pandas
import pandas_datareader.data as web
import datetime as dt

def hist_stock(comp_name, start_date=dt.datetime(2015,1,1), end_date=dt.datetime.today(), span=30):
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
    close_price.pop(0)
    return close_price

print(hist_stock('GOOG'))
