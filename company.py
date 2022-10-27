# company.py
"""Company class and PeerGroup subclass definitions and methods.
    Version 0.7.1
    Last updated 10/27/22
"""

from copy import deepcopy
from openbb_terminal.api import openbb as obb
import pandas as pd
from dataclasses import dataclass, field
from IPython.display import display

scores_value = pd.DataFrame({'value': {'v1': None, 'v2': None, 'v3': None, 'v4': None, 'v5': None, 'v6': None, 'v7': None, 'v8': None, 'v9': None}})
scores_mgmt = pd.DataFrame({'mgmt': {'m1': None, 'm2': None, 'm3': None, 'm4': None, 'm5': None, 'm6': None, 'm7': None, 'm8': None, 'm9': None}})
scores_ins = pd.DataFrame({'ins': {'i1': None, 'i2': None, 'i3': None, 'i4': None}})
scores_div = pd.DataFrame({'div': {'d1': None, 'd2': None, 'd3': None, 'd4': None}})

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
    score_dict: dict = field(default_factory=lambda: {'value': deepcopy(scores_value), 
                                                      'mgmt': deepcopy(scores_mgmt),
                                                      'ins': deepcopy(scores_ins), 
                                                      'div': deepcopy(scores_div)}) # a dictionary of dataframes

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
        if pe_mrq == 'n/a':
            self.score_dict['value'].loc['v1'][0] = 0

        elif pe_mrq <= (peer_pe_mrq * 0.9):
            self.score_dict['value'].loc['v1'][0] = 3

        elif pe_mrq <= (peer_pe_mrq * 1.05):
            self.score_dict['value'].loc['v1'][0] = 1

        elif pe_mrq > (peer_pe_mrq * 1.05):
            self.score_dict['value'].loc['v1'][0] = 0

        else:
            print('v1 case slipped through')

        #**************************************************************** v2
        if pe_mrq == 'n/a':
            self.score_dict['value'].loc['v2'][0] = 0

        elif pe_mrq <= (pe_5yr_avg * 0.75):
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
        if ptb_mrq == 'n/a' or roe_mrq == 'n/a':
            self.score_dict['value'].loc['v3'][0] = 0

        elif ptb_mrq <= (peer_ptb_mrq * 0.9) and roe_mrq >= (peer_roe_mrq * 1.1):
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
        if ptb_mrq == 'n/a':
            self.score_dict['value'].loc['v4'][0] = 0

        elif ptb_mrq < 2:
            self.score_dict['value'].loc['v4'][0] = 2

        elif ptb_mrq >= 2 and ptb_mrq <= 4:
            self.score_dict['value'].loc['v4'][0] = 1

        elif ptb_mrq > 4:
            self.score_dict['value'].loc['v4'][0] = 0

        else:
            print('v4 case slipped through')

        #**************************************************************** v5
        if ptb_mrq == 'n/a' or bvps_mrq == 'n/a':
            self.score_dict['value'].loc['v5'][0] = 0

        elif ptb_mrq <= (peer_ptb_mrq * 0.9) and bvps_mrq > (bvps_5yr_avg * 1.05):
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
        if pfcf_mrq == 'n/a':
            self.score_dict['value'].loc['v6'][0] = 0

        elif pfcf_mrq <= (peer_pfcf_mrq * .9):
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
        if tca_div_tld == 'n/a':
            self.score_dict['value'].loc['v7'][0] = 0

        elif tca_div_tld >= 1.1:
            self.score_dict['value'].loc['v7'][0] = 2

        elif tca_div_tld < 1.1 and tca_div_tld >= 0.9:
            self.score_dict['value'].loc['v7'][0] = 1

        elif tca_div_tld > 0.9:
            self.score_dict['value'].loc['v7'][0] = 0

        else:
            print('v7 case slipped through')

        #**************************************************************** v8
        if tca_div_tld == 'n/a':
            self.score_dict['value'].loc['v8'][0] = 0

        elif tca_div_tld >= (peer_tca_div_tld * 1.2):
            self.score_dict['value'].loc['v8'][0] = 4

        elif tca_div_tld < (peer_tca_div_tld * 1.2) and tca_div_tld > peer_tca_div_tld:
            self.score_dict['value'].loc['v8'][0] = 2

        elif tca_div_tld <= peer_tca_div_tld:
            self.score_dict['value'].loc['v8'][0] = 0

        else:
            print('v8 case slipped through')

        #**************************************************************** v9

        if pts_mrq == 'n/a' or tca_div_tld == 'n/a':
            self.score_dict['value'].loc['v9'][0] = 0

        elif pts_mrq < (peer_pts_mrq * 0.9) and tca_div_tld >= 1.1:
            self.score_dict['value'].loc['v9'][0] = 4

        elif pts_mrq <= (peer_pts_mrq * 0.9) and tca_div_tld < 1.1 and tca_div_tld >= 0.95:
            self.score_dict['value'].loc['v9'][0] = 3

        elif pts_mrq <= (peer_pts_mrq * 0.9) and tca_div_tld < 0.95 and tca_div_tld >= 0.8:
            self.score_dict['value'].loc['v9'][0] = 2

        elif pts_mrq > (peer_pts_mrq * 0.9) and pts_mrq <= (peer_pts_mrq * 1.1) and tca_div_tld >= 0.8:
            self.score_dict['value'].loc['v9'][0] = 1

        elif pts_mrq > (peer_pts_mrq * 0.9) or tca_div_tld < 0.8:
            self.score_dict['value'].loc['v9'][0] = 0

        else:
            print('v9 case slipped through')

    def set_scores_mgmt(self, peer_group):

        roa_mrq = self.df_mgmt.loc['roa_mrq'][0]
        peer_roa_mrq = peer_group.df_mgmt.loc['roa_mrq'][0]
        roa_5yr_avg = self.df_mgmt.loc['roa_5yr_avg'][0]
        roe_mrq = self.df_mgmt.loc['roe_mrq'][0]
        peer_roe_mrq = peer_group.df_mgmt.loc['roe_mrq'][0]
        roe_5yr_avg = self.df_mgmt.loc['roe_5yr_avg'][0]
        dte_mrq = self.df_mgmt.loc['dte_mrq'][0]
        dte_5yr_avg = self.df_mgmt.loc['dte_5yr_avg'][0]
        gpr = self.df_mgmt.loc['gpr'][0]
        peer_gpr = peer_group.df_mgmt.loc['gpr'][0]
        pm = self.df_mgmt.loc['pm'][0]
        peer_pm = peer_group.df_mgmt.loc['pm'][0]
        cr_mrq = self.df_mgmt.loc['cr_mrq'][0]
        cr_5yr_avg = self.df_mgmt.loc['cr_5yr_avg'][0]
        peer_cr_mrq = peer_group.df_mgmt.loc['cr_mrq'][0]

        #**************************************************************** m1

        if roa_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m1'][0] = 0

        elif roa_mrq >= (peer_roa_mrq * 1.1):
            self.score_dict['mgmt'].loc['m1'][0] = 3

        elif roa_mrq < (peer_roa_mrq * 1.1) and roa_mrq >= peer_roa_mrq:
            self.score_dict['mgmt'].loc['m1'][0] = 1

        elif roa_mrq < peer_roa_mrq:
            self.score_dict['mgmt'].loc['m1'][0] = 0

        else:
            print('m1 case slipped through')

        #**************************************************************** m2

        if roa_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m2'][0] = 0

        elif roa_mrq > (roa_5yr_avg * 1.1):
            self.score_dict['mgmt'].loc['m2'][0] = 3

        elif roa_mrq <= (roa_5yr_avg * 1.1) and roa_mrq >= (roa_5yr_avg * 0.95):
            self.score_dict['mgmt'].loc['m2'][0] = 1

        elif roa_mrq < (roa_5yr_avg * 0.95):
            self.score_dict['mgmt'].loc['m2'][0] = 0

        else:
            print('m2 case slipped through')

        #**************************************************************** m3

        if roe_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m3'][0] = 0

        elif roe_mrq >= (peer_roe_mrq * 1.1):
            self.score_dict['mgmt'].loc['m3'][0] = 3

        elif roe_mrq < (peer_roe_mrq * 1.1) and roa_mrq >= peer_roa_mrq:
            self.score_dict['mgmt'].loc['m3'][0] = 1

        elif roe_mrq < peer_roe_mrq:
            self.score_dict['mgmt'].loc['m3'][0] = 0

        else:
            print('m3 case slipped through')

        #**************************************************************** m4

        if roe_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m4'][0] = 0

        elif roe_mrq > (roe_5yr_avg * 1.1):
            self.score_dict['mgmt'].loc['m4'][0] = 3

        elif roe_mrq <= (roe_5yr_avg * 1.1) and roe_mrq >= (roe_5yr_avg * 0.95):
            self.score_dict['mgmt'].loc['m4'][0] = 1

        elif roe_mrq < (roe_5yr_avg * 0.95):
            self.score_dict['mgmt'].loc['m4'][0] = 0

        else:
            print('m4 case slipped through')

        #**************************************************************** m5

        if dte_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m5'][0] = 0

        elif dte_mrq < (dte_5yr_avg * 0.85):
            self.score_dict['mgmt'].loc['m5'][0] = 3

        elif dte_mrq >= (dte_5yr_avg * 0.85) and dte_mrq <= dte_5yr_avg:
            self.score_dict['mgmt'].loc['m5'][0] = 1

        elif dte_mrq >= dte_5yr_avg:
            self.score_dict['mgmt'].loc['m5'][0] = 0

        else:
            print('m5 case slipped through')

        #**************************************************************** m6

        if gpr == 'n/a':
            self.score_dict['mgmt'].loc['m6'][0] = 0

        elif gpr > (peer_gpr * 1.05):
            self.score_dict['mgmt'].loc['m6'][0] = 3

        elif gpr <= (peer_gpr * 1.05) and gpr >= (peer_gpr * 0.95):
            self.score_dict['mgmt'].loc['m6'][0] = 1

        elif gpr < (peer_gpr * 0.95):
            self.score_dict['mgmt'].loc['m6'][0] = 0

        else:
            print('m6 case slipped through')

        #**************************************************************** m7

        if pm == 'n/a':
            self.score_dict['mgmt'].loc['m7'][0] = 0

        elif pm > (peer_pm * 1.05):
            self.score_dict['mgmt'].loc['m7'][0] = 3

        elif pm <= (peer_pm * 1.05) and pm >= (peer_pm * 0.95):
            self.score_dict['mgmt'].loc['m7'][0] = 1

        elif pm < (peer_pm * 0.95):
            self.score_dict['mgmt'].loc['m7'][0] = 0

        else:
            print('m7 case slipped through')

        #**************************************************************** m8

        if cr_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m8'][0] = 0

        elif cr_mrq >= 3:
            self.score_dict['mgmt'].loc['m8'][0] = 3

        elif cr_mrq < 3 and cr_mrq >= 1.5:
            self.score_dict['mgmt'].loc['m8'][0] = 2

        elif cr_mrq < 1.5 and cr_mrq >= 1:
            self.score_dict['mgmt'].loc['m8'][0] = 1

        elif cr_mrq < 1:
            self.score_dict['mgmt'].loc['m8'][0] = 0

        else:
            print('m8 case slipped through')

        #**************************************************************** m9

        if cr_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m9'][0] = 0

        elif cr_mrq >= (peer_cr_mrq * 1.3):
            self.score_dict['mgmt'].loc['m9'][0] = 4

        elif cr_mrq < (peer_cr_mrq * 1.3) and cr_mrq >= (peer_cr_mrq * 1.15):
            self.score_dict['mgmt'].loc['m9'][0] = 2

        elif cr_mrq < (peer_cr_mrq * 1.15) and cr_mrq >= (peer_cr_mrq * 0.95):
            self.score_dict['mgmt'].loc['m9'][0] = 1

        elif cr_mrq < (peer_cr_mrq * 0.95):
            self.score_dict['mgmt'].loc['m9'][0] = 0

        else:
            print('m9 case slipped through')

    def set_scores_ins(self, peer_group):

        io = self.df_ins.loc['io'][0]
        peer_io = peer_group.df_ins.loc['io'][0]
        it = self.df_ins.loc['it'][0]
        peer_it = peer_group.df_ins.loc['it'][0]
        inst_t = self.df_ins.loc['inst_t'][0]

        #**************************************************************** i1

        if io == 'n/a':
            self.score_dict['ins'].loc['i1'][0] = 0

        elif io >= (peer_io * 1.5):
            self.score_dict['ins'].loc['i1'][0] = 2

        elif io < (peer_io * 1.5) and io >= (peer_io * 1.05):
            self.score_dict['ins'].loc['i1'][0] = 1

        elif io < (peer_io * 1.05):
            self.score_dict['ins'].loc['i1'][0] = 0

        else:
            print('i1 case slipped through')

        #**************************************************************** i2

        if io == 'n/a':
            self.score_dict['ins'].loc['i2'][0] = 0

        elif io >= 0.1:
            self.score_dict['ins'].loc['i2'][0] = 3

        elif io < 0.1 and io >= .05:
            self.score_dict['ins'].loc['i2'][0] = 2

        elif io < 0.05 and io >= 0.01:
            self.score_dict['ins'].loc['i2'][0] = 1

        elif io < 0.01:
            self.score_dict['ins'].loc['i2'][0] = 0

        else:
            print('i2 case slipped through')

        #**************************************************************** i3

        if it == 'n/a':
            self.score_dict['ins'].loc['i3'][0] = 0

        elif it >= 0.03:
            self.score_dict['ins'].loc['i3'][0] = 6

        elif it < 0.03 and io >= .015:
            self.score_dict['ins'].loc['i3'][0] = 4

        elif it < 0.015 and io >= 0:
            self.score_dict['ins'].loc['i3'][0] = 2

        elif it < 0:
            self.score_dict['ins'].loc['i3'][0] = 0

        else:
            print('i3 case slipped through')

        #**************************************************************** i4

        if inst_t == 'n/a':
            self.score_dict['ins'].loc['i4'][0] = 0

        elif inst_t >= 0.03:
            self.score_dict['ins'].loc['i4'][0] = 3

        elif inst_t < 0.03 and inst_t >= 0:
            self.score_dict['ins'].loc['i4'][0] = 1

        elif inst_t < 0:
            self.score_dict['ins'].loc['i4'][0] = 0

        else:
            print('i4 case slipped through')

    def set_scores_div(self, peer_group):

        div = self.div_dfs[0].loc['div'][0]
        peer_div = peer_group.div_dfs[0].loc['div'][0]
        div_y = self.div_dfs[0].loc['div_y'][0]
        peer_div_y = peer_group.div_dfs[0].loc['div_y'][0]

        try: # The amount of the most recent dividend
            last_div = self.div_dfs[1].tail(1)['Dividends'][0]

        except ValueError:
            last_div = 0

        try: # The average of the last 12 dividends
            last12_avg = self.div_dfs[1].tail(12).mean(axis=0)[0]

        except ValueError:
            last12_avg = 0

        #**************************************************************** d1

        if div == 'n/a' or peer_div == 'n/a':
            self.score_dict['div'].loc['d1'][0] = 0

        elif div >= (peer_div * 1.2):
            self.score_dict['div'].loc['d1'][0] = 2

        elif div < (peer_div * 1.2) and div >= peer_div:
            self.score_dict['div'].loc['d1'][0] = 1

        elif div < peer_div:
            self.score_dict['div'].loc['d1'][0] = 0

        else:
            print('d1 case slipped through')

        #**************************************************************** d2

        if div_y == 'n/a' or peer_div_y == 'n/a':
            self.score_dict['div'].loc['d2'][0] = 0

        elif div_y >= (peer_div_y * 1.2):
            self.score_dict['div'].loc['d2'][0] = 2

        elif div_y < (peer_div_y * 1.2) and div >= peer_div:
            self.score_dict['div'].loc['d2'][0] = 1

        elif div_y < peer_div_y:
            self.score_dict['div'].loc['d2'][0] = 0

        else:
            print('d2 case slipped through')

        #**************************************************************** d3

        if last_div == 0 or last12_avg == 0:
            self.score_dict['div'].loc['d3'][0] = 0

        elif last_div >= (last12_avg * 1.2):
            self.score_dict['div'].loc['d3'][0] = 2

        elif last_div < (last12_avg * 1.2) and last_div >= last12_avg:
            self.score_dict['div'].loc['d3'][0] = 1

        elif last_div < last12_avg:
            self.score_dict['div'].loc['d3'][0] = 0

        else:
            print('d3 case slipped through')

        #**************************************************************** d4

        if div_y == 'n/a':
            self.score_dict['div'].loc['d4'][0] = 0

        elif div_y >= .02:
            self.score_dict['div'].loc['d4'][0] = 4

        elif div_y < .02 and div_y >= .01:
            self.score_dict['div'].loc['d4'][0] = 2

        elif div_y < .01 and div_y >= .005:
            self.score_dict['div'].loc['d4'][0] = 1

        elif div_y < .005:
            self.score_dict['div'].loc['d4'][0] = 0

        else:
            print('d4 case slipped through')

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