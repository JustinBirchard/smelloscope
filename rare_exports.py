# rare_exports.py
#* Version 0.9.9.3
#* last updated 11/11/22

import datetime
import gspread
from gspread_formatting import *
from time import sleep
gc = gspread.service_account(filename='smelloscope-bf9b919f41a7.json')
today = str(datetime.date.today())

ws_metrics = None
ws_scores = None

# for column headers in Metrics
fmt1 = CellFormat(
    backgroundColor=Color(0.7, 0.9, 1),
    textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
    #horizontalAlignment='CENTER'
    )

fmt_bold_italic = CellFormat(
    textFormat=TextFormat(bold=True, italic=True)
    )

fmt_black_background = CellFormat(
    backgroundColor=Color(0, 0, 0)
    )

fmt_blue_background = CellFormat(
    backgroundColor=Color(0.7, 0.9, 1)
    )

fmt_grey_background = CellFormat(
    backgroundColor=Color(0.97, 0.97, 0.97)
    )

def gs_export(tick, companies, peer_group):
    """Calls all gs functions and creates the Google Sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
    """
    gs_create(tick)
    gs_scores(tick, companies, peer_group, ws_scores)
# Uncomment when done with scores page:    gs_metrics(tick, companies, peer_group, ws_metrics)

def gs_create(tick):
    """Creates Google Spreadsheet, initializes Worksheets,
       and shares via email.

    Args:
        tick (str): ticker of company
    """
    global ws_scores, ws_metrics # need these vars to be global
    sh = gc.create(f'{tick} {today}') # creating spreadsheet object
    print(f'Creating Google Spreadsheet called: "{tick} {today}"')

    # sharing via email
    sh.share('ssrjustin@gmail.com', perm_type='user', role='writer')

    # Adding worksheets
    ws_scores = sh.add_worksheet(title="Scores", rows=100, cols=14)
    ws_metrics = sh.add_worksheet(title="Metrics", rows=36, cols=7)

    # deleting blank sheet that gets created when creating a spreadsheet
    ws2 = sh.get_worksheet(0)
    sh.del_worksheet(ws2)


def gs_metrics(tick, companies, peer_group, ws_metrics):
    """Pulls in data and formats the "Metrics" sheet.
       Google allows 1 call/sec

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        ws_metrics (WorkSheet): gspread WorkSheet object
    """
    print('Now creating "Metrics" sheet.')
    price = companies[tick].df_basic.loc['price'][0]
    
    # Setting up header for the sheet which is just "price" & the value
    ws_metrics.update('A1', 'Price')
    ws_metrics.update('B1', price)

    # Exporting Value header names, stat names, and values
    ws_metrics.update('A3', 'Value')
    ws_metrics.update('B3', tick)
    ws_metrics.update('C3', 'Peer Avg')
    sleep(5)

    for i, name in enumerate(companies[tick].df_value.index):
        value = companies[tick].df_value.loc[name][0]
        ws_metrics.update(f'A{i + 4}', name)
        ws_metrics.update(f'B{i + 4}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_value.index):
        value = peer_group.df_value.loc[name][0]
        ws_metrics.update(f'C{i + 4}', value)
        sleep(1)
    print('Value stats exported to "Metrics" sheet.')

    # Exporting Management header names, stat names, and values
    ws_metrics.update('E3', 'Management')
    ws_metrics.update('F3', tick)
    ws_metrics.update('G3', 'Peer Avg')
    sleep(3)

    for i, name in enumerate(companies[tick].df_mgmt.index):
        value = companies[tick].df_mgmt.loc[name][0]
        ws_metrics.update(f'E{i + 4}', name)
        ws_metrics.update(f'F{i + 4}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_mgmt.index):
        value = peer_group.df_mgmt.loc[name][0]
        ws_metrics.update(f'G{i + 4}', value)
        sleep(1)  
    print('Management stats exported to "Metrics" sheet.')

    # Exporting Ins & Inst header names, stat names, and values
    ws_metrics.update('A25', 'Ins & Inst')
    ws_metrics.update('B25', tick)
    ws_metrics.update('C25', 'Peer Avg')
    sleep(3)

    for i, name in enumerate(companies[tick].df_ins.index):
        value = companies[tick].df_ins.loc[name][0]
        ws_metrics.update(f'A{i + 26}', name)
        ws_metrics.update(f'B{i + 26}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_ins.index):
        value = peer_group.df_ins.loc[name][0]
        ws_metrics.update(f'C{i + 26}', value)
        sleep(1)
    print('Ins & Inst stats exported to "Metrics" sheet.')

    # Exporting Dividend header names, stat names, and values
    ws_metrics.update('E23', 'Dividend')
    ws_metrics.update('F23', tick)
    ws_metrics.update('G23', 'Peer Avg')
    sleep(3)

    for i, name in enumerate(companies[tick].div_dfs[0].index):
        value = companies[tick].div_dfs[0].loc[name][0]
        ws_metrics.update(f'E{i + 24}', name)
        ws_metrics.update(f'F{i + 24}', value)
        sleep(2)

    if not peer_group.div_dfs[0].empty:
        for i, name in enumerate(companies[tick].div_dfs[0].index):
            value = peer_group.div_dfs[0].loc[name]
            ws_metrics.update(f'G{i + 24}', value[0])
            sleep(2)
            
    else:
        ws_metrics.update('G24', 'n/a')
        ws_metrics.update('G25', 'n/a')
        sleep(2)
    print('Dividend stats exported to "Metrics" sheet.')
    
    # Exporting Pub Sent header names, stat names, and values
    ws_metrics.update('A31', 'Pub Sent')
    ws_metrics.update('B31', tick)
    ws_metrics.update('C31', 'Peer Avg')
    sleep(3)

    for i, name in enumerate(companies[tick].df_pub_sent.index):
        value = companies[tick].df_pub_sent.loc[name][0]
        ws_metrics.update(f'A{i + 32}', name)
        ws_metrics.update(f'B{i + 32}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_pub_sent.index):
        value = peer_group.df_pub_sent.loc[name][0]
        ws_metrics.update(f'C{i + 32}', value)
        sleep(1)
    print('Public Sentiment stats exported to "Metrics" sheet.')

    # Exporting Pub Sent header names, stat names, and values
    ws_metrics.update('E27', 'Analyst')
    ws_metrics.update('F27', tick)
    ws_metrics.update('G27', 'Peer Avg')
    sleep(3)
    ws_metrics.update('E28', 'wb_score')
    ws_metrics.update('F28', companies[tick].analyst_data[2])
    ws_metrics.update('E29', 'fwd_pe')
    ws_metrics.update('F29', companies[tick].analyst_data[3])
    ws_metrics.update('G28', peer_group.analyst_data[2])
    ws_metrics.update('G29', peer_group.analyst_data[3])
    sleep(6)
    print('Analyst stats exported to "Metrics" sheet.')

    # Exporting ESG header names, stat names, and values
    ws_metrics.update('E31', 'ESG')
    ws_metrics.update('F31', tick)
    ws_metrics.update('G31', 'Peer Avg')
    sleep(3)

    for i, name in enumerate(companies[tick].df_esg.index):
        value = companies[tick].df_esg.loc[name][0]
        ws_metrics.update(f'E{i + 32}', name)
        ws_metrics.update(f'F{i + 32}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_esg.index):
        value = peer_group.df_esg.loc[name][0]
        ws_metrics.update(f'G{i + 32}', value)
        sleep(1)
    print('ESG stats exported to "Metrics" sheet.')

    format_cell_range(ws_metrics, 'A1:A36', fmt_bold_italic)
    format_cell_range(ws_metrics, 'E1:E36', fmt_bold_italic)
    sleep(2)
    print('Gussying up the "Metrics" sheet.')

    format_cell_range(ws_metrics, 'A3:G3', fmt1)
    set_column_width(ws_metrics, 'D', 20)
    sleep(2)
    format_cell_range(ws_metrics, 'D3:D36', fmt_blue_background)
    format_cell_range(ws_metrics, 'E23:G23', fmt1)
    sleep(2)
    format_cell_range(ws_metrics, 'E27:G27', fmt1)
    format_cell_range(ws_metrics, 'E31:G31', fmt1)
    sleep(2)
    format_cell_range(ws_metrics, 'A25:C25', fmt1)
    format_cell_range(ws_metrics, 'A31:C31', fmt1)
    sleep(2)

    for row in [x for x in range(4, 37) if not x % 2]:
        format_cell_range(ws_metrics, f'A{row}:C{row}', fmt_grey_background)
        sleep(1)

    for row in [x for x in range(4, 37) if not x % 2]:
        format_cell_range(ws_metrics, f'E{row}:G{row}', fmt_grey_background)
        sleep(1)

    ws_metrics.format('A1:B1', {'textFormat': {"fontSize": 18, 'bold': True}})
    ws_metrics.format('A3:G3', {'textFormat': {"fontSize": 11, 'bold': True}})
    ws_metrics.format('E23:G23', {'textFormat': {"fontSize": 11, 'bold': True}})
    sleep(2)
    ws_metrics.format('E27:G27', {'textFormat': {"fontSize": 11, 'bold': True}})
    ws_metrics.format('E31:G31', {'textFormat': {"fontSize": 11, 'bold': True}})
    sleep(2)
    ws_metrics.format('A25:C25', {'textFormat': {"fontSize": 11, 'bold': True}})
    ws_metrics.format('A31:C31', {'textFormat': {"fontSize": 11, 'bold': True}})

    print('"Metrics" sheet has been completed.')

#! *******************************************************************************
#! gs_scores is unfinished but working properly so far!
#! *******************************************************************************
def gs_scores(tick, companies, peer_group, ws_scores):
    """Pulls in data and formats the "Scores" sheet.
       Google allows 1 call/sec

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        ws_metrics (WorkSheet): gspread WorkSheet object
    """
    print('Now creating "Scores" sheet.')
    price = companies[tick].df_basic.loc['price'][0]
    name = companies[tick].df_basic.loc['name'][0]
    sector = companies[tick].df_basic.loc['sector'][0]
    industry = companies[tick].df_basic.loc['industry'][0]
    total_score = companies[tick].score_card['grand_total']
    today = str(datetime.date.today())

    peer_str = ''
    for ticker in companies.keys():
        peer_str += f'{ticker} '
    
    peer_str = peer_str.strip()
    no_of_peers = len(companies.keys())

    a1_a10 = [[name], ['Score'], ['Price'], ['Date'], ['Ticker'], ['Sector'], ['Industry'], 
                   ['Peer Group'], ['# of Peers'], ['Top Scores in Group']]

    b2_b9 = [[total_score], [price], [today], [tick], [sector], 
                   [industry], [peer_str], [no_of_peers]]

    a11_i11 = [['Stock', 'Total', 'V score', 'M score', 'I Score', 'D Score',
                   'P Score', 'A Score', 'E Score']]
     
    v_questions = []
    v_outof = ['/2', '/3', '/3', '/1', '/2', '/2', 
                '/2', '/2', '/1', '/4', '/2', '/2', '/3', '/29']
    v_scores = []

    m_questions = []
    m_outof = ['/3', '/3', '/2', '/2', '/1', '/1', 
                '/3', '/3', '/1', '/1', '/2', '/1', '/1', '/24']
    m_scores = []

    i_questions = []
    i_outof = ['/2', '/3', '/5', '/1', '/11']
    i_scores = []

    d_questions = []
    d_outof = ['/2', '/2', '/2', '/2', '/8']
    d_scores = []

    p_questions = []
    p_outof = ['/1', '/1', '/2', '/2', '/1', '/1', '/8']
    p_scores = []

    a_questions = []
    a_outof = ['/1', '/1', '/2', '/2', '/2', '/2', '/10']
    a_scores = []

    e_questions = []
    e_outof = ['/2', '/2', '/2', '/2', '/2', '/10']
    e_scores = []

    score_lists = [[v_questions, v_outof, v_scores], [m_questions, m_outof, m_scores], 
                   [i_questions, i_outof, i_scores], [d_questions, d_outof, d_scores], 
                   [p_questions, p_outof, p_scores], [a_questions, a_outof, a_scores], 
                   [e_questions, e_outof, e_scores]]

    score_cards = ['value', 'mgmt', 'ins', 'div', 'pub_sent', 'analyst_data', 'esg' ]

    for lists, card in zip(score_lists, score_cards):
        for question, outof, score in zip(companies[tick].score_card[card].index, lists[1], companies[tick].score_card[card].values):
            lists[0].append(question)
            score = ''.join((str(score[0]), outof))
            lists[2].append(score)

        # Shifting last element to first in score lists
        for l in [lists[0], lists[2]]:
            l.insert(0, l.pop())

    # for x in [v_questions, v_scores, m_questions, m_scores]:
    #     print(x)

    ws_scores.batch_update([
        {'range': 'A1:A10',
         'values': a1_a10},
        {'range': 'B2:B9',
        'values': b2_b9},
        {'range': 'A11:I11',
        'values': a11_i11},

        {'range': 'A18:N18',
        'values': [v_questions]},
        {'range': 'A19:N19',
        'values': [v_scores]},

        {'range': 'A21:N21',
        'values': [m_questions]},
        {'range': 'A22:N22',
        'values': [m_scores]},

        {'range': 'A24:E24',
        'values': [i_questions]},
        {'range': 'A25:E25',
        'values': [i_scores]},

        {'range': 'A27:E27',
        'values': [d_questions]},
        {'range': 'A28:E28',
        'values': [d_scores]},

        {'range': 'A30:G30',
        'values': [p_questions]},
        {'range': 'A31:G31',
        'values': [p_scores]},

        {'range': 'A33:G33',
        'values': [a_questions]},
        {'range': 'A34:G34',
        'values': [a_scores]},

        {'range': 'A36:F36',
        'values': [e_questions]},
        {'range': 'A37:F37',
        'values': [e_scores]},

        ])
        




    
#     # Setting up header for the sheet which is just "price" & the value
#     ws_metrics.update('A1', name)
#     ws_metrics.update('B1', price)

#     # Exporting Value header names, stat names, and values
#     ws_metrics.update('A3', 'Value')
#     ws_metrics.update('B3', tick)
#     ws_metrics.update('C3', 'Peer Avg')
#     sleep(5)

#     for i, name in enumerate(companies[tick].df_value.index):
#         value = companies[tick].df_value.loc[name][0]
#         ws_metrics.update(f'A{i + 4}', name)
#         ws_metrics.update(f'B{i + 4}', value)
#         sleep(2)

#     for i, name in enumerate(companies[tick].df_value.index):
#         value = peer_group.df_value.loc[name][0]
#         ws_metrics.update(f'C{i + 4}', value)
#         sleep(1)
#     print('Value stats exported to "Metrics" sheet.')

#     # Exporting Management header names, stat names, and values
#     ws_metrics.update('E3', 'Management')
#     ws_metrics.update('F3', tick)
#     ws_metrics.update('G3', 'Peer Avg')
#     sleep(3)

#     for i, name in enumerate(companies[tick].df_mgmt.index):
#         value = companies[tick].df_mgmt.loc[name][0]
#         ws_metrics.update(f'E{i + 4}', name)
#         ws_metrics.update(f'F{i + 4}', value)
#         sleep(2)

#     for i, name in enumerate(companies[tick].df_mgmt.index):
#         value = peer_group.df_mgmt.loc[name][0]
#         ws_metrics.update(f'G{i + 4}', value)
#         sleep(1)  
#     print('Management stats exported to "Metrics" sheet.')

#     # Exporting Ins & Inst header names, stat names, and values
#     ws_metrics.update('A25', 'Ins & Inst')
#     ws_metrics.update('B25', tick)
#     ws_metrics.update('C25', 'Peer Avg')
#     sleep(3)

#     for i, name in enumerate(companies[tick].df_ins.index):
#         value = companies[tick].df_ins.loc[name][0]
#         ws_metrics.update(f'A{i + 26}', name)
#         ws_metrics.update(f'B{i + 26}', value)
#         sleep(2)

#     for i, name in enumerate(companies[tick].df_ins.index):
#         value = peer_group.df_ins.loc[name][0]
#         ws_metrics.update(f'C{i + 26}', value)
#         sleep(1)
#     print('Ins & Inst stats exported to "Metrics" sheet.')

#     # Exporting Dividend header names, stat names, and values
#     ws_metrics.update('E23', 'Dividend')
#     ws_metrics.update('F23', tick)
#     ws_metrics.update('G23', 'Peer Avg')
#     sleep(3)

#     for i, name in enumerate(companies[tick].div_dfs[0].index):
#         value = companies[tick].div_dfs[0].loc[name][0]
#         ws_metrics.update(f'E{i + 24}', name)
#         ws_metrics.update(f'F{i + 24}', value)
#         sleep(2)

#     if not peer_group.div_dfs[0].empty:
#         for i, name in enumerate(companies[tick].div_dfs[0].index):
#             value = peer_group.div_dfs[0].loc[name]
#             ws_metrics.update(f'G{i + 24}', value[0])
#             sleep(2)
            
#     else:
#         ws_metrics.update('G24', 'n/a')
#         ws_metrics.update('G25', 'n/a')
#         sleep(2)
#     print('Dividend stats exported to "Metrics" sheet.')
    
#     # Exporting Pub Sent header names, stat names, and values
#     ws_metrics.update('A31', 'Pub Sent')
#     ws_metrics.update('B31', tick)
#     ws_metrics.update('C31', 'Peer Avg')
#     sleep(3)

#     for i, name in enumerate(companies[tick].df_pub_sent.index):
#         value = companies[tick].df_pub_sent.loc[name][0]
#         ws_metrics.update(f'A{i + 32}', name)
#         ws_metrics.update(f'B{i + 32}', value)
#         sleep(2)

#     for i, name in enumerate(companies[tick].df_pub_sent.index):
#         value = peer_group.df_pub_sent.loc[name][0]
#         ws_metrics.update(f'C{i + 32}', value)
#         sleep(1)
#     print('Public Sentiment stats exported to "Metrics" sheet.')

#     # Exporting Pub Sent header names, stat names, and values
#     ws_metrics.update('E27', 'Analyst')
#     ws_metrics.update('F27', tick)
#     ws_metrics.update('G27', 'Peer Avg')
#     sleep(3)
#     ws_metrics.update('E28', 'wb_score')
#     ws_metrics.update('F28', companies[tick].analyst_data[2])
#     ws_metrics.update('E29', 'fwd_pe')
#     ws_metrics.update('F29', companies[tick].analyst_data[3])
#     ws_metrics.update('G28', peer_group.analyst_data[2])
#     ws_metrics.update('G29', peer_group.analyst_data[3])
#     sleep(6)
#     print('Analyst stats exported to "Metrics" sheet.')

#     # Exporting ESG header names, stat names, and values
#     ws_metrics.update('E31', 'ESG')
#     ws_metrics.update('F31', tick)
#     ws_metrics.update('G31', 'Peer Avg')
#     sleep(3)

#     for i, name in enumerate(companies[tick].df_esg.index):
#         value = companies[tick].df_esg.loc[name][0]
#         ws_metrics.update(f'E{i + 32}', name)
#         ws_metrics.update(f'F{i + 32}', value)
#         sleep(2)

#     for i, name in enumerate(companies[tick].df_esg.index):
#         value = peer_group.df_esg.loc[name][0]
#         ws_metrics.update(f'G{i + 32}', value)
#         sleep(1)
#     print('ESG stats exported to "Metrics" sheet.')

#     format_cell_range(ws_metrics, 'A1:A36', fmt_bold_italic)
#     format_cell_range(ws_metrics, 'E1:E36', fmt_bold_italic)
#     sleep(2)
#     print('Gussying up the "Metrics" sheet.')

#     format_cell_range(ws_metrics, 'A3:G3', fmt1)
#     set_column_width(ws_metrics, 'D', 20)
#     sleep(2)
#     format_cell_range(ws_metrics, 'D3:D36', fmt_blue_background)
#     format_cell_range(ws_metrics, 'E23:G23', fmt1)
#     sleep(2)
#     format_cell_range(ws_metrics, 'E27:G27', fmt1)
#     format_cell_range(ws_metrics, 'E31:G31', fmt1)
#     sleep(2)
#     format_cell_range(ws_metrics, 'A25:C25', fmt1)
#     format_cell_range(ws_metrics, 'A31:C31', fmt1)
#     sleep(2)

#     for row in [x for x in range(4, 37) if not x % 2]:
#         format_cell_range(ws_metrics, f'A{row}:C{row}', fmt_grey_background)
#         sleep(1)

#     for row in [x for x in range(4, 37) if not x % 2]:
#         format_cell_range(ws_metrics, f'E{row}:G{row}', fmt_grey_background)
#         sleep(1)

#     ws_metrics.format('A1:B1', {'textFormat': {"fontSize": 18, 'bold': True}})
#     ws_metrics.format('A3:G3', {'textFormat': {"fontSize": 11, 'bold': True}})
#     ws_metrics.format('E23:G23', {'textFormat': {"fontSize": 11, 'bold': True}})
#     sleep(2)
#     ws_metrics.format('E27:G27', {'textFormat': {"fontSize": 11, 'bold': True}})
#     ws_metrics.format('E31:G31', {'textFormat': {"fontSize": 11, 'bold': True}})
#     sleep(2)
#     ws_metrics.format('A25:C25', {'textFormat': {"fontSize": 11, 'bold': True}})
#     ws_metrics.format('A31:C31', {'textFormat': {"fontSize": 11, 'bold': True}})

#     print('"Metrics" sheet has been completed.')
# #    ws_metrics.batch_format(metrics_formats)