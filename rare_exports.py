# rare_exports.py
#* Version 0.9.9.5
#* last updated 11/13/22

import datetime
import gspread
from gspread_formatting import *
from time import sleep
gc = gspread.service_account(filename='smelloscope-bf9b919f41a7.json')
today = str(datetime.date.today())

ws_metrics = None
ws_scores = None

# for column headers in Metrics

left_align = CellFormat(horizontalAlignment='LEFT')

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

fmt_yellow_background = CellFormat(
    backgroundColor=Color(255/255, 242/255, 204/255)
    )

fmt_grey_background = CellFormat(
    backgroundColor=Color(240/255, 240/255, 240/255)
    )

fmt_dkgrey_background = CellFormat(
    backgroundColor=Color(150/255, 150/255, 150/255)
    )

def gs_export(tick, companies, peer_group, custom='', e_to_j=False, e_to_m=False):
    """Calls all gs functions and creates the Google Sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        custom OPTIONAL (str): str for Spreadsheet file name default is ''
        e_to_j OPTIONAL (bool): True emails to Jeff7sr@gmail.com
        e_to_m OPTIONAL (bool): True emails to mer.broadway@gmail.com
    """
    gs_create(tick, custom, e_to_j, e_to_m)
    gs_scores(tick, companies, peer_group, ws_scores)
    gs_metrics(tick, companies, peer_group, ws_metrics)

def gs_create(tick, custom, e_to_j, e_to_m):
    """Creates Google Spreadsheet, initializes Worksheets,
       and shares via email.

    Args:
        tick (str): ticker of company
        custom (str): submitted by user in Lab when calling gs_export method
        e_to_j (bool): False unless set to True in Lab when calling gs_export. Emails to Jeff.
        e_to_m (bool): False unless set to True in Lab when calling gs_export. Emails to Mary.
    """
    global ws_scores, ws_metrics # need these vars to be global
    sh = gc.create(f'{tick} {today}{custom}') # creating spreadsheet object
    print(f'Creating Google Spreadsheet called: "{tick} {today}{custom}"')

    # sharing via email
    sh.share('ssrjustin@gmail.com', perm_type='user', role='writer')

    if e_to_j is True:
        sh.share('Jeff7sr@gmail.com', perm_type='user', role='writer')

    if e_to_m is True:
        sh.share('mer.broadway@gmail.com', perm_type='user', role='writer')

    # Adding worksheets
    ws_scores = sh.add_worksheet(title="Scores", rows=37, cols=14)
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
    sleep(5)
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
        if not peer_group.df_esg.loc[name].empty:
            value = peer_group.df_esg.loc[name][0]
            ws_metrics.update(f'G{i + 32}', value)
            sleep(1)
        
        elif peer_group.df_esg.loc[name].empty:
            value = 'n/a'
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
        ws_scores (WorkSheet): gspread WorkSheet object
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

    a17 = [[f'{tick} Detailed Scorecard']]

    b2_b9 = [[total_score], [price], [today], [tick], [sector], 
                   [industry], [peer_str], [no_of_peers]]

#* Begin Detailed Score Card section (rows 18 to 37)

    # Each category requires 3 lists "questions" will hold the question IDs, 
    # "outof" holds the available points for each question, scores will hold 
    # the scores for each question

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

    # Grouping all lists into lists so that they can be iterated through and appended with data
    score_lists = [[v_questions, v_outof, v_scores], [m_questions, m_outof, m_scores], 
                   [i_questions, i_outof, i_scores], [d_questions, d_outof, d_scores], 
                   [p_questions, p_outof, p_scores], [a_questions, a_outof, a_scores], 
                   [e_questions, e_outof, e_scores]]

    # putting score category names into list so we can zip together with groups of lists we careted above
    score_cards = ['value', 'mgmt', 'ins', 'div', 'pub_sent', 'analyst_data', 'esg' ]

    for lists, card in zip(score_lists, score_cards):
        for question, outof, score in zip(companies[tick].score_card[card].index, lists[1], companies[tick].score_card[card].values):
            lists[0].append(question)
            score = ''.join((str(score[0]), outof)) # joining score with "outof" so will be eg: '1/2' or '0/3', etc
            lists[2].append(score) # adding completed string to the category's score list

        # Shifting last element to first in score lists (because that's how it is displayed in spreadsheet)
        for l in [lists[0], lists[2]]:
            l.insert(0, l.pop())

#* End Detailed Score Card section (rows 18 to 37)

#* Begin Top Scores in Group section (rows 11 to 16)
    # Header for winners section
    a11_i11 = [['Stock', 'Total', 'V score', 'M score', 'I Score', 'D Score',
                   'P Score', 'A Score', 'E Score']]

    # lists that will hold the ticker and total scores for each category
    row12 = []
    row13 = []
    row14 = []
    row15 = []
    row16= []

    # Getting index and tick for each winner, assigning to list based on index
    for index, tick in enumerate(peer_group.winners.keys()):

        if index == 0:
            row12.append(tick)
            for score in peer_group.winners[tick].values():
                row12.append(score)

        elif index == 1:
            row13.append(tick)
            for score in peer_group.winners[tick].values():
                row13.append(score)

        elif index == 2:
            row14.append(tick)
            for score in peer_group.winners[tick].values():
                row14.append(score)

        elif index == 3:
            row15.append(tick)
            for score in peer_group.winners[tick].values():
                row15.append(score)

        elif index == 4:
            row16.append(tick)
            for score in peer_group.winners[tick].values():
                row16.append(score)

        # elif index == 5:
        #     row16.append(tick)
        #     for score in peer_group.winners[tick].values():
        #         row16.append(score)

    ws_scores.batch_update([
        {'range': 'A1:A10',
         'values': a1_a10},
        {'range': 'B2:B9',
        'values': b2_b9},
        {'range': 'A11:I11',
        'values': a11_i11},

        {'range': 'A17',
        'values': a17},

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

        {'range': 'A12:I12',
        'values': [row12]},
        {'range': 'A13:I13',
        'values': [row13]},
        {'range': 'A14:I14',
        'values': [row14]},
        {'range': 'A15:I15',
        'values': [row15]},
        {'range': 'A16:I16',
        'values': [row16]},
        ])
        
    format_cell_range(ws_scores, 'A1:N1', fmt_blue_background)
    format_cell_range(ws_scores, 'A10:N10', fmt_blue_background)
    format_cell_range(ws_scores, 'A17:N17', fmt_blue_background)
    format_cell_range(ws_scores, 'B2:B3', left_align)
    format_cell_range(ws_scores, 'B9', left_align)
    format_cell_range(ws_scores, 'A2:N3', fmt_yellow_background)
    format_cell_range(ws_scores, 'A11:N11', fmt_yellow_background)
    sleep(6)

    for row in [18, 21, 24, 27, 30, 33, 36]:
        format_cell_range(ws_scores, f'A{row}:N{row}', fmt_yellow_background)
        sleep(1)

    for row in [row for row in range(4, 10) if row % 2]:
        format_cell_range(ws_scores, f'A{row}:N{row}', fmt_grey_background)
        sleep(1)

    for row in [row for row in range(12, 17) if not row % 2]:
        format_cell_range(ws_scores, f'A{row}:N{row}', fmt_grey_background)
        sleep(1)

    for row in [20, 23, 26, 29, 32, 35]:
        format_cell_range(ws_scores, f'A{row}:N{row}', fmt_dkgrey_background)
        set_row_height(ws_scores, str(row), 10)
        sleep(1)

    ws_scores.format('A1', {'textFormat': {"fontSize": 36, 'bold': True}})
    ws_scores.format('A2:A3', {'textFormat': {"fontSize": 14, 'bold': True}})

    ws_scores.format('B2', {'textFormat': {"fontSize": 24, 'bold': True}})
    ws_scores.format('B3', {'textFormat': {"fontSize": 18, 'bold': True}})
    ws_scores.format('B4:B7', {'textFormat': {"fontSize": 12, 'bold': True}})
    ws_scores.format('A10', {'textFormat': {"fontSize": 24, 'bold': True}})
    ws_scores.format('A17', {'textFormat': {"fontSize": 24, 'bold': True}})
    ws_scores.format('A11:I11', {'textFormat': {'bold': True}})
    sleep(5)

    for row in [18, 21, 24, 27, 30, 33, 36]:
        ws_scores.format(f'A{row}:I{row}', {'textFormat': {'bold': True}})
        sleep(1)

    ws_scores.format('A1', {
                           "borders": {
                              "top": {"style": "SOLID_THICK"},
                              "left": {"style": "SOLID_THICK"},
                              }})
    sleep(2)
    ws_scores.format('B1:M1', {
                              "borders": 
                                  {
                                  "top": {"style": "SOLID_THICK"},
                                  }
                              })
    sleep(2)
    ws_scores.format('N1', {
                           "borders": 
                              {
                              "top": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},
                              }})
    sleep(2)
    ws_scores.format('A10', {
                           "borders": 
                              {
                              "top": {"style": "SOLID_THICK"},
                              "left": {"style": "SOLID_THICK"},
                              }})
    sleep(2)
    ws_scores.format('B10:M10', {
                                "borders": 
                                    {
                                    "top": {"style": "SOLID_THICK"},
                                    }
                                })
    sleep(2)
    ws_scores.format('N10', {
                           "borders": 
                              {
                              "top": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},
                              }})
    sleep(2)
    ws_scores.format('A17', {
                            "borders": 
                                {
                                "top": {"style": "SOLID_THICK"},
                                "left": {"style": "SOLID_THICK"},
                                }})
    sleep(2)
    ws_scores.format('B17:M17', {
                                "borders": 
                                    {
                                    "top": {"style": "SOLID_THICK"},
                                    }
                                })
    sleep(2)
    ws_scores.format('N17', {
                            "borders": 
                                {
                                "top": {"style": "SOLID_THICK"},
                                "right": {"style": "SOLID_THICK"},
                                }})
    sleep(2)
    ws_scores.format('A2:A9', {
                               "borders": 
                                   {
                                   "left": {"style": "SOLID_THICK"},
                                   }
                                })

    sleep(2)
    ws_scores.format('A11:A16', {
                               "borders": 
                                   {
                                   "left": {"style": "SOLID_THICK"},
                                   }
                                })

    sleep(2)
    ws_scores.format('A18:A36', {
                               "borders": 
                                   {
                                   "left": {"style": "SOLID_THICK"},
                                   }
                                })

    sleep(2)
    ws_scores.format('N1', {
                           "borders": 
                              {
                              "top": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},
                              }})
    sleep(2)
    ws_scores.format('N2:N9', {
                               "borders": 
                                   {
                                   "right": {"style": "SOLID_THICK"},
                                   }
                                })
    sleep(2)

    ws_scores.format('N11:N16', {
                               "borders": 
                                   {
                                   "right": {"style": "SOLID_THICK"},
                                   }
                                })
    sleep(2)

    ws_scores.format('N18:N36', {
                               "borders": 
                                   {
                                   "right": {"style": "SOLID_THICK"},
                                   }
                                })
    sleep(2)

    ws_scores.format('A37', {
                           "borders": 
                              {
                              "bottom": {"style": "SOLID_THICK"},
                              "left": {"style": "SOLID_THICK"},
                              }})
    sleep(2)
    ws_scores.format('B37:M37', {
                                "borders": 
                                    {
                                    "bottom": {"style": "SOLID_THICK"},
                                    }
                                })
    sleep(2)
    ws_scores.format('N37', {
                           "borders": 
                              {
                              "bottom": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},
                              }})