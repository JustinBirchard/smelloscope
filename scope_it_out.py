# scope_it_out.py
#* Smelloscope Version 1.3
#* file last updated 12/2/22
"""Returns a dict of Company objects and a PeerGroup object. 
   These are pulled into the Smelloscope lab by importing * 
   from scope_it_out

   scope_it_out takes user supplied list from stocklist.py 
   and pulls in stock data via OpenBB. Each stock becomes a 
   Company object and is populated with data. 

   A PeerGroup object will also be created. PeerGroup is a subclass 
   of Company and its methods will be used to pull in every metric 
   from every stock and then calculate an average value for 
   each metric.

   After all data has been gathered, the sniffer.py gives each Company 
   object a big_phat_whiff. 
   
   After all companies are sniffed, each Company's score card and all 
   other features will be accessable via the TheSmelloscope lab.

Returns:
    list: companies containing Company class objects
    object: PeerGroup subclass object
"""

print('Preparing olfactory sensory neurons...\n')

import math
import pandas as pd
from IPython.display import display
import io, logging
from contextlib import redirect_stdout, redirect_stderr

#Creating log file and IO object
logging.basicConfig(filename='log.log', level=logging.INFO)
f = io.StringIO()

#Redirecting api messages from obb to log file
with redirect_stdout(f), redirect_stderr(f):
    from openbb_terminal.sdk import openbb as obb      
logging.info(f.getvalue())

import objective_lens
from sniffer import big_phat_whiff
from company import Company, PeerGroup

#&# BEGIN: FUNCTION DEFINITIONS ***************************************
def show_total_scores(companies):
    """Show total scores for all Company objects.
    Args:
        companies (dict): dictionary of Company objects
    """
    for ticker in clean_stocks:
        print(companies[ticker].df_basic.loc['name'][0])
        print(str(companies[ticker].score_card['grand_total']))
        print('')
        print('')

def show_scorecards(companies):
    """Show detailed scorecards for each Company object.
    Args:
        companies (dict): dictionary of Company objects
    """
    for ticker in clean_stocks:
        print(companies[ticker].df_basic.loc['name'][0])
        print('TOTAL SCORE=  ' + str(companies[ticker].score_card['grand_total']))
        print('')
        display(companies[ticker].score_card['value'].T)
        display(companies[ticker].score_card['mgmt'].T)
        display(companies[ticker].score_card['ins'].T)
        display(companies[ticker].score_card['div'].T)
        display(companies[ticker].score_card['pub_sent'].T)
        display(companies[ticker].score_card['analyst_data'].T)
        display(companies[ticker].score_card['esg'].T)
        print('')
        print('')
        print('')

def show_metrics(companies):
    """Show detailed metrics for each Company object.
    Args:
        companies (dict): dictionary of Company objects
    """
    for ticker in clean_stocks:
        companies[ticker].display_dfs()

def export_metrics(companies):
    """Export Company metrics into a primitive Excel file.
       One file is created per Company.
       Files are saved in root folder.
    Args:
        companies (dict): dictionary of Company objects
    """
    for company in companies.values():
        company.data_to_excel()
        print(f"{company.df_basic.loc['ticker'][0]} metrics saved as Excel file.")


def p2f(str_perc):
    """Converts str representing percentage to a float. 
       Example: '10%' becomes 0.1
    Args:
        str_perc (str): str representation of a percentage

    Returns:
        float: converted string to float
    """
    return float(str_perc.strip('%'))/100

def try_it(string, calltype, avg=False, p2f_bool=False, perf=False):
    """For error handling when making calls to OpenBB.
    Args:
        string (str): Key to call the desired metric
        calltype (str): One of- 'data', 'metrics', 'esg', or 'ratios'
        avg (bool, optional): True returns 5yr_avg metrics. Defaults to False.
        p2f_bool (bool, optional): True converts str percentage to float. Default False.
        perf (bool, optional): True returns str value for ESG metric. Default False.

    Returns:
        str or float: depending on args and conditions
    """
    
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

    elif calltype == 'esg' and perf == False:    
        try:
            if isinstance(df_full_esg.loc[string][0], float):
                return df_full_esg.loc[string][0]
            else:
                return 'n/a'
            
        except KeyError:
            return 'n/a'

        except AttributeError:
            return 'n/a'

    elif calltype == 'esg' and perf == True:    
        try:
            if isinstance(df_full_esg.loc[string][0], str):
                return df_full_esg.loc[string][0]
            else:
                return 'n/a'
            
        except KeyError:
            return 'n/a'
        except AttributeError:
            return 'n/a'

    elif calltype == 'ratios' and avg is True:
        try:
            return df_ratios.loc[string]['5yr Avg']
            
        except KeyError:
            return 'n/a'
        except AttributeError:
            return 'n/a'       

    elif calltype == 'ratios' and avg is False:
        try:
            return df_ratios.loc[string][0]
            
        except KeyError:
            return 'n/a'
        except AttributeError:
            return 'n/a'   
#&# END: Function definitions *****************************************

#! BEGIN MAIN LOOP ***************************************************

clean_stocks = objective_lens.group_selection()
print('Angling the scope towards an interesting cluster...\n\n')

# Company objects will be added to this dict later
companies = {}

for stock in clean_stocks:

    # Running test because stocks that are younger than 5 years old 
    # are currently not available via FMP api
    fmp_msg1 = f'Dag nabbit! {stock} is not available via FMP api.'
    fmp_msg2 = ' Probably because it is not 5 years old. '
    fmp_msg3 = 'Please remove it from stocklist.py and try again. '
    fmp_msg4 = f'You can add {stock} to young_stocks set'
    fmp_msg5 = ' in stocklist.py to avoid this error in the future.'

    try:
        df_metrics = obb.stocks.fa.metrics(stock)

    except ValueError:
        print(fmp_msg1 + fmp_msg2 + fmp_msg3 + fmp_msg4 + fmp_msg5)

    # rare case for when fmp's api returns an empty list                                                                          
    if not isinstance(df_metrics, pd.DataFrame):
        raise TypeError(fmp_msg1 + fmp_msg2 + fmp_msg3 + fmp_msg4 + fmp_msg5)

#& BEGIN cleaning & refining df_metrics ************************************
    # Where possible, converting strings to floats in df_metrics    
    float_error_set = set() 
    for column in df_metrics.columns:       
        for row in df_metrics.index:         
            try:
                df_metrics[column][row] = float(df_metrics[column][row])
                
            except ValueError: # catching row names of those that cannot convert
                
                try: # for if FMP returns value that has "K" listed at end of str
                    get_rid_of_k = df_metrics[column][row].strip('K')
                    df_metrics[column][row] = float(get_rid_of_k.strip())

                except ValueError:
                    float_error_set.add(row)

    # Dropping all metrics that cannot be converted to float   
    df_metrics = df_metrics.drop(index= float_error_set)
    
    # Creating new column and calculating 5 year average for each metric
    df_metrics['5yr Avg'] = df_metrics.mean(axis=1)

    print(f'Getting a whiff of {obb.stocks.fa.profile(stock).loc["companyName"][0]}')

#&# END cleaning/refining df_metrics ************************************************
#&# BEGIN cleaning/refining df_ratios ***********************************************

    df_ratios = obb.stocks.fa.ratios(stock)

    # Where possible, converting strings to floats in df_ratios    
    float_error_set = set() 
    for column in df_ratios.columns:   
        for row in df_ratios.index:          
            try:
                df_ratios[column][row] = float(df_ratios[column][row])
                
            except ValueError:
                    float_error_set.add(row)
                   
    # Removing any row from df_ratios where values cannot be converted to float
    df_ratios = df_ratios.drop(index= float_error_set)
    
    # Creating new column that will hold the average of each row
    df_ratios['5yr Avg'] = df_ratios.mean(axis=1)

#&# END refining df_ratios ****************************************************

    # Testing to see if SEC data is available
    sec_analysis = ['temp']
    try:
        sec_analysis[0] = obb.stocks.fa.analysis(stock)
        if isinstance(sec_analysis[0], list):
            print(f"SEC data was not available for {stock}. No big deal, moving on.\n\n")
            sec_analysis[0] = 'n/a'

        elif sec_analysis[0].empty:
            sec_analysis[0] = 'n/a'

    except IndexError:
        print(f"SEC data was not available for {stock}. No big deal, moving on.\n\n")
        sec_analysis[0] = 'n/a'

    # getting Stock Twits sentiment data as a tuple:
    tuple_twits = obb.stocks.ba.bullbear(stock)
    
    # getting analyst recommendation totals by type over last 3 months
    df_rot = obb.stocks.dd.rot(stock).T[0]

    # getting ESG data
    df_full_esg = obb.stocks.fa.sust(stock)
    if df_full_esg.empty:
        df_esg = 'n/a'   
        df_full_esg = 'n/a'

#& BEGIN Creating variables for readability & grouping values into DataFrames & Sequences
############## *** BASIC DETAILS DATAFRAME *** ##############
    name = obb.stocks.fa.profile(stock).loc['companyName'][0]
    ticker = stock
    sector = obb.stocks.fa.profile(stock).loc['sector'][0]
    industry = obb.stocks.fa.profile(stock).loc['industry'][0]
    cap = obb.stocks.fa.quote(stock).loc['Market cap'][0]
    price = obb.stocks.fa.quote(stock).loc['Price'][0]
    
    # DataFrame will be added to Company object
    df_basic = pd.DataFrame({'name': name, 'ticker': ticker, 'sector': sector,
                             'industry': industry, 'cap': cap, 'price': price}, 
                              index=['Basic Details']).T
    
############## *** VALUE METRICS DATAFRAME *** ##############    
    # We'll keep knocking on Yahoo's door if they don't give what we need
    yahoo_success = 'no'
    while yahoo_success == 'no':
        try:
            tca_mrfy = obb.stocks.fa.balance(stock).loc['Total current assets'][0]
            yahoo_success = 'yes'

        except AttributeError:
            print('Yahoo error. Trying again.')

        except KeyError:
            print('Yahoo error. Trying again.')

    yahoo_success = 'no'
    while yahoo_success == 'no':
    # Cases for if the company has no debt
        try:
            if math.isnan(obb.stocks.fa.balance(stock).loc['Long-term debt'][0]) is True:
                tld_mrfy = 0 
                yahoo_success = 'yes'
            
            elif obb.stocks.fa.balance(stock).loc['Long-term debt'][0] is None:
                tld_mrfy = 0
                yahoo_success = 'yes' 
            
            else:  
                tld_mrfy = obb.stocks.fa.balance(stock).loc['Long-term debt'][0]
                yahoo_success = 'yes'

            if tld_mrfy == 0:
                tca_div_tld = tca_mrfy
            else:
                tca_div_tld = (tca_mrfy / tld_mrfy).round(4)

        except KeyError:
            tld_mrfy = 0
            tca_div_tld = tca_mrfy
            yahoo_success = 'yes'

        except AttributeError:
            print('Yahoo is having issues, trying again...')
 
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

    graham_mrfy = try_it('Graham number', 'metrics')
    peg = try_it('PEG', 'data')

    # DataFrame will be added to company object   
    df_value = pd.DataFrame({'tca_mrfy': tca_mrfy, 'tld_mrfy': tld_mrfy, 'tca_div_tld': tca_div_tld,
                             'ptb_mrq': ptb_mrq, 'ptb_mrfy': ptb_mrfy, 'ptb_5yr_avg': ptb_5yr_avg, 
                             'bvps_mrq': bvps_mrq, 'bvps_mrfy': bvps_mrfy, 'bvps_5yr_avg': bvps_5yr_avg, 
                             'pe_ttm': pe_ttm, 'pe_mrfy': pe_mrfy, 'pe_5yr_avg': pe_5yr_avg, 
                             'pfcf_ttm': pfcf_ttm, 'pfcf_mrfy': pfcf_mrfy, 'pfcf_5yr_avg': pfcf_5yr_avg, 
                             'pts_ttm': pts_ttm, 'pts_mrfy': pts_mrfy, 'pts_5yr_avg': pts_5yr_avg, 
                             'graham_mrfy': graham_mrfy, 'peg': peg}, 
                              index=['Value Metrics'])

    df_value = df_value.round(4)
    df_value = df_value.T
        
############## *** MANAGEMENT METRICS DATAFRAME *** ##############
    roa_ttm = try_it('ROA', 'data', p2f_bool=True)
    roa_mrfy = try_it('Return on tangible assets', 'metrics')
    roa_5yr_avg = try_it('Return on tangible assets', 'metrics', avg=True)

    roe_ttm = try_it('ROE', 'data', p2f_bool=True)
    roe_mrfy = try_it('Roe', 'metrics')
    roe_5yr_avg = try_it('Roe', 'metrics', avg=True)

    npm_mrfy = try_it('Net profit margin', 'ratios')
    npm_5yr_avg = try_it('Net profit margin', 'ratios', avg=True)

    opm_mrfy = try_it('Operating profit margin', 'ratios')
    opm_5yr_avg = try_it('Operating profit margin', 'ratios', avg=True)

    gpm_mrfy = try_it('Gross profit margin', 'ratios')
    gpm_5yr_avg = try_it('Gross profit margin', 'ratios', avg=True)

    cr_mrq = try_it('Current Ratio', 'data')
    cr_mrfy = df_metrics.loc['Current ratio'][0]
    cr_5yr_avg = df_metrics.loc['Current ratio']['5yr Avg']
    
    dte_mrq = try_it('LT Debt/Eq', 'data')
    dte_ttm = try_it('Debt to equity', 'metrics')
    dte_5yr_avg = try_it('Debt to equity', 'metrics', avg=True)
    
    # DataFrame will be added to company object    
    df_mgmt = pd.DataFrame({'roa_ttm': roa_ttm, 'roa_mrfy': roa_mrfy, 'roa_5yr_avg': roa_5yr_avg,
                            'roe_ttm': roe_ttm, 'roe_mrfy': roe_mrfy, 'roe_5yr_avg': roe_5yr_avg,
                            'npm_mrfy': npm_mrfy, 'npm_5yr_avg': npm_5yr_avg,
                            'opm_mrfy': opm_mrfy, 'opm_5yr_avg': opm_5yr_avg,
                            'gpm_mrfy': gpm_mrfy, 'gpm_5yr_avg': gpm_5yr_avg,                         
                            'cr_mrq': cr_mrq, 'cr_mrfy': cr_mrfy, 'cr_5yr_avg': cr_5yr_avg, 
                            'dte_mrq': dte_mrq, 'dte_ttm': dte_ttm, 'dte_5yr_avg': dte_5yr_avg},
                            index=['Management Metrics'])

    df_mgmt = df_mgmt.round(4)
    df_mgmt = df_mgmt.T
        
############## *** INSIDER & INSTITUION DATAFRAME *** ##############
    io = try_it('Insider Own', 'data', p2f_bool=True)
    it = try_it('Insider Trans', 'data', p2f_bool=True)

    inst_o = try_it('Inst Own', 'data', p2f_bool=True)
    inst_t = try_it('Inst Trans', 'data', p2f_bool=True)

    # DataFrame will be added to company object
    df_ins = pd.DataFrame({'io': io, 'it': it, 'inst_o': inst_o, 
                           'inst_t': inst_t}, index=['Insider & Insitution Data'])

    df_ins = df_ins.round(4)
    df_ins = df_ins.T
    
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
    if len(sent_list) < 1:
        news_sent = 'n/a'

    else:
        news_sent = sum(sent_list)/len(sent_list)
        
    shrt_int = obb.stocks.fa.data(stock).loc['Short Float / Ratio'][0][:7]
    shrt_int = shrt_int.strip('/')
    shrt_int = shrt_int.strip()
    shrt_int = p2f(shrt_int)
    
    # DataFrame will be added to company object
    df_pub_sent = pd.DataFrame({'twits_perc': twits_perc, 'shrt_int': shrt_int, 
                                'news_sent': news_sent}, index=['Public Sentiment Metrics'])

    df_pub_sent = df_pub_sent.round(4)
    df_pub_sent = df_pub_sent.T

############## *** COMPANY, SECTOR, & INDUSTRY NEWS *** ##############
    
    df_com_news = obb.news(f"{name} {ticker}", sort='published').head(20)
    df_sec_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Sector News'])
    df_ind_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Industry News'])

    # List will be added to company object
    news_dfs = [df_com_news, df_sec_news, df_ind_news]
    
############## *** ANALYST RATINGS *** ##############
# Note there are 2 DataFrames and one variable here: df_rating_30d, df_rot_3mo, wb_score
  
    # Pairing df_rating down to last 30 days and converting returned Series back to DataFrame
    df_rating_30d = obb.stocks.dd.rating(stock).T.loc['Rating'].head(30).to_frame()
    
    # DataFrame will be added to company object
    df_rot_3mo = pd.DataFrame({'Strong Buy': df_rot['strongBuy'], 
                               'Buy': df_rot['buy'], 
                               'Hold': df_rot['hold'], 
                               'Sell': df_rot['sell'], 
                               'Strong Sell': df_rot['strongSell']
                               }, index=['Last 3mo']).T

    # Warren Buffet Investing Score. Suppressing API output
    with redirect_stdout(f), redirect_stderr(f): 
        wb_score = obb.stocks.fa.score(stock)
        if wb_score is None:
            wb_score = 'n/a'
        
        if not isinstance(wb_score, str):
            wb_score = wb_score.round(4)
        
    # Logging the API output in log.log    
    logging.info(f.getvalue())

    fwd_pe = try_it('Forward P/E', 'data')

    # Creating list that holds Analyst data, will be added to Company object
    analyst_data = [df_rating_30d, df_rot_3mo, wb_score, fwd_pe]
    
############## *** ESG RATINGS *** ##############
    enviro = try_it('Environment score', 'esg')
    govern = try_it('Governance score', 'esg')
    social = try_it('Social score', 'esg')
    total_esg = try_it('Total esg', 'esg')
    esg_perf = try_it('Esg performance', 'esg', perf=True)
    
    df_esg = pd.DataFrame({'enviro': enviro, 'govern': govern, 
                           'social': social, 'total_esg': total_esg, 
                           'esg_perf': esg_perf}, index=['ESG'])

    df_esg = df_esg.round(4)
    df_esg = df_esg.T
#&# END Creating variables for readability & grouping values into DataFrames & Sequences

    # Adding new key (stock ticker) and value (Company object) to companies
    companies[ticker] = Company(df_basic, df_value, df_mgmt, 
                                df_ins, div_dfs, df_pub_sent,
                                news_dfs, analyst_data, df_esg,
                                df_full_esg, sec_analysis)

    print(f'{ticker} has been sniffed.\n')
#! END MAIN LOOP ***************************************************

# Creating PeerGroup object
peer_group = PeerGroup(companies=companies)

# Primary stock is needed for peer_group methods
primary_stock = clean_stocks[0]

# Pulling in the data and calculating averages for PeerGroup object
peer_group.set_avg_values(primary_stock)

# Fixes improper calculation set by set_all_data() for peer_group tca_div_tld
peer_tca = peer_group.df_value.loc['tca_mrfy'][0]
peer_tld = peer_group.df_value.loc['tld_mrfy'][0]
peer_group.df_value.loc['tca_div_tld'][0] = round((peer_tca / peer_tld), 4)

# For each stock, calculates scores for each category
for ticker in clean_stocks:
        big_phat_whiff(companies[ticker], peer_group)

# Pulls in data for the PeerGroup scoring dictionaries
peer_group.set_scoring_data(clean_stocks)

print('STOCKS ARE SMELT AND SCORES ARE DEALT!')