# sniffer.py
#* Smelloscope Version 1.3
#* file last updated 11/22/22
"""A collection of functions used for analyzing the data in 
   Company objects.

   The master function is big_phat_whiff. It calls all sniffer 
   functions at once.

   big_phat_whiff is imported and used by scope_it_out.py
"""

def big_phat_whiff(company, peer_group):
    """Calculates scores and sets the score_card for a Company.
       Calls all sniffer.py functions in one fell swoop.
       Used by importing into scope_it_out.py

    Args:
        company (Company): An instantiated Company object
        peer_group (PeerGroup): An instantiated PeerGroup object
    """
    set_scores_value(company, peer_group)
    set_scores_mgmt(company, peer_group)
    set_scores_ins(company, peer_group)
    set_scores_div(company, peer_group)
    set_scores_pub_sent(company, peer_group)
    set_scores_analyst_data(company, peer_group)
    set_scores_esg(company, peer_group)
    set_grand_total(company)

def try_it(string, calltype, peer_group):
    
    if calltype == 'esg':

        if peer_group.df_esg.loc[string].empty:
            return 'n/a'

        else:
            try:
                if isinstance(peer_group.df_esg.loc[string][0], float):
                    return peer_group.df_esg.loc[string][0]

            except KeyError:
                return 'n/a'

    elif calltype == 'div':

        if peer_group.div_dfs[0].loc['div_ann'].empty:
            return 'n/a'

        else:
            try:
                if isinstance(peer_group.div_dfs[0].loc['div_ann'][0], float):
                    return peer_group.div_dfs[0].loc['div_ann'][0]

            except KeyError:
                return 'n/a'      

def set_cat_total(company, score_cat):
    """Calculate the total for a scoring category.
        Creates new index name and value for a "scores" dataframe.
        The value will be the sum of all points in the category.

    Args:
        score_cat (str): Should be one of: 'value', 'mgmt', 'ins', 'div', 'pub_sent', 
                                            'analyst_data', or 'esg'
    """
    index = company.score_card[score_cat].index
    i_len = len(index)
    index = index.insert(i_len, f'{score_cat[0]}Total')
    company.score_card[score_cat].loc[f'{score_cat[0]}Total'] = company.score_card[score_cat].sum()

def set_grand_total(company):
    """Gets the total from each category and sums all totals. Grand total will be added as
        value for company.score_card['grand_total']
    """
    grand_total = 0
    for key in company.score_card.keys():
        if key != 'grand_total':
            grand_total += company.score_card[key].loc[f'{key[0]}Total'][0]

    company.score_card['grand_total'] = grand_total

#*******  VALUE SCORING METHOD ******* 
def set_scores_value(company, peer_group):
    """Calculates scores for Value category

    Args:
        peer_group (PeerGroup): Custom object. Subclass of Company.
    """
    # setting VALUE metrics variables
    pe_ttm = company.df_value.loc['pe_ttm'][0]
    peer_pe_ttm = peer_group.df_value.loc['pe_ttm'][0]
    pe_5yr_avg = company.df_value.loc['pe_5yr_avg'][0]
    ptb_mrq = company.df_value.loc['ptb_mrq'][0]
    peer_ptb_mrq = peer_group.df_value.loc['ptb_mrq'][0]
    roe_ttm = company.df_mgmt.loc['roe_ttm'][0]
    peer_roe_ttm = peer_group.df_mgmt.loc['roe_ttm'][0]
    bvps_mrq = company.df_value.loc['bvps_mrq'][0]
    bvps_5yr_avg = company.df_value.loc['bvps_5yr_avg'][0]
    pfcf_ttm = company.df_value.loc['pfcf_ttm'][0]
    pfcf_5yr_avg = company.df_value.loc['pfcf_5yr_avg'][0]
    peer_pfcf_ttm = peer_group.df_value.loc['pfcf_ttm'][0]
    tca_div_tld = company.df_value.loc['tca_div_tld'][0]
    peer_tca_div_tld = peer_group.df_value.loc['tca_div_tld'][0]
    pts_ttm = company.df_value.loc['pts_ttm'][0]
    pts_5yr_avg = company.df_value.loc['pts_5yr_avg'][0]
    peer_pts_ttm = peer_group.df_value.loc['pts_ttm'][0]
    graham_mrfy = company.df_value.loc['graham_mrfy'][0]
    price = company.df_basic.loc['price'][0]
    peg = company.df_value.loc['peg'][0]

    #??---------------------------------------------------------------------- v01
    if pe_ttm == 'n/a':
        company.score_card['value'].loc['v01'][0] = 0

    elif pe_ttm <= (peer_pe_ttm * 0.9):
        company.score_card['value'].loc['v01'][0] = 2

    elif pe_ttm <= (peer_pe_ttm * 1.05):
        company.score_card['value'].loc['v01'][0] = 1

    elif pe_ttm > (peer_pe_ttm * 1.05):
        company.score_card['value'].loc['v01'][0] = 0

    else:
        print('v01 case slipped through')

    #??---------------------------------------------------------------------- v02
    if pe_ttm == 'n/a' or pe_5yr_avg == 'n/a':
        company.score_card['value'].loc['v02'][0] = 0

    elif pe_ttm <= (pe_5yr_avg * 0.75):
        company.score_card['value'].loc['v02'][0] = 3

    elif pe_ttm < (pe_5yr_avg * 0.9):
        company.score_card['value'].loc['v02'][0] = 2

    elif pe_ttm <= pe_5yr_avg:
        company.score_card['value'].loc['v02'][0] = 1

    elif pe_ttm > pe_5yr_avg:
        company.score_card['value'].loc['v02'][0] = 0

    else:
        print('v02 case slipped through')

    #??----------------------------------------------------------------------  v03
    if ptb_mrq == 'n/a' or roe_ttm == 'n/a':
        company.score_card['value'].loc['v03'][0] = 0

    elif ptb_mrq <= (peer_ptb_mrq * 0.9) and roe_ttm >= (peer_roe_ttm * 1.1):
        company.score_card['value'].loc['v03'][0] = 3

    elif ptb_mrq <= (peer_ptb_mrq * 1.05) and roe_ttm >= (peer_roe_ttm * .95):
        company.score_card['value'].loc['v03'][0] = 1

    elif ptb_mrq > (peer_ptb_mrq * 1.05) or roe_ttm < (peer_roe_ttm * .95):
        company.score_card['value'].loc['v03'][0] = 0

    else:
        print('v03 case slipped through')

    #??---------------------------------------------------------------------- v04
    if ptb_mrq == 'n/a':
        company.score_card['value'].loc['v04'][0] = 0

    elif ptb_mrq < 4:
        company.score_card['value'].loc['v04'][0] = 1

    elif ptb_mrq >= 4:
        company.score_card['value'].loc['v04'][0] = 0

    else:
        print('v04 case slipped through')

    #??---------------------------------------------------------------------- v05
    if ptb_mrq == 'n/a' or bvps_mrq == 'n/a':
        company.score_card['value'].loc['v05'][0] = 0

    elif ptb_mrq <= (peer_ptb_mrq * 0.9) and bvps_mrq > (bvps_5yr_avg * 1.1):
        company.score_card['value'].loc['v05'][0] = 2

    elif ptb_mrq <= peer_ptb_mrq and bvps_mrq >= bvps_5yr_avg:
        company.score_card['value'].loc['v05'][0] = 1

    elif ptb_mrq > peer_ptb_mrq or bvps_mrq < bvps_5yr_avg:
        company.score_card['value'].loc['v05'][0] = 0

    else:
        print('v05 case slipped through')

    #??---------------------------------------------------------------------- v06
    if pfcf_ttm == 'n/a' or pfcf_ttm < 0 or pfcf_ttm > 50:
        company.score_card['value'].loc['v06'][0] = 0

    elif pfcf_ttm <= (peer_pfcf_ttm * .9):
        company.score_card['value'].loc['v06'][0] = 2

    elif pfcf_ttm > (peer_pfcf_ttm * .9) and pfcf_ttm <= (peer_pfcf_ttm * 1.05):
        company.score_card['value'].loc['v06'][0] = 1

    elif pfcf_ttm > (peer_pfcf_ttm * 1.05):
        company.score_card['value'].loc['v06'][0] = 0

    else:
        print('v06 case slipped through')

    #??---------------------------------------------------------------------- v07
    if pfcf_ttm == 'n/a' or pfcf_5yr_avg == 'n/a':
        company.score_card['value'].loc['v07'][0] = 0

    elif pfcf_ttm <= (pfcf_5yr_avg * 0.9):
        company.score_card['value'].loc['v07'][0] = 2

    elif pfcf_ttm > (pfcf_5yr_avg * 0.9) and pfcf_ttm < (pfcf_5yr_avg * 1.05):
        company.score_card['value'].loc['v07'][0] = 1

    elif pfcf_ttm > (pfcf_5yr_avg * 1.05):
        company.score_card['value'].loc['v07'][0] = 0

    else:
        print('v07 case slipped through')

    #??---------------------------------------------------------------------- v08
    if tca_div_tld == 'n/a':
        company.score_card['value'].loc['v08'][0] = 0

    elif tca_div_tld >= 1.5:
        company.score_card['value'].loc['v08'][0] = 2

    elif tca_div_tld < 1.5 and tca_div_tld >= 1.1:
        company.score_card['value'].loc['v08'][0] = 1

    elif tca_div_tld < 1.1:
        company.score_card['value'].loc['v08'][0] = 0

    else:
        print('v08 case slipped through')

    #??---------------------------------------------------------------------- v09
    if tca_div_tld == 'n/a':
        company.score_card['value'].loc['v09'][0] = 0

    elif tca_div_tld >= (peer_tca_div_tld * 1.2):
        company.score_card['value'].loc['v09'][0] = 1

    elif tca_div_tld < (peer_tca_div_tld * 1.2):
        company.score_card['value'].loc['v09'][0] = 0

    else:
        print('v09 case slipped through')

    #??---------------------------------------------------------------------- v10

    if pts_ttm == 'n/a':
        company.score_card['value'].loc['v10'][0] = 0

    elif pts_ttm < (peer_pts_ttm * 0.8) and tca_div_tld >= 1.3:
        company.score_card['value'].loc['v10'][0] = 4

    elif pts_ttm < (peer_pts_ttm * 0.9) and tca_div_tld >= 1.3:
        company.score_card['value'].loc['v10'][0] = 3

    elif pts_ttm < (peer_pts_ttm * 0.9) and tca_div_tld >= 1.1:
        company.score_card['value'].loc['v10'][0] = 2

    elif pts_ttm < peer_pts_ttm and tca_div_tld >= 1:
        company.score_card['value'].loc['v10'][0] = 1

    elif pts_ttm > peer_pts_ttm or tca_div_tld < 1:
        company.score_card['value'].loc['v10'][0] = 0

    else:
        print('v10 case slipped through')

    #?---------------------------------------------------------------------- v11
    if pts_ttm == 'n/a' or pts_5yr_avg == 'n/a':
        company.score_card['value'].loc['v11'][0] = 0

    elif pts_ttm <= (pts_5yr_avg * 0.8):
        company.score_card['value'].loc['v11'][0] = 2

    elif pts_ttm > (pts_5yr_avg * 0.8) and pts_ttm < pts_5yr_avg:
        company.score_card['value'].loc['v11'][0] = 1

    elif pts_ttm > pts_5yr_avg:
        company.score_card['value'].loc['v11'][0] = 0

    else:
        print('v11 case slipped through')

    #?---------------------------------------------------------------------- v12
    if graham_mrfy == 'n/a':
        company.score_card['value'].loc['v12'][0] = 0

    elif graham_mrfy >= price:
        company.score_card['value'].loc['v12'][0] = 2

    elif graham_mrfy < price and graham_mrfy >= (price * 0.8):
        company.score_card['value'].loc['v12'][0] = 1

    elif graham_mrfy < (price * 0.8):
        company.score_card['value'].loc['v12'][0] = 0

    else:
        print('v12 case slipped through')

    #?---------------------------------------------------------------------- v13
    if peg == 'n/a':
        company.score_card['value'].loc['v13'][0] = 0

    elif peg <= 1 and peg > 0:
        company.score_card['value'].loc['v13'][0] = 3

    elif peg > 1 and peg <= 1.8:
        company.score_card['value'].loc['v13'][0] = 1

    elif peg > 1.8:
        company.score_card['value'].loc['v13'][0] = 0

    else:
        print('v13 case slipped through')

    #??---------------------------------------------------------------------- vTotal
    set_cat_total(company, 'value')
    

#*******  MANAGEMENT SCORING METHOD ******* 
def set_scores_mgmt(company, peer_group):

    # setting MANAGEMENT variables for ease of reading
    roa_ttm = company.df_mgmt.loc['roa_ttm'][0]
    peer_roa_ttm = peer_group.df_mgmt.loc['roa_ttm'][0]
    roa_5yr_avg = company.df_mgmt.loc['roa_5yr_avg'][0]
    roe_ttm = company.df_mgmt.loc['roe_ttm'][0]
    peer_roe_ttm = peer_group.df_mgmt.loc['roe_ttm'][0]
    roe_5yr_avg = company.df_mgmt.loc['roe_5yr_avg'][0]
    dte_mrq = company.df_mgmt.loc['dte_mrq'][0]
    peer_dte_mrq = peer_group.df_mgmt.loc['dte_mrq'][0]
    dte_5yr_avg = company.df_mgmt.loc['dte_5yr_avg'][0]

    npm_mrfy = company.df_mgmt.loc['npm_mrfy'][0]
    npm_5yr_avg = company.df_mgmt.loc['npm_5yr_avg'][0]
    peer_npm_mrfy = peer_group.df_mgmt.loc['npm_mrfy'][0]
    opm_mrfy = company.df_mgmt.loc['opm_mrfy'][0]
    opm_5yr_avg = company.df_mgmt.loc['opm_5yr_avg'][0]
    peer_opm_mrfy = peer_group.df_mgmt.loc['opm_mrfy'][0]
    gpm_mrfy = company.df_mgmt.loc['gpm_mrfy'][0]
    gpm_5yr_avg = company.df_mgmt.loc['gpm_5yr_avg'][0]
    peer_gpm_mrfy = peer_group.df_mgmt.loc['gpm_mrfy'][0]

    cr_mrq = company.df_mgmt.loc['cr_mrq'][0]
    cr_5yr_avg = company.df_mgmt.loc['cr_5yr_avg'][0]
    peer_cr_mrq = peer_group.df_mgmt.loc['cr_mrq'][0]

    #??---------------------------------------------------------------------- m01

    if roa_ttm == 'n/a':
        company.score_card['mgmt'].loc['m01'][0] = 0

    elif roa_ttm >= (peer_roa_ttm * 1.3):
        company.score_card['mgmt'].loc['m01'][0] = 3

    elif roa_ttm < (peer_roa_ttm * 1.3) and roa_ttm >= (peer_roa_ttm * 1.1):
        company.score_card['mgmt'].loc['m01'][0] = 2

    elif roa_ttm < (peer_roa_ttm * 1.1) and roa_ttm >= peer_roa_ttm:
        company.score_card['mgmt'].loc['m01'][0] = 1

    elif roa_ttm < peer_roa_ttm:
        company.score_card['mgmt'].loc['m01'][0] = 0

    else:
        print('m01 case slipped through')

    #??---------------------------------------------------------------------- m02

    if roa_ttm == 'n/a':
        company.score_card['mgmt'].loc['m02'][0] = 0

    elif roa_ttm > (roa_5yr_avg * 1.2):
        company.score_card['mgmt'].loc['m02'][0] = 3

    elif roa_ttm <= (roa_5yr_avg * 1.2) and roa_ttm >= roa_5yr_avg:
        company.score_card['mgmt'].loc['m02'][0] = 1

    elif roa_ttm < roa_5yr_avg:
        company.score_card['mgmt'].loc['m02'][0] = 0

    else:
        print('m02 case slipped through')

    #??---------------------------------------------------------------------- m03

    if roe_ttm == 'n/a':
        company.score_card['mgmt'].loc['m03'][0] = 0

    elif roe_ttm >= (peer_roe_ttm * 1.2):
        company.score_card['mgmt'].loc['m03'][0] = 2

    elif roe_ttm < (peer_roe_ttm * 1.2) and roe_ttm >= (peer_roe_ttm * 1.05):
        company.score_card['mgmt'].loc['m03'][0] = 1

    elif roe_ttm < (peer_roe_ttm * 1.05):
        company.score_card['mgmt'].loc['m03'][0] = 0

    else:
        print('m03 case slipped through')

    #??---------------------------------------------------------------------- m04

    if roe_ttm == 'n/a' or roe_5yr_avg == 'n/a':
        company.score_card['mgmt'].loc['m04'][0] = 0

    elif roe_ttm > (roe_5yr_avg * 1.2):
        company.score_card['mgmt'].loc['m04'][0] = 2

    elif roe_ttm <= (roe_5yr_avg * 1.2) and roe_ttm >= roe_5yr_avg:
        company.score_card['mgmt'].loc['m04'][0] = 1

    elif roe_ttm < roe_5yr_avg:
        company.score_card['mgmt'].loc['m04'][0] = 0

    else:
        print('m04 case slipped through')

    #??---------------------------------------------------------------------- m05

    if dte_mrq == 'n/a' or dte_5yr_avg == 'n/a':
        company.score_card['mgmt'].loc['m05'][0] = 0

    elif dte_mrq <= (dte_5yr_avg * 0.95):
        company.score_card['mgmt'].loc['m05'][0] = 1

    elif dte_mrq > (dte_5yr_avg * 0.95):
        company.score_card['mgmt'].loc['m05'][0] = 0

    else:
        print('m05 case slipped through')

    #??---------------------------------------------------------------------- m06

    if dte_mrq == 'n/a':
        company.score_card['mgmt'].loc['m06'][0] = 0

    elif dte_mrq <= (peer_dte_mrq * 0.95):
        company.score_card['mgmt'].loc['m06'][0] = 1

    elif dte_mrq > (peer_dte_mrq * 0.95):
        company.score_card['mgmt'].loc['m06'][0] = 0

    else:
        print('m06 case slipped through')

    #??---------------------------------------------------------------------- m07

    if npm_mrfy == 'n/a':
        company.score_card['mgmt'].loc['m07'][0] = 0

    elif npm_mrfy > (npm_5yr_avg * 1.2):
        company.score_card['mgmt'].loc['m07'][0] = 3

    elif npm_mrfy <= (npm_5yr_avg * 1.2) and npm_mrfy >= (npm_5yr_avg * 1.05):
        company.score_card['mgmt'].loc['m07'][0] = 1

    elif npm_mrfy < (npm_5yr_avg * 1.05):
        company.score_card['mgmt'].loc['m07'][0] = 0

    else:
        print('m07 case slipped through')

    #??---------------------------------------------------------------------- m08

    if npm_mrfy == 'n/a':
        company.score_card['mgmt'].loc['m08'][0] = 0

    elif npm_mrfy >= (peer_npm_mrfy * 1.2):
        company.score_card['mgmt'].loc['m08'][0] = 2

    elif npm_mrfy < (peer_npm_mrfy * 1.2) and npm_mrfy >= peer_npm_mrfy:
        company.score_card['mgmt'].loc['m08'][0] = 1

    elif npm_mrfy < peer_npm_mrfy:
        company.score_card['mgmt'].loc['m08'][0] = 0

    else:
        print('m08 case slipped through')

    #??---------------------------------------------------------------------- m09

    if opm_mrfy == 'n/a':
        company.score_card['mgmt'].loc['m09'][0] = 0

    elif opm_mrfy >= (opm_5yr_avg * 1.1):
        company.score_card['mgmt'].loc['m09'][0] = 1

    elif opm_mrfy < (opm_5yr_avg * 1.1):
        company.score_card['mgmt'].loc['m09'][0] = 0

    else:
        print('m09 case slipped through')

    #??---------------------------------------------------------------------- m10

    if gpm_mrfy == 'n/a':
        company.score_card['mgmt'].loc['m10'][0] = 0

    elif gpm_mrfy > (gpm_5yr_avg * 1.1):
        company.score_card['mgmt'].loc['m10'][0] = 1

    elif gpm_mrfy <= (gpm_5yr_avg * 1.1):
        company.score_card['mgmt'].loc['m10'][0] = 0

    else:
        print('m10 case slipped through')

    #??---------------------------------------------------------------------- m11

    if cr_mrq == 'n/a':
        company.score_card['mgmt'].loc['m11'][0] = 0

    elif cr_mrq >= 1.2 and cr_mrq <= 2:
        company.score_card['mgmt'].loc['m11'][0] = 2

    elif cr_mrq < 1.2 and cr_mrq >= 1 or cr_mrq > 2 and cr_mrq <= 3:
        company.score_card['mgmt'].loc['m11'][0] = 1

    elif cr_mrq < 1 or cr_mrq > 3:
        company.score_card['mgmt'].loc['m11'][0] = 0

    else:
        print('m11 case slipped through')

    #??---------------------------------------------------------------------- m12

    if cr_mrq == 'n/a':
        company.score_card['mgmt'].loc['m12'][0] = 0

    elif cr_mrq <= (peer_cr_mrq * 1.2) and cr_mrq >= (peer_cr_mrq * 0.9):
        company.score_card['mgmt'].loc['m12'][0] = 1

    elif cr_mrq > (peer_cr_mrq * 1.2) or cr_mrq < (peer_cr_mrq * 0.9):
        company.score_card['mgmt'].loc['m12'][0] = 0

    else:
        print('m12 case slipped through')

    #??---------------------------------------------------------------------- m13

    if cr_mrq == 'n/a':
        company.score_card['mgmt'].loc['m13'][0] = 0

    elif cr_mrq <= (cr_5yr_avg * 1.2) and cr_mrq >= (cr_5yr_avg * 0.9):
        company.score_card['mgmt'].loc['m13'][0] = 1

    elif cr_mrq > (cr_5yr_avg * 1.2) or cr_mrq < (cr_5yr_avg * 0.9):
        company.score_card['mgmt'].loc['m13'][0] = 0

    else:
        print('m13 case slipped through')


    #??---------------------------------------------------------------------- mTotal
    set_cat_total(company, 'mgmt')

#*******  INSIDER & INSTITUION SCORING METHOD ******* 
def set_scores_ins(company, peer_group):

    io = company.df_ins.loc['io'][0]
    peer_io = peer_group.df_ins.loc['io'][0]
    it = company.df_ins.loc['it'][0]
    peer_it = peer_group.df_ins.loc['it'][0]
    inst_t = company.df_ins.loc['inst_t'][0]

    #??---------------------------------------------------------------------- i01

    if io == 'n/a':
        company.score_card['ins'].loc['i01'][0] = 0

    elif io >= (peer_io * 1.5):
        company.score_card['ins'].loc['i01'][0] = 2

    elif io < (peer_io * 1.5) and io >= (peer_io * 1.05):
        company.score_card['ins'].loc['i01'][0] = 1

    elif io < (peer_io * 1.05):
        company.score_card['ins'].loc['i01'][0] = 0

    else:
        print('i01 case slipped through')

    #??---------------------------------------------------------------------- i02

    if io == 'n/a':
        company.score_card['ins'].loc['i02'][0] = 0

    elif io >= 0.1:
        company.score_card['ins'].loc['i02'][0] = 3

    elif io < 0.1 and io >= .05:
        company.score_card['ins'].loc['i02'][0] = 2

    elif io < 0.05 and io >= 0.01:
        company.score_card['ins'].loc['i02'][0] = 1

    elif io < 0.01:
        company.score_card['ins'].loc['i02'][0] = 0

    else:
        print('i02 case slipped through')

    #??---------------------------------------------------------------------- i03

    if it == 'n/a':
        company.score_card['ins'].loc['i03'][0] = 0

    elif it >= 0.03:
        company.score_card['ins'].loc['i03'][0] = 5

    elif it < 0.03 and it >= 0.015:
        company.score_card['ins'].loc['i03'][0] = 3

    elif it < 0.015 and it >= 0:
        company.score_card['ins'].loc['i03'][0] = 1

    elif it < 0:
        company.score_card['ins'].loc['i03'][0] = 0

    else:
        print('i03 case slipped through')

    #??---------------------------------------------------------------------- i04

    if inst_t == 'n/a':
        company.score_card['ins'].loc['i04'][0] = 0

    elif inst_t >= 0.02:
        company.score_card['ins'].loc['i04'][0] = 1

    elif inst_t < 0.02:
        company.score_card['ins'].loc['i04'][0] = 0

    else:
        print('i04 case slipped through')

    #??---------------------------------------------------------------------- iTotal
    set_cat_total(company, 'ins')

#*******  DIVIDEND SCORING METHOD ******* 
def set_scores_div(company, peer_group):

    div_ann = company.div_dfs[0].loc['div_ann'][0]
    peer_div_ann = try_it('div_ann', 'div', peer_group)
    div_y_mrfy = company.div_dfs[0].loc['div_y_mrfy'][0]
    peer_div_y_mrfy = try_it('div_y_mrfy', 'div', peer_group)

    try: # The amount of the most recent dividend
        last_div = company.div_dfs[1].tail(1)['Dividends'][0]

    except ValueError:
        last_div = 'n/a'

    except AttributeError:
        last_div = 'n/a'

    try: # The average of the last 12 dividends
        last12_avg = company.div_dfs[1].tail(12).mean(axis=0)[0]

    except ValueError:
        last12_avg = 'n/a'

    except AttributeError:
        last12_avg = 'n/a'

    #??---------------------------------------------------------------------- d01

    # setting 'n/a' to 1 so as not to penalize companies who have no div
    if div_ann == 'n/a' or peer_div_ann == 'n/a':
        company.score_card['div'].loc['d01'][0] = 1

    elif div_ann >= (peer_div_ann * 1.2):
        company.score_card['div'].loc['d01'][0] = 2

    elif div_ann < (peer_div_ann * 1.2) and div_ann >= peer_div_ann:
        company.score_card['div'].loc['d01'][0] = 1

    elif div_ann < peer_div_ann:
        company.score_card['div'].loc['d01'][0] = 0

    else:
        print('d01 case slipped through')



    #??---------------------------------------------------------------------- d02

    # setting 'n/a' to 1 so as not to penalize companies who have no div
    if last_div == 'n/a' or last12_avg == 'n/a':
        company.score_card['div'].loc['d02'][0] = 1

    elif last_div >= (last12_avg * 1.2):
        company.score_card['div'].loc['d02'][0] = 2

    elif last_div < (last12_avg * 1.2) and last_div >= last12_avg:
        company.score_card['div'].loc['d02'][0] = 1

    elif last_div < last12_avg:
        company.score_card['div'].loc['d02'][0] = 0

    else:
        print('d02 case slipped through')

    #??---------------------------------------------------------------------- d03

    # setting 'n/a' to 1 so as not to penalize companies who have no div
    if div_y_mrfy == 'n/a' or peer_div_y_mrfy == 'n/a':
        company.score_card['div'].loc['d03'][0] = 1

    elif div_y_mrfy >= (peer_div_y_mrfy * 1.2):
        company.score_card['div'].loc['d03'][0] = 2

    elif div_y_mrfy < (peer_div_y_mrfy * 1.2) and div_y_mrfy >= peer_div_y_mrfy:
        company.score_card['div'].loc['d03'][0] = 1

    elif div_y_mrfy < peer_div_y_mrfy:
        company.score_card['div'].loc['d03'][0] = 0

    else:
        print('d03 case slipped through')

    #??---------------------------------------------------------------------- d04

    if div_y_mrfy == 'n/a':
        company.score_card['div'].loc['d04'][0] = 1

    elif div_y_mrfy >= .02:
        company.score_card['div'].loc['d04'][0] = 2

    elif div_y_mrfy < .02 and div_y_mrfy >= .0075:
        company.score_card['div'].loc['d04'][0] = 1

    elif div_y_mrfy < .0075:
        company.score_card['div'].loc['d04'][0] = 0

    else:
        print('d04 case slipped through')

    #??---------------------------------------------------------------------- dTotal
    set_cat_total(company, 'div')

#*******  PUBLIC SENTIMENT SCORING METHOD ***
def set_scores_pub_sent(company, peer_group):

    twits_perc = company.df_pub_sent.loc['twits_perc'][0]
    peer_twits_perc = peer_group.df_pub_sent.loc['twits_perc'][0]
    shrt_int = company.df_pub_sent.loc['shrt_int'][0]
    peer_shrt_int = peer_group.df_pub_sent.loc['shrt_int'][0]
    news_sent = company.df_pub_sent.loc['news_sent'][0]
    peer_news_sent = peer_group.df_pub_sent.loc['news_sent'][0]

    #??---------------------------------------------------------------------- p01

    if twits_perc == 'n/a':
        company.score_card['pub_sent'].loc['p01'][0] = 0

    elif twits_perc >= .8:
        company.score_card['pub_sent'].loc['p01'][0] = 1

    elif twits_perc < .8:
        company.score_card['pub_sent'].loc['p01'][0] = 0

    else:
        print('p01 case slipped through')

    #??---------------------------------------------------------------------- p02

    if twits_perc == 'n/a':
        company.score_card['pub_sent'].loc['p02'][0] = 0

    elif twits_perc >= (peer_twits_perc * 1.1):
        company.score_card['pub_sent'].loc['p02'][0] = 1

    elif twits_perc < (peer_twits_perc * 1.1):
        company.score_card['pub_sent'].loc['p02'][0] = 0

    else:
        print('p02 case slipped through')

    #??---------------------------------------------------------------------- p03

    if shrt_int == 'n/a':
        company.score_card['pub_sent'].loc['p03'][0] = 0

    elif shrt_int <= 0.01:
        company.score_card['pub_sent'].loc['p03'][0] = 2

    elif shrt_int > 0.01 and shrt_int <= 0.02:
        company.score_card['pub_sent'].loc['p03'][0] = 1

    elif shrt_int > 0.02:
        company.score_card['pub_sent'].loc['p03'][0] = 0

    else:
        print('p03 case slipped through')

    #??---------------------------------------------------------------------- p04

    if shrt_int == 'n/a':
        company.score_card['pub_sent'].loc['p04'][0] = 0

    elif shrt_int <= (peer_shrt_int * 0.9):
        company.score_card['pub_sent'].loc['p04'][0] = 2

    elif shrt_int > (peer_shrt_int * 0.9) and shrt_int <= (peer_shrt_int * 1.05):
        company.score_card['pub_sent'].loc['p04'][0] = 1

    elif shrt_int > (peer_shrt_int * 1.05):
        company.score_card['pub_sent'].loc['p04'][0] = 0

    else:
        print('p04 case slipped through')

    #??---------------------------------------------------------------------- p05

    if news_sent == 'n/a':
        company.score_card['pub_sent'].loc['p05'][0] = 0

    elif news_sent >= 0.25:
        company.score_card['pub_sent'].loc['p05'][0] = 1

    elif news_sent < 0.25:
        company.score_card['pub_sent'].loc['p05'][0] = 0

    else:
        print('p05 case slipped through')

    #??---------------------------------------------------------------------- p06

    if news_sent == 'n/a':
        company.score_card['pub_sent'].loc['p06'][0] = 0

    elif news_sent >= (peer_news_sent * 1.05):
        company.score_card['pub_sent'].loc['p06'][0] = 1

    elif news_sent < (peer_news_sent * 1.05):
        company.score_card['pub_sent'].loc['p06'][0] = 0

    else:
        print('p06 case slipped through')

    #??---------------------------------------------------------------------- pTotal
    set_cat_total(company, 'pub_sent')

#*******  ANALYST DATA SCORING METHOD *****
def set_scores_analyst_data(company, peer_group):

    wghtd_buys_sum = company.analyst_data[1].loc['Buy'][0] + (company.analyst_data[1].loc['Strong Buy'][0] * 1.25)
    wghtd_peer_buys_sum = peer_group.analyst_data[1].loc['Buy'][0] + (peer_group.analyst_data[1].loc['Strong Buy'][0] * 1.25)
    holds = company.analyst_data[1].loc['Hold'][0]
    peer_holds = peer_group.analyst_data[1].loc['Hold'][0]
    wghtd_sells_sum = company.analyst_data[1].loc['Sell'][0] + (company.analyst_data[1].loc['Strong Sell'][0] * 1.25)
    wghtd_peer_sells_sum = peer_group.analyst_data[1].loc['Sell'][0] + (peer_group.analyst_data[1].loc['Strong Sell'][0] * 1.25)

    buys_perc = wghtd_buys_sum / (wghtd_buys_sum + holds + wghtd_sells_sum)
    peer_buys_perc = wghtd_peer_buys_sum / (wghtd_peer_buys_sum + peer_holds + wghtd_peer_sells_sum)
    sells_perc = wghtd_sells_sum / (wghtd_buys_sum + holds + wghtd_sells_sum)
    peer_sells_perc = wghtd_peer_sells_sum / (wghtd_peer_buys_sum + peer_holds + wghtd_peer_sells_sum)

    series_last_14 = company.analyst_data[0]['Rating'].head(14)
    
    #counting how many Strong Buy ratings have been issued in last 14 days
    strong_buys = 0
    for rating in series_last_14:
        if rating == 'Strong Buy':
            strong_buys += 1

    wb_score = company.analyst_data[2]
    fwd_pe = company.analyst_data[3]
    pe_ttm = company.df_value.loc['pe_ttm'][0]

    #??---------------------------------------------------------------------- a01

    if buys_perc == 'n/a':
        company.score_card['analyst_data'].loc['a01'][0] = 0

    elif buys_perc >= (peer_buys_perc * 1.05):
        company.score_card['analyst_data'].loc['a01'][0] = 1

    elif buys_perc < (peer_buys_perc * 1.05):
        company.score_card['analyst_data'].loc['a01'][0] = 0

    else:
        print('a01 case slipped through')

    #??---------------------------------------------------------------------- a02

    if sells_perc == 'n/a':
        company.score_card['analyst_data'].loc['a02'][0] = 0

    elif sells_perc <= (peer_sells_perc * .95):
        company.score_card['analyst_data'].loc['a02'][0] = 1

    elif sells_perc > (peer_sells_perc * .95):
        company.score_card['analyst_data'].loc['a02'][0] = 0

    else:
        print('a02 case slipped through')

    #??---------------------------------------------------------------------- a03

    if wghtd_buys_sum == 'n/a':
        company.score_card['analyst_data'].loc['a03'][0] = 0

    elif wghtd_buys_sum >= (wghtd_peer_buys_sum * 1.5):
        company.score_card['analyst_data'].loc['a03'][0] = 2

    elif wghtd_buys_sum < (wghtd_peer_buys_sum * 1.5) and wghtd_buys_sum >= (wghtd_peer_buys_sum * 1.1):
        company.score_card['analyst_data'].loc['a03'][0] = 1

    elif wghtd_buys_sum < (wghtd_peer_buys_sum * 1.1):
        company.score_card['analyst_data'].loc['a03'][0] = 0

    else:
        print('a03 case slipped through')

    #??---------------------------------------------------------------------- a04

    if strong_buys == 'n/a':
        company.score_card['analyst_data'].loc['a04'][0] = 0

    elif strong_buys >= 10:
        company.score_card['analyst_data'].loc['a04'][0] = 2

    elif strong_buys < 10 and strong_buys >= 8:
        company.score_card['analyst_data'].loc['a04'][0] = 1

    elif strong_buys < 8:
        company.score_card['analyst_data'].loc['a04'][0] = 0

    else:
        print('a04 case slipped through')

    #??---------------------------------------------------------------------- a05

    # Scoring 'n/a' as worth 1pt so as not to punish those not on S&P or NASDAQ 100
    if wb_score == 'n/a':
        company.score_card['analyst_data'].loc['a05'][0] = 1

    elif wb_score >= 80:
        company.score_card['analyst_data'].loc['a05'][0] = 2

    elif wb_score < 80 and wb_score >= 75:
        company.score_card['analyst_data'].loc['a05'][0] = 1

    elif wb_score < 75:
        company.score_card['analyst_data'].loc['a05'][0] = 0

    else:
        print('a05 case slipped through')

    #??---------------------------------------------------------------------- a06

    if fwd_pe == 'n/a' or pe_ttm == 'n/a':
        company.score_card['analyst_data'].loc['a06'][0] = 0

    elif fwd_pe <=  (pe_ttm * 0.8):
        company.score_card['analyst_data'].loc['a06'][0] = 2

    elif fwd_pe >= (pe_ttm * 0.8) and fwd_pe <= (pe_ttm * 0.95):
        company.score_card['analyst_data'].loc['a06'][0] = 1

    elif fwd_pe > (pe_ttm * 0.95):
        company.score_card['analyst_data'].loc['a06'][0] = 0

    else:
        print('a06 case slipped through')

    #??---------------------------------------------------------------------- aTotal
    set_cat_total(company, 'analyst_data')

#*******  ESG SCORING METHOD ************** 
def set_scores_esg(company, peer_group):

    enviro = company.df_esg.loc['enviro'][0]
    peer_enviro = try_it('enviro', 'esg', peer_group)
    govern = company.df_esg.loc['govern'][0]
    peer_govern = try_it('govern', 'esg', peer_group)
    social = company.df_esg.loc['social'][0]
    peer_social = try_it('social', 'esg', peer_group)
    total_esg = company.df_esg.loc['total_esg'][0]
    peer_total_esg = try_it('total_esg', 'esg', peer_group)
    esg_perf = company.df_esg.loc['esg_perf'][0]

    #?---------------------------------------------------------------------- e01

    # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
    if enviro == 'n/a':
        company.score_card['esg'].loc['e01'][0] = 0.5

    elif enviro <= (peer_enviro * 0.8):
        company.score_card['esg'].loc['e01'][0] = 2

    elif enviro > (peer_enviro * 0.8) and enviro <= (peer_enviro * 1.05):
        company.score_card['esg'].loc['e01'][0] = 1

    elif enviro > (peer_enviro * 1.05):
        company.score_card['esg'].loc['e01'][0] = 0

    else:
        print('e01 case slipped through')

    #?---------------------------------------------------------------------- e02

    # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
    if govern == 'n/a':
        company.score_card['esg'].loc['e02'][0] = 0.5

    elif govern <= (peer_govern * 0.8):
        company.score_card['esg'].loc['e02'][0] = 2

    elif govern > (peer_govern * 0.8) and govern <= (peer_govern * 1.05):
        company.score_card['esg'].loc['e02'][0] = 1

    elif govern > (peer_govern * 1.05):
        company.score_card['esg'].loc['e02'][0] = 0

    else:
        print('e02 case slipped through')

    #?---------------------------------------------------------------------- e03

    # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
    if social == 'n/a':
        company.score_card['esg'].loc['e03'][0] = 0.5

    elif social <= (peer_social * 0.8):
        company.score_card['esg'].loc['e03'][0] = 2

    elif social > (peer_social * 0.8) and social <= (peer_social * 1.05):
        company.score_card['esg'].loc['e03'][0] = 1

    elif social > (peer_social * 1.05):
        company.score_card['esg'].loc['e03'][0] = 0

    else:
        print('e03 case slipped through')

    #?---------------------------------------------------------------------- e04

    # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
    if total_esg == 'n/a':
        company.score_card['esg'].loc['e04'][0] = 0.5

    elif total_esg <= (peer_total_esg * 0.8):
        company.score_card['esg'].loc['e04'][0] = 2

    elif total_esg > (peer_total_esg * 0.8) and total_esg <= peer_total_esg:
        company.score_card['esg'].loc['e04'][0] = 1

    elif total_esg > peer_total_esg:
        company.score_card['esg'].loc['e04'][0] = 0

    else:
        print('e04 case slipped through')

    #?---------------------------------------------------------------------- e05

    # Scoring 'n/a' as worth 1pt so as not to punish those who do not have ratings
    if esg_perf == 'n/a':
        company.score_card['esg'].loc['e05'][0] = 1

    elif esg_perf == 'LAG_PERF' or esg_perf == 'UNDER_PERF':
        company.score_card['esg'].loc['e05'][0] = 2

    elif esg_perf == 'AVG_PERF':
        company.score_card['esg'].loc['e05'][0] = 1

    elif esg_perf == 'OUT_PERF' or esg_perf == 'LEAD_PERF':
        company.score_card['esg'].loc['e05'][0] = 0

    else:
        print('e05 case slipped through')

    #?---------------------------------------------------------------------- eTotal
    set_cat_total(company, 'esg')