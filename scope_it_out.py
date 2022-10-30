# scope_it_out.py
# file previously called: smellogather.py
#* Version 0.9.5
#* Last update 10/30/22

"""scope_it_out takes the user supplied list from stocklist.py and 
   pulls in a variety of metrics and data via OpenBB. 

   Each stock in the list will become a Company object and will be 
   populated with data. Data can be examined via Company methods in 
   TheSmelloscope lab.

   A PeerGroup object will also be created. PeerGroup is a subclass 
   of Company and its methods will be used to pull in every metric 
   from every Company and then calculate an average value for 
   each metric.

   After all data has been gathered and assembled, the sniffer.py
   will give each Company object a big_phat_whiff. 
   
   Once the whiff is complete, the Company's score card will be 
   accessable via the TheSmelloscope lab.

   The main point of this script is:
   1) Instantiate a Company object for each stock in stocklist.py
   2) Instantiate a PeerGroup object
   3) Create company_list which holds one or more Company objects.
   4) Analyze the data in the PeerGroup object and each Company object 
   5) Populate the score_card of each Company object

Returns:
    list: company_list containing Company class objects
    object: PeerGroup subclass object
"""

from sniffer import big_phat_whiff
from company import Company, PeerGroup
from stocklist import stocks

import math
import pandas as pd
from openbb_terminal.api import openbb as obb


# crating peers list based on user selected stocks from stocklist.py
peers = []
for index, stock in enumerate(stocks):
    peers.append((stock, index + 1))

# converts strings representing percentage to a float, eg '10%' becomes 0.1
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

    elif calltype == 'esg':    
        try:
            return df_esg.loc[string][0]
            
        except KeyError:
            return 'n/a'

        except AttributeError:
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

    # Getting ESG data
    df_esg = obb.stocks.fa.sust(stock)
    if df_esg.empty:
        df_esg = 'n/a'
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
 
    yahoo_success = 'no'
    tries = 0
 
    while yahoo_success == 'no':
        tries += 1
        try:
            tca_mrfy = obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Total current assets'][0]
            yahoo_success = 'yes'

        except AttributeError:
            print('Yahoo error. Trying again.')

    print('Number of tries : ' + str(tries))

    # Cases for if the company has no debt
    try:
        if math.isnan(obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Long-term debt'][0]) is True:
            tld_mrfy = 0 
        
        elif obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Long-term debt'][0] is None:
            tld_mrfy = 0         
        
        else:  
            tld_mrfy = obb.stocks.fa.yf_financials(stock, "balance-sheet").loc['Long-term debt'][0]

        if tld_mrfy == 0:
            tca_div_tld = 'n/a'
        else:
            tca_div_tld = tca_mrfy / tld_mrfy

    except KeyError:
        tld_mrfy = 0
        tca_div_tld = 'n/a'
 
    ptb_mrq = try_it('P/B', 'data')
    ptb_mrfy = try_it('Ptb ratio', 'metrics')
    ptb_5yr_avg = try_it('Ptb ratio', 'metrics', avg=True)

    bvps_mrq = float(obb.stocks.fa.data(stock).loc['Book/sh'][0])
    bvps_mrfy = df_metrics.loc['Book value per share'][0]
    bvps_5yr_avg = df_metrics.loc['Book value per share']['5yr Avg']
    
    pe_ttm = try_it('P/E', 'data')
    pe_mrfy = try_it('Pe ratio', 'metrics')
    pe_5yr_avg = try_it('Pe ratio', 'metrics', avg=True)
        
    pfcf_ttm = try_it('P/FCF', 'data')
    pfcf_mrfy = try_it('Pfcf ratio', 'metrics')
    pfcf_5yr_avg = try_it('Pfcf ratio', 'metrics', avg=True)

    pts_ttm = try_it('P/S', 'data')
    pts_mrfy = try_it('Price to sales ratio', 'metrics')
    pts_5yr_avg = try_it('Price to sales ratio', 'metrics', avg=True)

    # DataFrame will be added to company object   
    df_value = pd.DataFrame({'tca_mrfy': tca_mrfy, 'tld_mrfy': tld_mrfy, 'tca_div_tld': tca_div_tld,
                             'ptb_mrq': ptb_mrq, 'ptb_mrfy': ptb_mrfy, 'ptb_5yr_avg': ptb_5yr_avg, 
                             'bvps_mrq': bvps_mrq, 'bvps_mrfy': bvps_mrfy, 'bvps_5yr_avg': bvps_5yr_avg, 
                             'pe_ttm': pe_ttm, 'pe_mrfy': pe_mrfy, 'pe_5yr_avg': pe_5yr_avg, 
                             'pfcf_ttm': pfcf_ttm, 'pfcf_mrfy': pfcf_mrfy, 'pfcf_5yr_avg': pfcf_5yr_avg, 
                             'pts_ttm': pts_ttm, 'pts_mrfy': pts_mrfy, 'pts_5yr_avg': pts_5yr_avg}, 
                              index=['Value Metrics']).T
        
############## *** MANAGEMENT METRICS DATAFRAME *** ##############

    roa_ttm = p2f(obb.stocks.fa.data(stock).loc['ROA'][0])
    roa_mrfy = df_metrics.loc['Return on tangible assets'][0]
    roa_5yr_avg = df_metrics.loc['Return on tangible assets']['5yr Avg']

    roe_ttm = p2f(obb.stocks.fa.data(stock).loc['ROE'][0])
    roe_mrfy = df_metrics.loc['Roe'][0]
    roe_5yr_avg = df_metrics.loc['Roe']['5yr Avg']

    gpr_mrfy = float(obb.stocks.fa.fmp_income(stock).loc['Gross profit ratio'][0])
    
    pm_ttm = try_it('Profit Margin', 'data', p2f_bool=True)

    cr_mrq = float(obb.stocks.fa.data(stock).loc['Current Ratio'][0])
    cr_mrfy = df_metrics.loc['Current ratio'][0]
    cr_5yr_avg = df_metrics.loc['Current ratio']['5yr Avg']
    
    dte_mrq = try_it('LT Debt/Eq', 'data')
    dte_ttm = df_metrics.loc['Debt to equity'][0]
    dte_5yr_avg = df_metrics.loc['Debt to equity']['5yr Avg']
    
    # DataFrame will be added to company object    
    df_mgmt = pd.DataFrame({'roe_ttm': roe_ttm, 'roe_mrfy': roe_mrfy, 'roe_5yr_avg': roe_5yr_avg,
                            'roa_ttm': roa_ttm, 'roa_mrfy': roa_mrfy, 'roa_5yr_avg': roa_5yr_avg,
                            'gpr_mrfy': gpr_mrfy, 'pm_ttm': pm_ttm, 'cr_mrq': cr_mrq, 'cr_mrfy': cr_mrfy, 
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

    div_ann = try_it('Dividend', 'data')
    div_y_mrfy = try_it('Dividend yield', 'metrics')
    
    # DataFrame will be added to company object via div_dfs list
    df_div = pd.DataFrame({'div_ann': div_ann, 'div_y_mrfy': div_y_mrfy}, index=['Dividend Metrics']).T
    
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
        twits_perc = 'n/a'
        
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
    enviro = try_it('Environment score', 'esg')
    govern = try_it('Governance score', 'esg')
    social = try_it('Social score', 'esg')
    total_esg = try_it('Total esg', 'esg')
    esg_perf = try_it('Esg performance', 'esg')
    
    df_esg = pd.DataFrame({'enviro': enviro, 'govern': govern, 'social': social,
                           'total_esg': total_esg, 'esg_perf': esg_perf}, index=['ESG']).T

#*#################################################################################    
############## *** Creating Company objects: *** #################################  
#*#################################################################################

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

    elif slot == 5:
        c5 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c5)

    elif slot == 6:
        c6 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c6)

    elif slot == 7:
        c7 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c7)

    elif slot == 8:
        c8 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c8)

    elif slot == 9:
        c9 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c9)

    elif slot == 10:
        c10 = Company(df_basic, df_value, df_mgmt, df_ins, div_dfs, df_pub_sent, news_dfs, analyst_data, df_esg)
        company_list.append(c10)

# Creating PeerGroup object
peer_group = PeerGroup(company_list=company_list)

# Pulling in the data for PeerGroup object
peer_group.set_all_data()

# Fixes improper calculation set by set_all_data() for peer_group tca_div_tld
peer_group.df_value.loc['tca_div_tld'][0] = peer_group.df_value.loc['tca_mrfy'][0] / peer_group.df_value.loc['tld_mrfy'][0]

# For each stock, calculates scores for each category using company history and peer averages
for slot in range(0, len(company_list)):
    big_phat_whiff(company_list[slot], peer_group)