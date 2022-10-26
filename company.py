# company.py
"""Company class and PeerGroup subclass definitions and methods.
    Version 0.6
    Last updated 10/25/22
"""

from copy import deepcopy
from openbb_terminal.api import openbb as obb
import pandas as pd
from dataclasses import dataclass, field
from IPython.display import display

scores_value = pd.DataFrame({'Value': {'v1': None, 'v2': None, 'v3': None, 'v4': None, 'v5': None, 'v6': None, 'v7': None, 'v8': None, 'v9': None}})
scores_mgmt = pd.DataFrame({'MGMT': {'m1': None, 'm2': None, 'm3': None, 'm4': None}})

@dataclass
class Company:
    """Class Company for creating Company objects."""

    df_basic: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(6,1), holds basic company details
    df_value: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(18,1), holds value metrics
    df_mgmt: pd.DataFrame = field(default_factory=pd.DataFrame)# shape=(14,1), holds management metrics
    df_ins: pd.DataFrame = field(default_factory=pd.DataFrame)# shape=(4,1), holds insider & instituion data
    div_dfs: list = field(default_factory=list, repr=False) # holds 2 DataFrames containing dividend data
    df_pub_sent: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(3,1), holds public sentiment data
    news_dfs: list = field(default_factory=list, repr=False) # holds 3 DataFrames containing Company, Sector, & Industry news
    analyst_data: list = field(default_factory=list, repr=False) # olds 2 DataFrames containing Analyst ratingsmetrics
    df_esg: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(27,1), holds ESG data & metrics
    score_dict: dict = field(default_factory=lambda: {'value': deepcopy(scores_value), 'mgmt': deepcopy(scores_mgmt)}) # a dictionary of dataframes

    def set_scores_value(self, peer_group):

        # variables for ease of reading
        pe_mrq = self.df_value.loc['pe_mrq'][0]
        peer_pe_mrq = peer_group.df_value.loc['pe_mrq'][0]
        pe_5yr_avg = self.df_value.loc['pe_5yr_avg'][0]
        ptb_mrq = self.df_value.loc['ptb_mrq'][0]
        peer_ptb_mrq = peer_group.df_value.loc['ptb_mrq'][0]
        roe_mrq = self.df_mgmt.loc['roe_mrq'][0]
        peer_roe_mrq = peer_group.df_mgmt.loc['roe_mrq'][0]
        bvps_mrq = self.df_value.loc['bvps_mrq'][0]
        bvps_5yr_avg = self.df_value.loc['bvps_5yr_avg'][0]
        pfcf_mrq = self.df_value.loc['pfcf_mrq'][0]
        pfcf_5yr_avg = self.df_value.loc['pfcf_5yr_avg'][0]
        peer_pfcf_mrq = peer_group.df_value.loc['pfcf_mrq'][0]
        tca_div_tld = self.df_value.loc['tca_div_tld'][0]
        peer_tca_div_tld = peer_group.df_value.loc['tca_div_tld'][0]
        pts_mrq = self.df_value.loc['pts_mrq'][0]
        pts_5yr_avg = self.df_value.loc['pts_5yr_avg'][0]
        peer_pts_mrq = peer_group.df_value.loc['pts_mrq'][0]

        #**************************************************************** v1
        if pe_mrq <= (peer_pe_mrq * 0.9):
            self.score_dict['value'].loc['v1'][0] = 3

        elif pe_mrq <= (peer_pe_mrq * 1.05):
            self.score_dict['value'].loc['v1'][0] = 1

        elif pe_mrq > (peer_pe_mrq * 1.05):
            self.score_dict['value'].loc['v1'][0] = 0

        else:
            print('v1 case slipped through')

        #**************************************************************** v2
        if pe_mrq <= (pe_5yr_avg * 0.75):
            self.score_dict['value'].loc['v2'][0] = 3

        elif pe_mrq < (pe_5yr_avg * 0.9):
            self.score_dict['value'].loc['v2'][0] = 2

        elif pe_mrq <= pe_5yr_avg:
            self.score_dict['value'].loc['v2'][0] = 1

        elif pe_mrq > pe_5yr_avg:
            self.score_dict['value'].loc['v2'][0] = 0

        else:
            print('v2 case slipped through')

        #**************************************************************** v3
        if ptb_mrq <= (peer_ptb_mrq * 0.9) and roe_mrq >= (peer_roe_mrq * 1.1):
            self.score_dict['value'].loc['v3'][0] = 3

        elif ptb_mrq <= (peer_ptb_mrq * 1.05) and roe_mrq >= (peer_roe_mrq * .95):
            self.score_dict['value'].loc['v3'][0] = 2

        elif ptb_mrq >= (peer_ptb_mrq * 1.05) and roe_mrq <= (peer_roe_mrq * .95):
            self.score_dict['value'].loc['v3'][0] = 1

        elif ptb_mrq > (peer_ptb_mrq * 1.05) or roe_mrq < (peer_roe_mrq * .95):
            self.score_dict['value'].loc['v3'][0] = 0

        else:
            print('v3 case slipped through')

        #**************************************************************** v4
        if ptb_mrq < 2:
            self.score_dict['value'].loc['v4'][0] = 2

        elif ptb_mrq >= 2 and ptb_mrq <= 4:
            self.score_dict['value'].loc['v4'][0] = 1

        elif ptb_mrq > 4:
            self.score_dict['value'].loc['v4'][0] = 0

        else:
            print('v4 case slipped through')

        #**************************************************************** v5
        if ptb_mrq <= (peer_ptb_mrq * 0.9) and bvps_mrq > (bvps_5yr_avg * 1.05):
            self.score_dict['value'].loc['v5'][0] = 3

        elif ptb_mrq <= (peer_ptb_mrq * 0.9) and bvps_mrq >= (bvps_5yr_avg * 0.95):
            self.score_dict['value'].loc['v5'][0] = 2

        elif ptb_mrq <= (peer_ptb_mrq * 1.05) and bvps_mrq >= (bvps_5yr_avg * 0.95):
            self.score_dict['value'].loc['v5'][0] = 1

        elif ptb_mrq > (peer_ptb_mrq * 1.05) or bvps_mrq < (bvps_5yr_avg * 0.95):
            self.score_dict['value'].loc['v5'][0] = 0

        else:
            print('v5 case slipped through')

        #**************************************************************** v6
        if pfcf_mrq <= (peer_pfcf_mrq * .9):
            self.score_dict['value'].loc['v6'][0] = 3

        elif pfcf_mrq > (peer_pfcf_mrq * .9) and pfcf_mrq <= peer_pfcf_mrq:
            self.score_dict['value'].loc['v6'][0] = 2

        elif pfcf_mrq >= peer_pfcf_mrq and pfcf_mrq < (peer_pfcf_mrq * 1.05):
            self.score_dict['value'].loc['v6'][0] = 1

        elif pfcf_mrq > (peer_pfcf_mrq * 1.05):
            self.score_dict['value'].loc['v6'][0] = 0

        else:
            print('v6 case slipped through')

        #**************************************************************** v7
        if tca_div_tld >= 1.1:
            self.score_dict['value'].loc['v7'][0] = 2

        elif tca_div_tld < 1.1 and tca_div_tld >= 0.9:
            self.score_dict['value'].loc['v7'][0] = 1

        elif tca_div_tld > 0.9:
            self.score_dict['value'].loc['v7'][0] = 0

        else:
            print('v7 case slipped through')

        #**************************************************************** v8
        if tca_div_tld >= (peer_tca_div_tld * 1.2):
            self.score_dict['value'].loc['v8'][0] = 4

        elif tca_div_tld < (peer_tca_div_tld * 1.2) and tca_div_tld > peer_tca_div_tld:
            self.score_dict['value'].loc['v8'][0] = 2

        elif tca_div_tld <= peer_tca_div_tld:
            self.score_dict['value'].loc['v8'][0] = 0

        else:
            print('v8 case slipped through')

        #**************************************************************** v9
        if pts_mrq < (peer_pts_mrq * 0.9) and tca_div_tld >= 1.1:
            self.score_dict['value'].loc['v9'][0] = 4

        elif pts_mrq >= (peer_pts_mrq * 0.9) and pts_mrq <= peer_pts_mrq and tca_div_tld < 1.1 and tca_div_tld >= 0.95:
            self.score_dict['value'].loc['v9'][0] = 3

        elif pts_mrq >= (peer_pts_mrq * 0.9) and pts_mrq <= peer_pts_mrq and tca_div_tld < 0.95 and tca_div_tld >= 0.8:
            self.score_dict['value'].loc['v9'][0] = 2

        elif pts_mrq > peer_pts_mrq and pts_mrq <= (peer_pts_mrq * 1.1) and tca_div_tld >= 0.8:
            self.score_dict['value'].loc['v9'][0] = 1

        elif pts_mrq >= (peer_pts_mrq * 1.1) or tca_div_tld < 0.8:
            self.score_dict['value'].loc['v9'][0] = 0

        else:
            print('v9 case slipped through')

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
    
    company_list: list = field(default_factory=list) # List of 1 or more Company objects

    def set_df_basic(self):
        """Set self.df_basic values"""

        self.df_basic['name'] = self.company_list[0].df_basic.loc['ticker'] + ' Peer Group Avg'
        self.df_basic['ticker'] = self.company_list[0].df_basic.loc['ticker'] + ' Peer Avg'
        self.df_basic['sector'] = self.company_list[0].df_basic.loc['sector']
        self.df_basic['industry'] = self.company_list[0].df_basic.loc['industry']
        self.df_basic['cap'] = 'temp n/a'
        self.df_basic['price'] = 'temp n/a'

        self.df_basic = self.df_basic.T

    def set_df_value(self):
        """Set self.df_value values"""

        result_list = []

        for metric in self.company_list[0].df_value.index:
            for company in self.company_list:

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

        for metric in self.company_list[0].df_mgmt.index:
            for company in self.company_list:
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

        for metric in self.company_list[0].df_ins.index:
            for company in self.company_list:
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

        for metric in self.company_list[0].div_dfs[0].index:
            for company in self.company_list:
                result_list.append(company.div_dfs[0].loc[metric])
            
            result_list = [series for series in result_list if not isinstance(series[0], str)]

            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.div_dfs[0][metric] = sum / len(result_list)

            else:
                self.div_dfs[0][metric] = 'n/a'

#            self.div_dfs[0][metric] = sum / len(result_list)
            result_list.clear()

        self.div_dfs[0] = self.div_dfs[0].T

    def set_df_pub_sent(self):
        """Set self.df_pub_sent values"""

        result_list = []

        for metric in self.company_list[0].df_pub_sent.index:
            for company in self.company_list:
                result_list.append(company.df_pub_sent.loc[metric])
            
            result_list = [series for series in result_list if not isinstance(series[0], str)]
            sum = 0
            for value in result_list:
                sum += value

            if len(result_list) != 0:
                self.df_pub_sent[metric] = sum / len(result_list)

            else:
                self.df_pub_sent[metric] = 'n/a'

#            self.df_pub_sent[metric] = sum / len(result_list)
            result_list.clear()

        self.df_pub_sent = self.df_pub_sent.T

    def set_news_dfs(self):
        """Set self.div_dfs values"""

        df_com_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Company News'])
        df_sec_news = obb.common.news(self.company_list[0].df_basic.loc['sector'][0] + 'Sector News Stock Market', sort='published').head(50)
        df_ind_news = obb.common.news(self.company_list[0].df_basic.loc['industry'][0] + 'Industry News Stock Market', sort='published').head(50)

        self.news_dfs = [df_com_news, df_sec_news, df_ind_news]

    def set_na_dfs(self):
        df_rating_30d = pd.DataFrame({'Data N/A': 'n/a'}, index=['df_rating_30d']).T
        df_rot_3mo = pd.DataFrame({'Data N/A': 'n/a'}, index=['df_rot_3mo']).T
        wb_score = 'n/a'
        empty_data = [df_rating_30d, df_rot_3mo, wb_score]
        for na_value in empty_data:
            self.analyst_data.append(na_value)

        self.df_esg = pd.DataFrame({'Data N/A': 'n/a'}, index=['ESG Data']).T

    def set_all_data(self):
        self.set_df_basic()
        self.set_df_value()
        self.set_df_mgmt()
        self.set_df_ins()
        self.set_div_dfs()
        self.set_df_pub_sent()
        self.set_news_dfs()
        self.set_na_dfs()