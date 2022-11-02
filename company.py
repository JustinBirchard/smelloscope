# company.py
"""Company class and PeerGroup subclass definitions and methods.
"""
#* version 0.9.6
#* last updated 11/2/22

from copy import deepcopy
from openbb_terminal.api import openbb as obb
import pandas as pd
from dataclasses import dataclass, field
from IPython.display import display

# DataFrames below serve as templates for company score cards
# They'll be deep-copied into Company objects
scores_value = pd.DataFrame({'value': {'v01': None, 'v02': None, 
                                       'v03': None, 'v04': None, 
                                       'v05': None, 'v06': None, 
                                       'v07': None, 'v08': None, 
                                       'v09': None, 'v10': None, 
                                       'v11': None}})

scores_mgmt = pd.DataFrame({'mgmt': {'m01': None, 'm02': None,
                                     'm03': None, 'm04': None, 
                                     'm05': None, 'm06': None, 
                                     'm07': None, 'm08': None, 
                                     'm09': None, 'm10': None}})

scores_ins = pd.DataFrame({'ins': {'i01': None, 'i02': None, 
                                   'i03': None, 'i04': None}})

scores_div = pd.DataFrame({'div': {'d01': None, 'd02': None, 
                                   'd03': None, 'd04': None}})

scores_pub_sent = pd.DataFrame({'pub_sent': {'p01': None, 'p02': None, 
                                             'p03': None, 'p04': None,
                                             'p05': None, 'p06': None}})

scores_analyst_data = pd.DataFrame({'analyst_data': {'a01': None, 'a02': None,
                                                     'a03': None, 'a04': None,
                                                     'a05': None}})

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
    score_card: dict = field(default_factory=lambda: {'value': deepcopy(scores_value), 
                                                      'mgmt': deepcopy(scores_mgmt),
                                                      'ins': deepcopy(scores_ins), 
                                                      'div': deepcopy(scores_div),
                                                      'pub_sent': deepcopy(scores_pub_sent),
                                                      'analyst_data': deepcopy(scores_analyst_data),
                                                      'esg': deepcopy(scores_esg),
                                                      'grand_total': None}) # dict that hold score cards and grand_total



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

@dataclass
class PeerGroup(Company):
    """Subclass PeerGroup for creating PeerGroup objects

    Args:
        Company (Object): Class Company Object
    """
    
    companies: dict = field(default_factory=dict) # List of 1 or more Company objects

    def set_all_data(self):
        self.set_df_basic()
        self.set_df_value()
        self.set_df_mgmt()
        self.set_df_ins()
        self.set_div_dfs()
        self.set_df_pub_sent()
        self.set_news_dfs()
        self.set_analyst_data()
        self.set_df_esg()

    def set_df_basic(self):
        """Set self.df_basic values"""

        self.df_basic['name'] = self.companies['c1'].df_basic.loc['ticker'] + ' Peer Group Avg'
        self.df_basic['ticker'] = self.companies['c1'].df_basic.loc['ticker'] + ' Peer Avg'
        self.df_basic['sector'] = self.companies['c1'].df_basic.loc['sector']
        self.df_basic['industry'] = self.companies['c1'].df_basic.loc['industry']
        self.df_basic['cap'] = 'temp n/a'
        self.df_basic['price'] = 'temp n/a'

        self.df_basic = self.df_basic.T

    def set_df_value(self):
        """Set self.df_value values"""

        result_list = []

        for metric in self.companies['c1'].df_value.index:
            for company in self.companies.values():

                result_list.append(company.df_value.loc[metric])

            # discarding series objects that hold string values
            result_list = [series for series in result_list if not isinstance(series[0], str)]
            
            sum = 0
            for value in result_list:
                sum += value

            self.df_value[metric] = sum / len(result_list)
            result_list.clear()

        self.df_value = self.df_value.T

    def set_df_mgmt(self):
        """Set self.df_mgmt values"""

        result_list = []

        for metric in self.companies['c1'].df_mgmt.index:
            for company in self.companies.values():
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

        self.df_mgmt = self.df_mgmt.T

    def set_df_ins(self):
        """Set self.df_ins values"""

        result_list = []

        for metric in self.companies['c1'].df_ins.index:
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

        self.df_ins = self.df_ins.T

    def set_div_dfs(self):
        """Set self.div_dfs values"""
        self.df_div = pd.DataFrame()
        self.df_div_his = pd.DataFrame({'Data N/A': 'n/a'}, index=[0]).T
        self.div_dfs.append(self.df_div)
        self.div_dfs.append(self.df_div_his)

        result_list = []

        for metric in self.companies['c1'].div_dfs[0].index:
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

        self.div_dfs[0] = self.div_dfs[0].T

    def set_df_pub_sent(self):
        """Set self.df_pub_sent values"""

        result_list = []

        for metric in self.companies['c1'].df_pub_sent.index:
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

        self.df_pub_sent = self.df_pub_sent.T

    def set_news_dfs(self):
        """Set self.div_dfs values"""

        df_com_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Company News'])
        df_sec_news = obb.common.news(self.companies['c1'].df_basic.loc['sector'][0] + 'Sector News Stock Market', sort='published').head(50)
        df_ind_news = obb.common.news(self.companies['c1'].df_basic.loc['industry'][0] + 'Industry News Stock Market', sort='published').head(50)

        self.news_dfs = [df_com_news, df_sec_news, df_ind_news]

    def set_analyst_data(self):
        df_rating_30d = pd.DataFrame({'Data N/A': 'n/a'}, index=['df_rating_30d']).T
        peer_df_rot_3mo = pd.DataFrame({'Strong Buy': 0, 'Buy': 0, 'Hold': 0, 'Sell': 0, 'Strong Sell': 0}, index=['Last 3mo']).T

        for company in self.companies.values():
            peer_df_rot_3mo += company.analyst_data[1]

        peer_df_rot_3mo = peer_df_rot_3mo / len(self.companies.keys())

        self.analyst_data = [df_rating_30d, peer_df_rot_3mo]

    def set_df_esg(self):
        """Set self.df_pub_sent values"""

        result_list = []

        for metric in self.companies['c1'].df_esg.index:
            for company in self.companies.values():
                result_list.append(company.df_esg.loc[metric])
            
            result_list = [series for series in result_list if not isinstance(series[0], str)]
            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.df_esg[metric] = sum / len(result_list)

            else:
                self.df_esg[metric] = 'n/a'

            result_list.clear()

        self.df_esg = self.df_esg.T