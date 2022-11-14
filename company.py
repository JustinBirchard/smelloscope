# company.py
"""Company class and PeerGroup subclass definitions and methods.
"""
#* Version 0.9.9.5
#* last updated 11/13/22

from stocklist import stocks
from copy import deepcopy
from openbb_terminal.api import openbb as obb
import pandas as pd
from dataclasses import dataclass, field
from IPython.display import display

# Setting display options for viewing dataframes in Lab
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Retrieving the first stock in stocks and using as the primary stock
primary_stock = stocks[0]

def find_X_best_scores(list_of_tuples, X):
    """Iterates thru given list of tuples X times. 
       In every iteration, finds max of 2nd element, 
       adds tuple to final_list_of_tuples, and removes 
       it from list_of_tuples before iterating again. 

    Args:
        list_of_tuples (list): list of tuples, where tuple is ticker & score
        X (int): How many top scores to retreive from each category

    Returns:
        list: list of tuples containing top scores for the category
    """

    final_list_of_tuples = [] # will hold final results

    # looping through list X times
    for i in range(0, X):
        maximum = ('', 0)
         
        # finding the max score in current version of alist
        for element in range(len(list_of_tuples)):    
            if list_of_tuples[element][1] > maximum[1]:
                maximum = list_of_tuples[element];
                 
        # Removing value that was the max score from alist before next iteration
        list_of_tuples.remove(maximum);
        
        # Appending the tuple set that was the max score to final_list
        final_list_of_tuples.append(maximum)
         
    return final_list_of_tuples

# DataFrames below serve as templates for company score cards
# They'll be deep-copied into Company objects
scores_value = pd.DataFrame({'value': {'v01': None, 'v02': None, 
                                       'v03': None, 'v04': None, 
                                       'v05': None, 'v06': None, 
                                       'v07': None, 'v08': None, 
                                       'v09': None, 'v10': None, 
                                       'v11': None, 'v12': None,
                                       'v13': None}})

scores_mgmt = pd.DataFrame({'mgmt': {'m01': None, 'm02': None,
                                     'm03': None, 'm04': None, 
                                     'm05': None, 'm06': None, 
                                     'm07': None, 'm08': None, 
                                     'm09': None, 'm10': None,
                                     'm11': None, 'm12': None,
                                     'm13': None}})

scores_ins = pd.DataFrame({'ins': {'i01': None, 'i02': None, 
                                   'i03': None, 'i04': None}})

scores_div = pd.DataFrame({'div': {'d01': None, 'd02': None, 
                                   'd03': None, 'd04': None}})

scores_pub_sent = pd.DataFrame({'pub_sent': {'p01': None, 'p02': None, 
                                             'p03': None, 'p04': None,
                                             'p05': None, 'p06': None}})

scores_analyst_data = pd.DataFrame({'analyst_data': {'a01': None, 'a02': None,
                                                     'a03': None, 'a04': None,
                                                     'a05': None, 'a06': None}})

scores_esg = pd.DataFrame({'esg': {'e01': None, 'e02': None,
                                   'e03': None, 'e04': None,
                                   'e05': None}})

@dataclass
class Company:
    """Company objects hold a variety of metrics and data.
       Each stock in stocklist.py will become a Company object.
       Methods are meant to be called in TheSmelloscope lab.
    """
    df_basic: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(6,1), basic company details
    df_value: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(18,1), value metrics
    df_mgmt: pd.DataFrame = field(default_factory=pd.DataFrame)# shape=(14,1), management metrics
    df_ins: pd.DataFrame = field(default_factory=pd.DataFrame)# shape=(4,1), insider & instituion data
    div_dfs: list = field(default_factory=list, repr=False) # holds 2 DataFrames containing dividend data
    df_pub_sent: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(3,1), public sentiment data
    news_dfs: list = field(default_factory=list, repr=False) # holds 3 DFs containing Company, Sector, & Industry news
    analyst_data: list = field(default_factory=list, repr=False) # holds 2 DataFrames containing Analyst ratingsmetrics
    df_esg: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(5,1), holds ESG data & metrics
    sec_analysis: list = field(default_factory=list, repr=False) # will hold SEC sentiment analysis dataframe or 'n/a'
    score_card: dict = field(default_factory=lambda: {'value': deepcopy(scores_value), 
                                                      'mgmt': deepcopy(scores_mgmt),
                                                      'ins': deepcopy(scores_ins), 
                                                      'div': deepcopy(scores_div),
                                                      'pub_sent': deepcopy(scores_pub_sent),
                                                      'analyst_data': deepcopy(scores_analyst_data),
                                                      'esg': deepcopy(scores_esg),
                                                      'grand_total': None}) # dict that hold score cards and grand_total

    def show_sec_analysis(self):
        if isinstance(self.sec_analysis[0], str):
            print(f"SEC analysis was not available for {self.df_basic.loc['name'][0]} at this time.")

        else:
            for row in range(0, len(self.sec_analysis[0])):
                print('Category: ' + self.sec_analysis[0].loc[row]['Group'])
                print('Good News?  ' + str(self.sec_analysis[0].loc[row]['Good']) + '\n')
                print('Sentence analyzed: \n' + self.sec_analysis[0].loc[row]['Sentence'] + ('\n' * 3))

    def show_news(self):
        """Show title and link for company related news articles.
        """
        for title, link in zip(self.news_dfs[0].T.loc['title'], self.news_dfs[0].T.loc['link']):
            print(title)
            print(link + '\n')       

    def data_to_excel(self):
        """Combine selected data into a new dataframe and output to excel file.
        """
        group = [self.df_basic, self.df_value, self.df_mgmt, 
                self.df_ins, self.div_dfs[0], self.df_pub_sent, self.analyst_data[1]]

        combined_dict = {}

        for dataframe in group:
            for row in dataframe.index:
                combined_dict[row] = dataframe.loc[row][0]

        # Creating df out of dict, transposing, exporting to excel. Filename will output to root folder with filename: [TICKER].xlsx
        pd.DataFrame(combined_dict, index=['Values']).T.to_excel(self.df_basic.loc['ticker'][0] + '.xlsx')

    def display_dfs(self):
        """View selected dataframes in Jupyter Lab or IPython
        """
        group = [self.df_basic, self.df_value, self.df_mgmt, 
                self.df_ins, self.div_dfs[0], self.df_pub_sent, 
                self.analyst_data[0], self.analyst_data[1], self.df_esg]

        for df in group:
            display(df)

    def metric_names(self, data_type):
        """Prints the names of the metrics in Company
           dataframes.  

        Args:
            data_type (str): nickname of the dataframe
        """
        if data_type == 'basic':
            print([x for x in self.df_basic.index])

        elif data_type == 'value':
            print([x for x in self.df_value.index])

        elif data_type == 'mgmt':
            print([x for x in self.df_mgmt.index])

        elif data_type == 'ins':
            print([x for x in self.df_ins.index])

        elif data_type == 'div':
            print([x for x in self.div_dfs[0].index])

        elif data_type == 'pub_sent':
            print([x for x in self.df_pub_sent.index])

        elif data_type == 'analyst':
            print(['analyst'])

        elif data_type == 'esg':
            print([x for x in self.df_esg.index])

    def access_data(self, data_type, value_name):

        if data_type == 'basic' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'basic':
            print(self.df_basic.loc['name'][0])
            print(str(self.df_basic.loc[value_name][0]) + '\n')

        elif data_type == 'value' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'value':
            print(self.df_basic.loc['name'][0])
            print(str(self.df_value.loc[value_name][0]) + '\n')

        elif data_type == 'mgmt' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'mgmt':
            print(self.df_basic.loc['name'][0])
            print(str(self.df_mgmt.loc[value_name][0]) + '\n')

        elif data_type == 'ins' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'ins':
            print(self.df_basic.loc['name'][0])
            print(str(self.df_ins.loc[value_name][0]) + '\n')

        elif data_type == 'div' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'div':
            print(self.df_basic.loc['name'][0])
            print(str(self.div_dfs[0].loc[value_name][0]) + '\n')

        elif data_type == 'pub_sent' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'pub_sent':
            print(self.df_basic.loc['name'][0])
            print(str(self.df_pub_sent.loc[value_name][0]) + '\n')

        elif data_type == 'analyst' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'analyst' and value_name == 'analyst':
            print(self.df_basic.loc['name'][0] + '\n')
            print(f'Warren Buffet Score = {self.analyst_data[2]}')
            print(f'Forward P/E = {self.analyst_data[3]}')
            display(self.analyst_data[1])
            print('\n')

        elif data_type == 'esg' and value_name == 'options':
            self.metric_names(data_type)

        elif data_type == 'esg':
            print(self.df_basic.loc['name'][0])
            print(str(self.df_esg.loc[value_name][0]) + '\n')

@dataclass
class PeerGroup(Company):
    """Subclass PeerGroup for creating PeerGroup objects

    Args:
        Company (Object): Class Company Object
    """
    
    companies: dict = field(default_factory=dict) # 1 or more Company objects
    peer_score_totals: dict = field(default_factory=lambda: {}) # company score totals for each category
    category_totals: dict = field(default_factory=lambda: {'grand_total': [], 'vTotal': [], 'mTotal': [], 
                                                           'iTotal': [], 'dTotal': [], 'pTotal': [], 
                                                           'aTotal': [], 'eTotal': []}) # category totals by comapny
    top_scores: dict = field(default_factory=lambda: {}) # top company scores for each category
    winners: dict = field(default_factory=lambda: {}) # the top scorers of the PeerGroup

    def set_scoring_data(self):
        """Populates scores for the three PeerGroup score dictionaries.
           And also the winners dictionary.
        """
        self.set_peer_score_totals()
        self.set_cat_totals()
        self.set_top_scores()
        self.set_winners()

    def set_peer_score_totals(self):
        """Populates the peer_score_totals dictionary which contains
           grand total and category totals for every company.
           CAN ONLY RUN AFTER:
           set_avg_values
        """
        for tick in stocks:
            grand_total = self.companies[tick].score_card['grand_total']
            vTotal = self.companies[tick].score_card['value'].loc['vTotal'][0]
            mTotal = self.companies[tick].score_card['mgmt'].loc['mTotal'][0]
            iTotal = self.companies[tick].score_card['ins'].loc['iTotal'][0]
            dTotal = self.companies[tick].score_card['div'].loc['dTotal'][0]
            pTotal = self.companies[tick].score_card['pub_sent'].loc['pTotal'][0]
            aTotal = self.companies[tick].score_card['analyst_data'].loc['aTotal'][0]
            eTotal = self.companies[tick].score_card['esg'].loc['eTotal'][0]
                     
            self.peer_score_totals[tick] = {'grand_total': grand_total, 'vTotal': vTotal, 
                                                 'mTotal': mTotal, 'iTotal': iTotal, 
                                                 'dTotal': dTotal, 'pTotal': pTotal, 
                                                 'aTotal': aTotal, 'eTotal': eTotal}
                                                 
    def set_cat_totals(self):
        """Populates the category_totals dictionary which holds 
           total scores for each company grouped by category.
           CAN ONLY RUN AFTER:
           set_peer_score_totals
        """
        for tick in self.companies.keys():
            for cat in self.category_totals.keys():
                self.category_totals[cat].append((tick, self.peer_score_totals[tick][cat]))

    def set_top_scores(self):
        """Finds the top X scores for every category and adds
           them to the top_scores dictionary.
           To accomplish this, the find_X_best_scores function
           is used and arg X is determined programatically based 
           on how many peers are in group.
           CAN ONLY RUN AFTER:
           set_peer_score_totals
           set_cat_totals
        """
        cat_totals_copy = deepcopy(self.category_totals)
        for cat in cat_totals_copy.keys():
            if len(self.peer_score_totals.keys()) > 5:
                self.top_scores[cat] = find_X_best_scores(cat_totals_copy[cat], 5)
                
            elif len(self.peer_score_totals.keys()) > 3:
                self.top_scores[cat] = find_X_best_scores(cat_totals_copy[cat], 3)
                
            elif len(self.peer_score_totals.keys()) >= 2:
                self.top_scores[cat] = find_X_best_scores(cat_totals_copy[cat], 1)

    def set_winners(self):
        """Creates dict out of the top 3-5 winners from the peer group.
           Number of winners will depend on total tickers in stocks list.
           CAN ONLY RUN AFTER:
           set_peer_score_totals()
           set_cat_totals()
           set_top_scores()
        """
        for winner in self.top_scores['grand_total']:
            self.winners[winner[0]] = self.peer_score_totals[winner[0]]

    def set_avg_values(self):
        self.set_df_basic()
        self.set_df_value()
        self.set_df_mgmt()
        self.set_df_ins()
        self.set_div_dfs()
        self.set_df_pub_sent()
        self.set_news_dfs()
        self.set_analyst_data()
        self.set_df_esg()
        self.set_sec_analysis()

    def set_df_basic(self):
        """Set self.df_basic values"""

        self.df_basic['name'] = self.companies[primary_stock].df_basic.loc['ticker'] + ' Peer Group Avg'
        self.df_basic['ticker'] = self.companies[primary_stock].df_basic.loc['ticker'] + ' Peer Avg'
        self.df_basic['sector'] = self.companies[primary_stock].df_basic.loc['sector']
        self.df_basic['industry'] = self.companies[primary_stock].df_basic.loc['industry']
        self.df_basic['cap'] = 'temp n/a'
        self.df_basic['price'] = 'temp n/a'

        self.df_basic = self.df_basic.T

    def set_df_value(self):
        """Set self.df_value by calculating average value for each metric in the 
           Value category and assigning it to PeerGroup object.

           Metrics that are discarded from calculation if:
           1) They are < 0 or > 50
           2) They have 'n/a' value
        """

        result_list = []

        for metric in self.companies[primary_stock].df_value.index:
            for company in self.companies.values():
                value = company.df_value.loc[metric][0]

                if metric not in ['tca_mrfy', 'tld_mrfy', 'tca_div_tld'] and value != 'n/a':
                    if value >= 0 and value <= 50: 
                        result_list.append(company.df_value.loc[metric])

                elif metric == 'tca_mrfy' or metric == 'tld_mrfy' or metric == 'tca_div_tld':
                    result_list.append(company.df_value.loc[metric])

            # discarding series objects that hold string values
            result_list = [series for series in result_list if not isinstance(series[0], str)]
            
            sum = 0
            for value in result_list:
                sum += value
            
            try:
                self.df_value[metric] = sum / len(result_list)

            except ZeroDivisionError:
                self.df_value[metric] = 'n/a'


            result_list.clear()

        self.df_value = self.df_value.round(4)
        self.df_value = self.df_value.T

    def set_df_mgmt(self):
        """Set self.df_mgt by calculating average value for each metric 
           in the Management category and assigning it to PeerGroup object.

           Percentage based values are discarded from calculation if 
           they are < -1 or > 1
           
           Ratio based values are discarded if they are < 0 or >= 8
        """

        result_list = []

        for metric in self.companies[primary_stock].df_mgmt.index:
            for company in self.companies.values():
                value = company.df_mgmt.loc[metric][0]
                special_keys = ['cr_mrq', 'cr_mrfy', 'cr_5yr_avg', 
                                'dte_mrq', 'dte_ttm', 'dte_5yr_avg']

                if metric not in special_keys and value != 'n/a':
                    if value >= -1 and value <= 1: 
                        result_list.append(company.df_mgmt.loc[metric])

                elif metric in special_keys and value != 'n/a':
                    if value >= 0 and value <= 8: 
                        result_list.append(company.df_mgmt.loc[metric])
           
            result_list = [series for series in result_list if not isinstance(series[0], str)]

            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.df_mgmt[metric] = sum / len(result_list)

            else:
                self.df_mgmt[metric] = 'n/a'

            result_list.clear()

        self.df_mgmt = self.df_mgmt.round(4)
        self.df_mgmt = self.df_mgmt.T

    def set_df_ins(self):
        """Set self.df_ins by calculating average value for each metric 
           in the Management category and assigning it to PeerGroup object.
           'n/a' values are discarded
        """
        result_list = []

        for metric in self.companies[primary_stock].df_ins.index:
            for company in self.companies.values():
                result_list.append(company.df_ins.loc[metric])
            
            result_list = [series for series in result_list if not isinstance(series[0], str)]

            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.df_ins[metric] = sum / len(result_list)

            else:
                self.df_ins[metric] = 'n/a'

            result_list.clear()

        self.df_ins = self.df_ins.round(4)
        self.df_ins = self.df_ins.T

    def set_div_dfs(self):
        """Set self.div_dfs[0] and self.div_dfs[1] by calculating average value 
           for each applicable metric in the Dividend category and assigning it 
           to PeerGroup object.
           'n/a' values are discarded.
           self.div_dfs[0] will be set as 'n/a' as that dataframe is a 
           line-by-line dividend history report and doesn't makes sense for PeerGroup.
        """
        self.df_div = pd.DataFrame()
        self.df_div_his = pd.DataFrame({'Data N/A': 'n/a'}, index=[0]).T
        self.div_dfs.append(self.df_div)
        self.div_dfs.append(self.df_div_his)

        result_list = []

        for metric in self.companies[primary_stock].div_dfs[0].index:
            for company in self.companies.values():
                result_list.append(company.div_dfs[0].loc[metric])
            
            result_list = [series for series in result_list if not isinstance(series[0], str)]

            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.div_dfs[0][metric] = sum / len(result_list)

            else:
                self.div_dfs[0][metric] = 'n/a'

            result_list.clear()

        self.div_dfs[0] = self.div_dfs[0].round(4)
        self.div_dfs[0] = self.div_dfs[0].T

    def set_df_pub_sent(self):
        """Set self.df_pub_sent by calculating average value for each metric 
           in the Public Sentiment category and assigning it to PeerGroup object.
           'n/a' values are discarded
        """

        result_list = []

        for metric in self.companies[primary_stock].df_pub_sent.index:
            for company in self.companies.values():
                result_list.append(company.df_pub_sent.loc[metric])
            
            result_list = [series for series in result_list if not isinstance(series[0], str)]
            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.df_pub_sent[metric] = sum / len(result_list)

            else:
                self.df_pub_sent[metric] = 'n/a'

            result_list.clear()

        self.df_pub_sent = self.df_pub_sent.round(4)
        self.df_pub_sent = self.df_pub_sent.T

    def set_news_dfs(self):
        """Set self.news_dfs values. 
           self.news_dfs[0] will be set to 'n/a' as it is company specific.
        """

        df_com_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Company News'])
        df_sec_news = obb.common.news(self.companies[primary_stock].df_basic.loc['sector'][0] + 'Sector News Stock Market', sort='published').head(50)
        df_ind_news = obb.common.news(self.companies[primary_stock].df_basic.loc['industry'][0] + 'Industry News Stock Market', sort='published').head(50)

        self.news_dfs = [df_com_news, df_sec_news, df_ind_news]

    def set_analyst_data(self):
        """Set self.analyst_data values
           self.analyst_data[0] dataframe will be set with 'n/a' values as it 
           is a company spcefic data point.
        """
        df_rating_30d = pd.DataFrame({'Data N/A': 'n/a'}, index=['df_rating_30d']).T
        peer_df_rot_3mo = pd.DataFrame({'Strong Buy': 0, 'Buy': 0, 'Hold': 0, 'Sell': 0, 'Strong Sell': 0}, index=['Last 3mo']).T

        for company in self.companies.values():
            peer_df_rot_3mo += company.analyst_data[1]

        peer_df_rot_3mo = peer_df_rot_3mo / len(self.companies.keys())

        wb_score = ''
        fwd_pe = ''

        result_list = []
        # calaculating avg wb_score
        for company in self.companies.values():
            result_list.append(company.analyst_data[2])         
            result_list = [value for value in result_list if not isinstance(value, str)]
            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                wb_score = sum / len(result_list)

            else:
                wb_score = 'n/a'

        result_list.clear()

        # calaculating avg fwd_pe
        for company in self.companies.values():
            result_list.append(company.analyst_data[3])         
            result_list = [value for value in result_list if not isinstance(value, str)]
            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                fwd_pe = sum / len(result_list)

            else:
                fwd_pe = 'n/a'

        result_list.clear()

        if not isinstance(wb_score, str):
            wb_score = round(wb_score, 2)

        fwd_pe = round(fwd_pe, 2)

        self.analyst_data = [df_rating_30d, peer_df_rot_3mo, wb_score, fwd_pe]

    def set_df_esg(self):
        """Set self.df_esg by calculating average value for each metric 
           in the ESG category and assigning it to PeerGroup object.
           'n/a' values are discarded
        """
        result_list = []

        for metric in self.companies[primary_stock].df_esg.index:
            for company in self.companies.values():
                result_list.append(company.df_esg.loc[metric])

            result_list = [series for series in result_list if isinstance(series[0], float)]
            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.df_esg[metric] = sum / len(result_list)

            else:
                self.df_esg[metric] = 'n/a'

            result_list.clear()

        self.df_esg = self.df_esg.round(4)
        self.df_esg = self.df_esg.T

    def set_sec_analysis(self):
        self.sec_analysis = 'n/a'