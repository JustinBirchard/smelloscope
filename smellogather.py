# smellogather.py
#* Version 0.9
#* Last update 10/23/22

"""smellogather takes a user supplied list of stocks and pulls in a wide
   variety of metrics and data via OpenBB. 

   Each stock will become a Company object and can be examined easily via
   calls and methods. 

   The main point of this script is to the create company_list variable
   which holds one or more instaniated Company objects

Returns:
    list: company_list containing Company class objects
"""

import math
import pandas as pd
from openbb_terminal.api import openbb as obb
from company import Company, PeerGroup

peers = [('MSFT', 1), ('AAPL', 2), ('ORCL', 3), ('PRGS', 4)]

# used to convert strings representing percentage to a float, eg '10%' becomes 0.1
def p2f(str_perc):
    return float(str_perc.strip('%'))/100

# used for error handling when making calls to OpenBB
def try_it(string, calltype, avg=False, p2f_bool=False):
    
    if calltype == 'data' and p2f_bool is False:
        try:
            return float(obb.stocks.fa.data(stock).loc[string][0])

        except KeyError:
            return 'n/a'
        
    elif calltype == 'data' and p2f_bool is True:
        try:
            return p2f(obb.stocks.fa.data(stock).loc[string][0])
        
        except KeyError:
            return 'n/a'
        
    elif calltype == 'metrics' and avg is False:    
        try:            
            return df_metrics.loc[string][0]
                    
        except KeyError:
            return 'n/a'
        
    elif calltype == 'metrics' and avg is True:    
        try:
            return df_metrics.loc[string]['5yr Avg']
            
        except KeyError:
            return 'n/a'

for company in peers:
    
    stock = company[0]
    slot = company[1]

############## *** Making calls to OpenBB to get collections of data: *** ###################
# Sequences in this section will be massaged and used later to set company object variables #
  
    # fmp's api will sometimes throw error and return an empty list instead of requested dataframe
    df_metrics = obb.stocks.fa.fmp_metrics(stock)                                                                                    
    if not isinstance(df_metrics, pd.DataFrame):
        raise TypeError('Dag nabbit!' + ' ' + stock + ' is not available via FMP api. Failed to build df_metrics')
        
    # Where possible, converting strings to floats in df_metrics    
    float_error_set = set() 
    for column in df_metrics.columns:
        
        for row in df_metrics.index:
            
            try:
                df_metrics[column][row] = float(df_metrics[column][row])
                
            except ValueError: # catching the row names for those that cannot be converted to float
                float_error_set.add(row)
                
    df_metrics_discarded = pd.DataFrame() # holds data removed from df_metrics in case needed later
    for row in float_error_set: # Adding appropriate rows to the new dataframe
        df_metrics_discarded[row] = df_metrics.loc[row]

    df_metrics_discarded = df_metrics_discarded.T # transposing so it matches format of df_metrics
    
    # Removing any row from df_metrics where values cannot be converted to float
    df_metrics = df_metrics.drop(index= float_error_set)
    
    # Creating new column that will hold the average of each row
    df_metrics['5yr Avg'] = df_metrics.mean(axis=1)

    # Getting Stock Twits sentiment data as a tuple:
    tuple_twits = obb.stocks.ba.bullbear(stock)
    
    # Analyst recommendation totals by type over last 3 months
    df_rot = obb.stocks.dd.rot(stock).T[0]

################################################################################################    
# Creating variables for readability then grouping values into DataFrames & Sequences       
    
############## *** BASIC DETAILS DATAFRAME *** ##############

    name = obb.stocks.fa.profile(stock).loc['companyName'][0]
    ticker = stock
    sector = obb.stocks.fa.profile(stock).loc['sector'][0]
    industry = obb.stocks.fa.profile(stock).loc['industry'][0]
    cap = obb.stocks.fa.quote(stock).loc['Market cap'][0]
    price = obb.stocks.fa.quote(stock).loc['Price'][0]
    
    # DataFrame will be added to company object
    df_basic = pd.DataFrame({'name': name, 'ticker': ticker, 'sector': sector,
                             'industry': industry, 'cap': cap, 'price': price}, 
                              index=['Basic Details']).T
    
############## *** VALUE METRICS DATAFRAME *** ##############

    tca = obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Total current assets'][0]

    # Case for if the company has no debt
    if math.isnan(obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Long-term debt'][0]) is True:
        tld = 0 
    
    elif obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Long-term debt'][0] is None:
        tld = 0         
    
    else:  
        tld = obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Long-term debt'][0]

    if tld == 0:
        tca_div_tld = 'n/a'
    else:
        tca_div_tld = tca / tld
 
    ptb_mrq = try_it('P/B', 'data')
    ptb_ttm = df_metrics.loc['Ptb ratio'][0]
    ptb_5yr_avg = df_metrics.loc['Ptb ratio']['5yr Avg']

    bvps_mrq = float(obb.stocks.fa.data(stock).loc['Book/sh'][0])
    bvps_ttm = df_metrics.loc['Book value per share'][0]
    bvps_5yr_avg = df_metrics.loc['Book value per share']['5yr Avg']
    
    pe_mrq = try_it('P/E', 'data')
    pe_ttm = try_it('Pe ratio', 'metrics')
    pe_5yr_avg = try_it('Pe ratio', 'metrics', avg=True)
        
    pfcf_mrq = try_it('P/FCF', 'data')
    pfcf_ttm = try_it('Pfcf ratio', 'metrics')
    pfcf_5yr_avg = try_it('Pfcf ratio', 'metrics', avg=True)

    pts_mrq = try_it('P/S', 'data')
    pts_ttm = try_it('Price to sales ratio', 'metrics')
    pts_5yr_avg = try_it('Price to sales ratio', 'metrics', avg=True)

    # DataFrame will be added to company object   
    df_value = pd.DataFrame({'tca': tca, 'tld': tld, 'tca_div_tld': tca_div_tld,
                             'ptb_mrq': ptb_mrq, 'ptb_ttm': ptb_ttm, 'ptb_5yr_avg': ptb_5yr_avg, 
                             'bvps_mrq': bvps_mrq, 'bvps_ttm': bvps_ttm, 'bvps_5yr_avg': bvps_5yr_avg, 
                             'pe_mrq': pe_mrq, 'pe_ttm': pe_ttm, 'pe_5yr_avg': pe_5yr_avg, 
                             'pfcf_mrq': pfcf_mrq, 'pfcf_ttm': pfcf_ttm, 'pfcf_5yr_avg': pfcf_5yr_avg, 
                             'pts_mrq': pts_mrq, 'pts_ttm': pts_ttm, 'pts_5yr_avg': pts_5yr_avg}, 
                              index=['Value Metrics']).T
        
############## *** MANAGEMENT METRICS DATAFRAME *** ##############

    roe_mrq = p2f(obb.stocks.fa.data(stock).loc['ROE'][0])
    roe_ttm = df_metrics.loc['Roe'][0]
    roe_5yr_avg = df_metrics.loc['Roe']['5yr Avg']
    
    roa_mrq = p2f(obb.stocks.fa.data(stock).loc['ROA'][0])
    roa_ttm = df_metrics.loc['Return on tangible assets'][0]
    roa_5yr_avg = df_metrics.loc['Return on tangible assets']['5yr Avg']
    
    gpr = float(obb.stocks.fa.fmp_income(stock).loc['Gross profit ratio'][0])
    
    pm = try_it('Profit Margin', 'data', p2f_bool=True)

    cr_mrq = float(obb.stocks.fa.data(stock).loc['Current Ratio'][0])
    cr_ttm = df_metrics.loc['Current ratio'][0]
    cr_5yr_avg = df_metrics.loc['Current ratio']['5yr Avg']
    
    dte_mrq = try_it('LT Debt/Eq', 'data')
    dte_ttm = df_metrics.loc['Debt to equity'][0]
    dte_5yr_avg = df_metrics.loc['Debt to equity']['5yr Avg']
    
    # DataFrame will be added to company object    
    df_mgmt = pd.DataFrame({'roe_mrq': roe_mrq, 'roe_ttm': roe_ttm, 'roe_5yr_avg': roe_5yr_avg,
                            'roa_mrq': roa_mrq, 'roa_ttm': roa_ttm, 'roa_5yr_avg': roa_5yr_avg,
                            'gpr': gpr, 'pm': pm, 'cr_mrq': cr_mrq, 'cr_ttm': cr_ttm, 
                            'cr_5yr_avg': cr_5yr_avg, 'dte_mrq': dte_mrq, 'dte_ttm': dte_ttm,
                            'dte_5yr_avg': dte_5yr_avg}, index=['Management Metrics']).T
        
############## *** INSIDER & INSTITUION DATAFRAME *** ##############

    io = p2f(obb.stocks.fa.data(stock).loc['Insider Own'][0])
    it = p2f(obb.stocks.fa.data(stock).loc['Insider Trans'][0])

    inst_o = try_it('Inst Own', 'data', p2f_bool=True)
    inst_t = try_it('Inst Trans', 'data', p2f_bool=True)

    # DataFrame will be added to company object
    df_ins = pd.DataFrame({'io': io, 'it': it, 'inst_o': inst_o, 
                           'inst_t': inst_t}, index=['Insider & Insitution Data']).T
    
############## *** DIVIDEND DATAFRAMES *** ##############
# Note that there are 2 Dividend DataFrames: df_div & df_div_his

    div = try_it('Dividend', 'data')
    div_y = try_it('Dividend yield', 'metrics')
    
    # DataFrame will be added to company object via div_dfs list
    df_div = pd.DataFrame({'div': div, 'div_y': div_y}, index=['Dividend Metrics']).T
    
    # DataFrame (or string if no dividend) will be added to company object via div_dfs list
    df_div_his = obb.stocks.fa.divs(stock)    
    if df_div_his.empty:
        df_div_his = 'n/a'
    
    # List will be added to company object
    div_dfs = [df_div, df_div_his]
    
############## *** PUBLIC SENTIMENT & SHORT INTEREST DATAFRAME *** ##############
    
    if tuple_twits[1] != 0 and tuple_twits[2] != 0: # Normal case
        twits_perc = tuple_twits[2] / tuple_twits[1]
        
    elif tuple_twits[1] == 0: # Case for if there are no ratings
        twits_perc = 'Not Rated'
        
    elif tuple_twits[2] == 0: # Case for if all ratings are bearish
        twits_perc = 0
        
    # Getting sentiment from last 10 days of news articles
    df_news_sent = obb.stocks.ba.headlines(stock)

    sent_list = []
    for date in df_news_sent.index:
        sent_list.append(float(df_news_sent.loc[date][0]))
        
    # Calculating the average sentiment over last 10 days
    news_sent = sum(sent_list)/len(sent_list)
        
    shrt_int = p2f(obb.stocks.fa.data(stock).loc['Short Float'][0])
    
    # DataFrame will be added to company object
    df_pub_sent = pd.DataFrame({'twits_perc': twits_perc, 'shrt_int': shrt_int, 
                                'news_sent': news_sent}, index=['Public Sentiment Metrics']).T
        
############## *** COMPANY, SECTOR, & INDUSTRY NEWS *** ##############

    df_com_news = obb.common.news(name, sort='published').head(20)
    df_sec_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Company News'])
    df_ind_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Company News'])

    # List will be added to company object
    news_dfs = [df_com_news, df_sec_news, df_ind_news]
    
############## *** ANALYST RATINGS *** ##############
# Note there are 2 DataFrames and one variable here: df_rating_30d, df_rot_3mo, wb_score
  
    # Pairing df_rating down to last 30 days and converting returned Series object back into DataFrame
    df_rating_30d = obb.stocks.dd.rating(stock).T.loc['Rating'].head(30).to_frame()
    
    # DataFrame will be added to company object
    df_rot_3mo = pd.DataFrame({'Strong Buy': df_rot['strongBuy'], 'Buy': df_rot['buy'], 'Hold': df_rot['hold'], 
                               'Sell': df_rot['sell'], 'Strong Sell': df_rot['strongSell']}, index=['Last 3mo']).T

    # Warren Buffet Investing Score
    wb_score = obb.stocks.fa.score(stock)
    if wb_score is None:
        wb_score = 'n/a'       

    analyst_data = [df_rating_30d, df_rot_3mo, wb_score]
    
############## *** ESG RATINGS *** ##############

    df_esg = obb.stocks.fa.sust(stock)
    
##################################################################################    
############## *** Creating Company objects: *** #################################  
##################################################################################

    if slot == 1:
        c1 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list = []
        company_list.append(c1)
        
    elif slot == 2:
        c2 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c2)

    elif slot == 3:
        c3 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c3)
        
    elif slot == 4:
        c4 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c4)