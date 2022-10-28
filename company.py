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

scores_value = pd.DataFrame({'value': {'v1': None, 'v2': None, 'v3': None, 'v4': None, 'v5': None, 
                                       'v6': None, 'v7': None, 'v8': None, 'v9': None, 'v10': None, 'v11': None}})

scores_mgmt = pd.DataFrame({'mgmt': {'m1': None, 'm2': None, 'm3': None, 'm4': None, 
                                     'm5': None, 'm6': None, 'm7': None, 'm8': None, 'm9': None, 'm10': None}})

scores_ins = pd.DataFrame({'ins': {'i1': None, 'i2': None, 'i3': None, 'i4': None}})
scores_div = pd.DataFrame({'div': {'d1': None, 'd2': None, 'd3': None, 'd4': None}})
scores_pub_sent = pd.DataFrame({'pub_sent': {'p1': None, 'p2': None, 'p3': None, 'p4': None, 'p5': None, 'p6': None}})
scores_analyst_data = pd.DataFrame({'analyst_data': {'a1': None, 'a2': None, 'a3': None, 'a4': None, 'a5': None}})
scores_esg = pd.DataFrame({'esg': {'e1': None, 'e2': None, 'e3': None, 'e4': None, 'e5': None}})

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
    analyst_data: list = field(default_factory=list, repr=False) # holds 2 DataFrames containing Analyst ratingsmetrics
    df_esg: pd.DataFrame = field(default_factory=pd.DataFrame) # shape=(5,1), holds ESG data & metrics
    score_dict: dict = field(default_factory=lambda: {'value': deepcopy(scores_value), 
                                                      'mgmt': deepcopy(scores_mgmt),
                                                      'ins': deepcopy(scores_ins), 
                                                      'div': deepcopy(scores_div),
                                                      'pub_sent': deepcopy(scores_pub_sent),
                                                      'analyst_data': deepcopy(scores_analyst_data),
                                                      'esg': deepcopy(scores_esg)}) # a dictionary of dataframes

    def set_scores_value(self, peer_group):

        # setting VALUE variables for ease of reading
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
            self.score_dict['value'].loc['v6'][0] = 2

        elif pfcf_mrq > (peer_pfcf_mrq * .9) and pfcf_mrq <= (peer_pfcf_mrq * 1.05):
            self.score_dict['value'].loc['v6'][0] = 1

        elif pfcf_mrq > (peer_pfcf_mrq * 1.05):
            self.score_dict['value'].loc['v6'][0] = 0

        else:
            print('v6 case slipped through')

        #**************************************************************** v7
        if pfcf_mrq == 'n/a' or pfcf_5yr_avg == 'n/a':
            self.score_dict['value'].loc['v7'][0] = 0

        elif pfcf_mrq <= (pfcf_5yr_avg * 0.9):
            self.score_dict['value'].loc['v7'][0] = 2

        elif pfcf_mrq > (pfcf_5yr_avg * 0.9) and pfcf_mrq < (pfcf_5yr_avg * 1.05):
            self.score_dict['value'].loc['v7'][0] = 1

        elif pfcf_mrq > (pfcf_5yr_avg * 1.05):
            self.score_dict['value'].loc['v7'][0] = 0

        else:
            print('v7 case slipped through')

        #**************************************************************** v8
        if tca_div_tld == 'n/a':
            self.score_dict['value'].loc['v8'][0] = 0

        elif tca_div_tld >= 1.1:
            self.score_dict['value'].loc['v8'][0] = 2

        elif tca_div_tld < 1.1 and tca_div_tld >= 0.9:
            self.score_dict['value'].loc['v8'][0] = 1

        elif tca_div_tld < 0.9:
            self.score_dict['value'].loc['v8'][0] = 0

        else:
            print('v8 case slipped through')

        #**************************************************************** v9
        if tca_div_tld == 'n/a':
            self.score_dict['value'].loc['v9'][0] = 0

        elif tca_div_tld >= (peer_tca_div_tld * 1.2):
            self.score_dict['value'].loc['v9'][0] = 2

        elif tca_div_tld < (peer_tca_div_tld * 1.2) and tca_div_tld > peer_tca_div_tld:
            self.score_dict['value'].loc['v9'][0] = 1

        elif tca_div_tld <= peer_tca_div_tld:
            self.score_dict['value'].loc['v9'][0] = 0

        else:
            print('v9 case slipped through')

        #**************************************************************** v10

        if pts_mrq == 'n/a' or tca_div_tld == 'n/a':
            self.score_dict['value'].loc['v10'][0] = 0

        elif pts_mrq < (peer_pts_mrq * 0.9) and tca_div_tld >= 1.1:
            self.score_dict['value'].loc['v10'][0] = 4

        elif pts_mrq <= (peer_pts_mrq * 0.9) and tca_div_tld < 1.1 and tca_div_tld >= 0.95:
            self.score_dict['value'].loc['v10'][0] = 3

        elif pts_mrq <= (peer_pts_mrq * 0.9) and tca_div_tld < 0.95 and tca_div_tld >= 0.8:
            self.score_dict['value'].loc['v10'][0] = 2

        elif pts_mrq > (peer_pts_mrq * 0.9) and pts_mrq <= (peer_pts_mrq * 1.1) and tca_div_tld >= 0.8:
            self.score_dict['value'].loc['v10'][0] = 1

        elif pts_mrq > (peer_pts_mrq * 0.9) or tca_div_tld < 0.8:
            self.score_dict['value'].loc['v10'][0] = 0

        else:
            print('v10 case slipped through')

        #**************************************************************** v11
        if pts_mrq == 'n/a' or pts_5yr_avg == 'n/a':
            self.score_dict['value'].loc['v11'][0] = 0

        elif pts_mrq <= (pts_5yr_avg * 0.9):
            self.score_dict['value'].loc['v11'][0] = 2

        elif pts_mrq > (pts_5yr_avg * 0.9) and pts_mrq < (pts_5yr_avg * 1.05):
            self.score_dict['value'].loc['v11'][0] = 1

        elif pts_mrq > (pts_5yr_avg * 1.05):
            self.score_dict['value'].loc['v11'][0] = 0

        else:
            print('v11 case slipped through')


    def set_scores_mgmt(self, peer_group):

        # setting MANAGEMENT variables for ease of reading
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

        elif roe_mrq < (peer_roe_mrq * 1.1) and roe_mrq >= peer_roe_mrq:
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

        elif gpr > (peer_gpr * 1.1):
            self.score_dict['mgmt'].loc['m6'][0] = 4

        elif gpr <= (peer_gpr * 1.1) and gpr >= peer_gpr:
            self.score_dict['mgmt'].loc['m6'][0] = 2

        elif gpr < peer_gpr:
            self.score_dict['mgmt'].loc['m6'][0] = 0

        else:
            print('m6 case slipped through')

        #**************************************************************** m7

        if pm == 'n/a':
            self.score_dict['mgmt'].loc['m7'][0] = 0

        elif pm > (peer_pm * 1.1):
            self.score_dict['mgmt'].loc['m7'][0] = 4

        elif pm <= (peer_pm * 1.1) and pm >= peer_pm:
            self.score_dict['mgmt'].loc['m7'][0] = 2

        elif pm < peer_pm:
            self.score_dict['mgmt'].loc['m7'][0] = 0

        else:
            print('m7 case slipped through')

        #**************************************************************** m8

        if cr_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m8'][0] = 0

        elif cr_mrq >= 1.1 and cr_mrq <= 2:
            self.score_dict['mgmt'].loc['m8'][0] = 2

        elif cr_mrq < 1.1 and cr_mrq >= 0.95 or cr_mrq > 2 and cr_mrq <= 3:
            self.score_dict['mgmt'].loc['m8'][0] = 1

        elif cr_mrq < 0.95 or cr_mrq > 3:
            self.score_dict['mgmt'].loc['m8'][0] = 0

        else:
            print('m8 case slipped through')

        #**************************************************************** m9

        if cr_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m9'][0] = 0

        elif cr_mrq <= (peer_cr_mrq * 1.2) and cr_mrq >= (peer_cr_mrq * 0.9):
            self.score_dict['mgmt'].loc['m9'][0] = 1

        elif cr_mrq > (peer_cr_mrq * 1.2) or cr_mrq < (peer_cr_mrq * 0.9):
            self.score_dict['mgmt'].loc['m9'][0] = 0

        else:
            print('m9 case slipped through')

        #**************************************************************** m10

        if cr_mrq == 'n/a':
            self.score_dict['mgmt'].loc['m10'][0] = 0

        elif cr_mrq <= (cr_5yr_avg * 1.2) and cr_mrq >= (cr_5yr_avg * 0.9):
            self.score_dict['mgmt'].loc['m10'][0] = 1

        elif cr_mrq > (cr_5yr_avg * 1.2) or cr_mrq < (cr_5yr_avg * 0.9):
            self.score_dict['mgmt'].loc['m10'][0] = 0

        else:
            print('m10 case slipped through')

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
            self.score_dict['ins'].loc['i3'][0] = 4

        elif it < 0.03 and io >= .015:
            self.score_dict['ins'].loc['i3'][0] = 3

        elif it < 0.015 and io >= 0:
            self.score_dict['ins'].loc['i3'][0] = 1

        elif it < 0:
            self.score_dict['ins'].loc['i3'][0] = 0

        else:
            print('i3 case slipped through')

        #**************************************************************** i4

        if inst_t == 'n/a':
            self.score_dict['ins'].loc['i4'][0] = 0

        elif inst_t >= 0.02:
            self.score_dict['ins'].loc['i4'][0] = 1

        elif inst_t < 0.02:
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
            last_div = 'n/a'

        except AttributeError:
            last_div = 'n/a'

        try: # The average of the last 12 dividends
            last12_avg = self.div_dfs[1].tail(12).mean(axis=0)[0]

        except ValueError:
            last12_avg = 'n/a'

        except AttributeError:
            last12_avg = 'n/a'

        #**************************************************************** d1

        # setting 'n/a' to 1 so as not to penalize companies who have no div
        if div == 'n/a' or peer_div == 'n/a':
            self.score_dict['div'].loc['d1'][0] = 1

        elif div >= (peer_div * 1.2):
            self.score_dict['div'].loc['d1'][0] = 2

        elif div < (peer_div * 1.2) and div >= peer_div:
            self.score_dict['div'].loc['d1'][0] = 1

        elif div < peer_div:
            self.score_dict['div'].loc['d1'][0] = 0

        else:
            print('d1 case slipped through')



        #**************************************************************** d2

        # setting 'n/a' to 1 so as not to penalize companies who have no div
        if last_div == 'n/a' or last12_avg == 'n/a':
            self.score_dict['div'].loc['d2'][0] = 1

        elif last_div >= (last12_avg * 1.2):
            self.score_dict['div'].loc['d2'][0] = 2

        elif last_div < (last12_avg * 1.2) and last_div >= last12_avg:
            self.score_dict['div'].loc['d2'][0] = 1

        elif last_div < last12_avg:
            self.score_dict['div'].loc['d2'][0] = 0

        else:
            print('d2 case slipped through')

        #**************************************************************** d3

        # setting 'n/a' to 1 so as not to penalize companies who have no div
        if div_y == 'n/a' or peer_div_y == 'n/a':
            self.score_dict['div'].loc['d3'][0] = 1

        elif div_y >= (peer_div_y * 1.2):
            self.score_dict['div'].loc['d3'][0] = 2

        elif div_y < (peer_div_y * 1.2) and div >= peer_div:
            self.score_dict['div'].loc['d3'][0] = 1

        elif div_y < peer_div_y:
            self.score_dict['div'].loc['d3'][0] = 0

        else:
            print('d3 case slipped through')

        #**************************************************************** d4

        if div_y == 'n/a':
            self.score_dict['div'].loc['d4'][0] = 1

        elif div_y >= .02:
            self.score_dict['div'].loc['d4'][0] = 2

        elif div_y < .02 and div_y >= .0075:
            self.score_dict['div'].loc['d4'][0] = 1

        elif div_y < .0075:
            self.score_dict['div'].loc['d4'][0] = 0

        else:
            print('d4 case slipped through')


    def set_scores_pub_sent(self, peer_group):

        twits_perc = self.df_pub_sent.loc['twits_perc'][0]
        peer_twits_perc = peer_group.df_pub_sent.loc['twits_perc'][0]
        shrt_int = self.df_pub_sent.loc['shrt_int'][0]
        peer_shrt_int = peer_group.df_pub_sent.loc['shrt_int'][0]
        news_sent = self.df_pub_sent.loc['news_sent'][0]
        peer_news_sent = peer_group.df_pub_sent.loc['news_sent'][0]

        #**************************************************************** p1

        if twits_perc == 'n/a':
            self.score_dict['pub_sent'].loc['p1'][0] = 0

        elif twits_perc >= .8:
            self.score_dict['pub_sent'].loc['p1'][0] = 1

        elif twits_perc < .8:
            self.score_dict['pub_sent'].loc['p1'][0] = 0

        else:
            print('p1 case slipped through')

        #**************************************************************** p2

        if twits_perc == 'n/a':
            self.score_dict['pub_sent'].loc['p2'][0] = 0

        elif twits_perc >= (peer_twits_perc * 1.1):
            self.score_dict['pub_sent'].loc['p2'][0] = 1

        elif twits_perc < (peer_twits_perc * 1.1):
            self.score_dict['pub_sent'].loc['p2'][0] = 0

        else:
            print('p2 case slipped through')

        #**************************************************************** p3

        if shrt_int == 'n/a':
            self.score_dict['pub_sent'].loc['p3'][0] = 0

        elif shrt_int <= 0.01:
            self.score_dict['pub_sent'].loc['p3'][0] = 2

        elif shrt_int > 0.01 and shrt_int <= 0.02:
            self.score_dict['pub_sent'].loc['p3'][0] = 1

        elif shrt_int > 0.02:
            self.score_dict['pub_sent'].loc['p3'][0] = 0

        else:
            print('p3 case slipped through')

        #**************************************************************** p4

        if shrt_int == 'n/a':
            self.score_dict['pub_sent'].loc['p4'][0] = 0

        elif shrt_int <= (peer_shrt_int * 0.9):
            self.score_dict['pub_sent'].loc['p4'][0] = 2

        elif shrt_int > (peer_shrt_int * 0.9) and shrt_int <= (peer_shrt_int * 1.05):
            self.score_dict['pub_sent'].loc['p4'][0] = 1

        elif shrt_int > (peer_shrt_int * 1.05):
            self.score_dict['pub_sent'].loc['p4'][0] = 0

        else:
            print('p4 case slipped through')

        #**************************************************************** p5

        if news_sent == 'n/a':
            self.score_dict['pub_sent'].loc['p5'][0] = 0

        elif news_sent >= 0.25:
            self.score_dict['pub_sent'].loc['p5'][0] = 1

        elif news_sent < 0.25:
            self.score_dict['pub_sent'].loc['p5'][0] = 0

        else:
            print('p5 case slipped through')

        #**************************************************************** p6

        if news_sent == 'n/a':
            self.score_dict['pub_sent'].loc['p6'][0] = 0

        elif news_sent >= (peer_news_sent * 1.1):
            self.score_dict['pub_sent'].loc['p6'][0] = 1

        elif news_sent < (peer_news_sent * 1.1):
            self.score_dict['pub_sent'].loc['p6'][0] = 0

        else:
            print('p6 case slipped through')



    def set_scores_analyst_data(self, peer_group):

        wghtd_buys_sum = self.analyst_data[1].loc['Buy'][0] + (self.analyst_data[1].loc['Strong Buy'][0] * 1.25)
        wghtd_peer_buys_sum = peer_group.analyst_data[1].loc['Buy'][0] + (peer_group.analyst_data[1].loc['Strong Buy'][0] * 1.25)
        holds = self.analyst_data[1].loc['Hold'][0]
        peer_holds = peer_group.analyst_data[1].loc['Hold'][0]
        wghtd_sells_sum = self.analyst_data[1].loc['Sell'][0] + (self.analyst_data[1].loc['Strong Sell'][0] * 1.25)
        wghtd_peer_sells_sum = peer_group.analyst_data[1].loc['Sell'][0] + (peer_group.analyst_data[1].loc['Strong Sell'][0] * 1.25)

        buys_perc = wghtd_buys_sum / (wghtd_buys_sum + holds + wghtd_sells_sum)
        peer_buys_perc = wghtd_peer_buys_sum / (wghtd_peer_buys_sum + peer_holds + wghtd_peer_sells_sum)
        sells_perc = wghtd_sells_sum / (wghtd_buys_sum + holds + wghtd_sells_sum)
        peer_sells_perc = wghtd_peer_sells_sum / (wghtd_peer_buys_sum + peer_holds + wghtd_peer_sells_sum)

        series_last_14 = self.analyst_data[0]['Rating'].head(14)
        
        #counting how many Strong Buy ratings have been issued in last 14 days
        strong_buys = 0
        for rating in series_last_14:
            if rating == 'Strong Buy':
                strong_buys += 1

        wb_score = self.analyst_data[2]

        #**************************************************************** a1

        if buys_perc == 'n/a':
            self.score_dict['analyst_data'].loc['a1'][0] = 0

        elif buys_perc >= (peer_buys_perc * 1.1):
            self.score_dict['analyst_data'].loc['a1'][0] = 1

        elif buys_perc < (peer_buys_perc * 1.1):
            self.score_dict['analyst_data'].loc['a1'][0] = 0

        else:
            print('a1 case slipped through')

        #**************************************************************** a2

        if sells_perc == 'n/a':
            self.score_dict['analyst_data'].loc['a2'][0] = 0

        elif sells_perc <= (peer_sells_perc * .9):
            self.score_dict['analyst_data'].loc['a2'][0] = 1

        elif sells_perc > (peer_sells_perc * .9):
            self.score_dict['analyst_data'].loc['a2'][0] = 0

        else:
            print('a2 case slipped through')

        #**************************************************************** a3

        if wghtd_buys_sum == 'n/a':
            self.score_dict['analyst_data'].loc['a3'][0] = 0

        elif wghtd_buys_sum >= (wghtd_peer_buys_sum * 1.5):
            self.score_dict['analyst_data'].loc['a3'][0] = 3

        elif wghtd_buys_sum < (wghtd_peer_buys_sum * 1.5) and wghtd_buys_sum >= (wghtd_peer_buys_sum * 1.1):
            self.score_dict['analyst_data'].loc['a3'][0] = 2

        elif wghtd_buys_sum < (wghtd_peer_buys_sum * 1.1) and wghtd_buys_sum >= (wghtd_peer_buys_sum * 0.7):
            self.score_dict['analyst_data'].loc['a3'][0] = 1

        elif wghtd_buys_sum < (wghtd_peer_buys_sum * 0.7):
            self.score_dict['analyst_data'].loc['a3'][0] = 0

        else:
            print('a3 case slipped through')

        #**************************************************************** a4

        if strong_buys == 'n/a':
            self.score_dict['analyst_data'].loc['a4'][0] = 0

        elif strong_buys >= 10:
            self.score_dict['analyst_data'].loc['a4'][0] = 2

        elif strong_buys < 10 and strong_buys >= 8:
            self.score_dict['analyst_data'].loc['a4'][0] = 1

        elif strong_buys < 8:
            self.score_dict['analyst_data'].loc['a4'][0] = 0

        else:
            print('a4 case slipped through')

        #**************************************************************** a5

        # Scoring 'n/a' as worth 1pt so as not to punish those not on S&P or NASDAQ 100
        if wb_score == 'n/a':
            self.score_dict['analyst_data'].loc['a5'][0] = 1

        elif wb_score >= 80:
            self.score_dict['analyst_data'].loc['a5'][0] = 3

        elif wb_score < 80 and wb_score >= 75:
            self.score_dict['analyst_data'].loc['a5'][0] = 2

        elif wb_score < 75 and wb_score >= 70:
            self.score_dict['analyst_data'].loc['a5'][0] = 1

        elif wb_score < 70:
            self.score_dict['analyst_data'].loc['a5'][0] = 0

        else:
            print('a5 case slipped through')


    def set_scores_esg(self, peer_group):

        enviro = self.df_esg.loc['enviro'][0]
        peer_enviro = peer_group.df_esg.loc['enviro'][0]
        govern = self.df_esg.loc['govern'][0]
        peer_govern = peer_group.df_esg.loc['govern'][0]
        social = self.df_esg.loc['social'][0]
        peer_social = peer_group.df_esg.loc['social'][0]
        total_esg = self.df_esg.loc['total_esg'][0]
        peer_total_esg = peer_group.df_esg.loc['total_esg'][0]
        esg_perf = self.df_esg.loc['esg_perf'][0]

        #**************************************************************** e1

        # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
        if enviro == 'n/a':
            self.score_dict['esg'].loc['e1'][0] = 1

        elif enviro >= (peer_enviro * 1.3):
            self.score_dict['esg'].loc['e1'][0] = 2

        elif enviro < (peer_enviro * 1.3) and enviro >= (peer_enviro * 0.95):
            self.score_dict['esg'].loc['e1'][0] = 1

        elif enviro < (peer_enviro * 0.95):
            self.score_dict['esg'].loc['e1'][0] = 0

        else:
            print('e1 case slipped through')

        #**************************************************************** e2

        # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
        if govern == 'n/a':
            self.score_dict['esg'].loc['e2'][0] = 1

        elif govern >= (peer_govern * 1.3):
            self.score_dict['esg'].loc['e2'][0] = 2

        elif govern < (peer_govern * 1.3) and govern >= (peer_govern * 0.95):
            self.score_dict['esg'].loc['e2'][0] = 1

        elif govern < (peer_govern * 0.95):
            self.score_dict['esg'].loc['e2'][0] = 0

        else:
            print('e2 case slipped through')

        #**************************************************************** e3

        # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
        if social == 'n/a':
            self.score_dict['esg'].loc['e3'][0] = 1

        elif social >= (peer_social * 1.3):
            self.score_dict['esg'].loc['e3'][0] = 2

        elif social < (peer_social * 1.3) and social >= (peer_social * 0.95):
            self.score_dict['esg'].loc['e3'][0] = 1

        elif social < (peer_social * 0.95):
            self.score_dict['esg'].loc['e3'][0] = 0

        else:
            print('e3 case slipped through')

        #**************************************************************** e4

        # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
        if total_esg == 'n/a':
            self.score_dict['esg'].loc['e4'][0] = 1

        elif total_esg >= (peer_total_esg * 1.2):
            self.score_dict['esg'].loc['e4'][0] = 2

        elif total_esg < (peer_total_esg * 1.2) and total_esg >= peer_total_esg:
            self.score_dict['esg'].loc['e4'][0] = 1

        elif total_esg < peer_total_esg:
            self.score_dict['esg'].loc['e4'][0] = 0

        else:
            print('e4 case slipped through')

        #**************************************************************** e5

        # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
        if esg_perf == 'n/a':
            self.score_dict['esg'].loc['e5'][0] = 1

        elif esg_perf == 'OUT_PERF':
            self.score_dict['esg'].loc['e5'][0] = 2

        elif esg_perf == 'AVG_PERF':
            self.score_dict['esg'].loc['e5'][0] = 1

        elif esg_perf == 'UNDER_PERF':
            self.score_dict['esg'].loc['e5'][0] = 0

        else:
            print('e5 case slipped through')




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

            result_list.clear()

        self.df_pub_sent = self.df_pub_sent.T

    def set_news_dfs(self):
        """Set self.div_dfs values"""

        df_com_news = pd.DataFrame({'Data N/A': 'n/a'}, index=['Company News'])
        df_sec_news = obb.common.news(self.company_list[0].df_basic.loc['sector'][0] + 'Sector News Stock Market', sort='published').head(50)
        df_ind_news = obb.common.news(self.company_list[0].df_basic.loc['industry'][0] + 'Industry News Stock Market', sort='published').head(50)

        self.news_dfs = [df_com_news, df_sec_news, df_ind_news]

    def set_analyst_data(self):
        df_rating_30d = pd.DataFrame({'Data N/A': 'n/a'}, index=['df_rating_30d']).T
        peer_df_rot_3mo = pd.DataFrame({'Strong Buy': 0, 'Buy': 0, 'Hold': 0, 'Sell': 0, 'Strong Sell': 0}, index=['Last 3mo']).T

        for company in self.company_list:
            peer_df_rot_3mo += company.analyst_data[1]

        peer_df_rot_3mo = peer_df_rot_3mo / len(self.company_list)

        self.analyst_data = [df_rating_30d, peer_df_rot_3mo]

    def set_df_esg(self):
        """Set self.df_pub_sent values"""

        result_list = []

        for metric in self.company_list[0].df_esg.index:
            for company in self.company_list:
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