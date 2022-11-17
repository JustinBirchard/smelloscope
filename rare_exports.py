# rare_exports.py
#* Version 0.9.9.8
#* last updated 11/16/22
"""Exports Smelloscope data to fancy spreadsheets.

   Currently compatible with Google Sheets.
   Excel compatibility in future updates.
   
   Google API Notes:
   One API call allowed per second, otherwise get ExhaustedResource error.
   Specific format is required for batch importing rows vs columns
   For columns (eg, A1:A3), the format is [['A1 value'], ['A2 value'], ['A3 value]]
   For rows (eg, A1:C1), the format is [['A1', 'B1', 'C1']]
"""

import datetime
import gspread
from gspread_formatting import *
from time import sleep

gc = gspread.service_account(filename='smelloscope-bf9b919f41a7.json')
today = str(datetime.date.today())

ws_metrics = None
ws_scores = None

# Creating CellFormat objects used in funcs for custom formatting
fmt_bold_blue = CellFormat(backgroundColor=Color(0.7, 0.9, 1),
                  textFormat=TextFormat(bold=True, 
                  foregroundColor=Color(0, 0, 0)))

fmt_bold = CellFormat(textFormat=TextFormat(bold=True))

left_align = CellFormat(horizontalAlignment='LEFT')
right_align = CellFormat(horizontalAlignment='RIGHT')

fmt_bold_italic = CellFormat(textFormat=TextFormat(bold=True, italic=True))
fmt_italic = CellFormat(textFormat=TextFormat(italic=True))

fmt_black_background = CellFormat(backgroundColor=Color(0, 0, 0))

fmt_blue_background = CellFormat(backgroundColor=Color(0.7, 0.9, 1))

fmt_yellow_background = CellFormat(backgroundColor=Color(255/255, 242/255, 204/255))

fmt_grey_background = CellFormat(backgroundColor=Color(240/255, 240/255, 240/255))

fmt_dkgrey_background = CellFormat(backgroundColor=Color(150/255, 150/255, 150/255))

def gs_export(tick, companies, peer_group, custom='', e_to_j=False, e_to_m=False):
    """Calls all gs functions and creates the Google Sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        custom OPTIONAL (str): str used to customize spreadsheet file name
        e_to_j OPTIONAL (bool): True emails to Jeff7sr@gmail.com
        e_to_m OPTIONAL (bool): True emails to mer.broadway@gmail.com
    """
    gs_create(tick, custom, e_to_j, e_to_m)
#    gs_scores(tick, companies, peer_group, ws_scores)
#    gs_metrics(tick, companies, peer_group, ws_metrics)
#    gs_analyst(tick, companies, ws_analyst)
    gs_news(tick, companies, peer_group, ws_news)

def gs_create(tick, custom, e_to_j, e_to_m):
    """Creates Google Spreadsheet, initializes Worksheets,
       and shares via email.
       Note that variables for WorkSheet objects must be set to global.

    Args:
        tick (str): ticker of company
        custom (str): submitted by user in Lab when calling gs_export method
        e_to_j (bool): False unless set to True in Lab when calling gs_export. Emails to Jeff.
        e_to_m (bool): False unless set to True in Lab when calling gs_export. Emails to Mary.
    """

    global ws_scores, ws_metrics, ws_analyst, ws_news # need these vars to be global
    
    print(f'Creating Google Spreadsheet called: "{tick} {today}{custom}"')

    sh = gc.create(f'{tick} {today}{custom}') # creating spreadsheet object

    # sharing via email
    sh.share('ssrjustin@gmail.com', perm_type='user', role='writer')

    if e_to_j is True:
        sh.share('Jeff7sr@gmail.com', perm_type='user', role='writer')

    if e_to_m is True:
        sh.share('mer.broadway@gmail.com', perm_type='user', role='writer')

    # Adding worksheets
    ws_scores = sh.add_worksheet(title="Scores", rows=37, cols=14)
    ws_metrics = sh.add_worksheet(title="Metrics", rows=36, cols=7)
    ws_analyst = sh.add_worksheet(title="Analyst", rows=18, cols=7)
    ws_news = sh.add_worksheet(title="News", rows=46, cols=2)

    # deleting blank sheet that gets created when creating a spreadsheet
    ws2 = sh.get_worksheet(0)
    sh.del_worksheet(ws2)

def gs_scores(tick, companies, peer_group, ws_scores):
    """Pulls in data and formats the "Scores" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        ws_scores (WorkSheet): gspread WorkSheet object
    """
    print('Creating "Scores" sheet.')
    price = companies[tick].df_basic.loc['price'][0]
    name = companies[tick].df_basic.loc['name'][0]
    sector = companies[tick].df_basic.loc['sector'][0]
    industry = companies[tick].df_basic.loc['industry'][0]
    total_score = companies[tick].score_card['grand_total']
    today = str(datetime.date.today())
    
    # One string to hold all peers (and in the darkness bind them)
    peer_str = ''
    for ticker in companies.keys():
        peer_str += f'{ticker} '
    
    peer_str = peer_str.strip()
    no_of_peers = len(companies.keys())

    # Lists that hold titles & values to be batch imported into columns
    a1_a10 = [[name], ['Score'], ['Price'], ['Date'], ['Ticker'], ['Sector'], ['Industry'], 
                   ['Peer Group'], ['# of Peers'], ['Top Scores in Group']]

    a17 = [[f'{tick} Detailed Scorecard']]

    b2_b9 = [[total_score], [price], [today], [tick], [sector], 
                   [industry], [peer_str], [no_of_peers]]

#& Begin Detailed Score Card section (rows 18 to 37)

    # Each category requires 3 lists:
    #           "questions" will hold the question IDs, 
    #           "outof" holds the available points for each question, 
    #           "scores" will hold the scores for each question

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

    # putting score category names into list so we can zip together with groups of lists created above
    score_cards = ['value', 'mgmt', 'ins', 'div', 'pub_sent', 'analyst_data', 'esg' ]

    for lists, card in zip(score_lists, score_cards):
        for question, outof, score in zip(companies[tick].score_card[card].index, lists[1], companies[tick].score_card[card].values):
            lists[0].append(question)
            score = ''.join((str(score[0]), outof)) # joining score with "outof" so will be eg: '1/2' or '0/3', etc
            lists[2].append(score) # adding completed string to the category's score list

        # Shifting last element to first in score lists (because that's how it is displayed in spreadsheet)
        for l in [lists[0], lists[2]]:
            l.insert(0, l.pop())

#& End Detailed Score Card section (rows 18 to 37)
#& Begin Top Scores in Group section (rows 11 to 16)

    # Header for winners section
    a11_i11 = [['Stock', 'Total', 'V score', 'M score', 'I Score', 'D Score',
                   'P Score', 'A Score', 'E Score']]

    # lists will hold the ticker and total scores for each category
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

    # Batch updating using all lists above
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
    
    print('Gussying up the "Scores" sheet.')
    # Formatting section
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
    sleep(2)
    ws_scores.format('B2', {'textFormat': {"fontSize": 24, 'bold': True}})
    ws_scores.format('B3', {'textFormat': {"fontSize": 18, 'bold': True}})
    ws_scores.format('B4:B7', {'textFormat': {"fontSize": 12, 'bold': True}})
    ws_scores.format('A10', {'textFormat': {"fontSize": 24, 'bold': True}})
    ws_scores.format('A17', {'textFormat': {"fontSize": 24, 'bold': True}})
    ws_scores.format('A11:I11', {'textFormat': {'bold': True}})
    sleep(6)

    for row in [18, 21, 24, 27, 30, 33, 36]:
        ws_scores.format(f'A{row}:I{row}', {'textFormat': {'bold': True}})
        sleep(1)

    for column in ['A', 'B', 'C', 'D', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']:
        set_column_width(ws_scores, column, 72)
        sleep(1)

    # Begin borders section (which was HUGE pain in the ass!)
    ws_scores.format('A1', {"borders": 
                              {"top": {"style": "SOLID_THICK"},
                              "left": {"style": "SOLID_THICK"},}
                           })
    sleep(2)
    ws_scores.format('B1:M1', {"borders": 
                                  {"top": {"style": "SOLID_THICK"},}
                              })
    sleep(2)
    ws_scores.format('N1', {"borders": 
                              {"top": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},}
                           })
    sleep(2)
    ws_scores.format('A10', {"borders": 
                              {"top": {"style": "SOLID_THICK"},
                              "left": {"style": "SOLID_THICK"},}
                            })
    sleep(2)
    ws_scores.format('B10:M10', {"borders": 
                                    {"top": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('N10', {"borders": 
                              {"top": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},}
                            })
    sleep(2)
    ws_scores.format('A17', {"borders": 
                                {"top": {"style": "SOLID_THICK"},
                                "left": {"style": "SOLID_THICK"},}
                            })
    sleep(2)
    ws_scores.format('B17:M17', {"borders": 
                                    {"top": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('N17', {"borders": 
                                {"top": {"style": "SOLID_THICK"},
                                "right": {"style": "SOLID_THICK"},}
                            })
    sleep(2)
    ws_scores.format('A2:A9', {"borders": 
                                   {"left": {"style": "SOLID_THICK"},}
                              })
    sleep(2)
    ws_scores.format('A11:A16', {"borders": 
                                   {"left": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('A18:A36', {"borders": 
                                   {"left": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('N1', {"borders": 
                              {"top": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},}
                           })
    sleep(2)
    ws_scores.format('N2:N9', {"borders": 
                                   {"right": {"style": "SOLID_THICK"},}
                              })
    sleep(2)
    ws_scores.format('N11:N16', {"borders": 
                                   {"right": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('N18:N36', {"borders": 
                                   {"right": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('A37', {"borders": 
                              {"bottom": {"style": "SOLID_THICK"},
                              "left": {"style": "SOLID_THICK"},}
                            })
    sleep(2)
    ws_scores.format('B37:M37', {"borders": 
                                    {"bottom": {"style": "SOLID_THICK"},}
                                })
    sleep(2)
    ws_scores.format('N37', {"borders": 
                              {"bottom": {"style": "SOLID_THICK"},
                              "right": {"style": "SOLID_THICK"},}
                            })

    print('"Scores" sheet complete.')

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

    # Batch updating headers and stock price
    ws_metrics.batch_update([
                            {'range': 'A1:B1',
                            'values': [['Price', price]]},
                            {'range': 'A3:C3',
                            'values': [['Value', tick, 'Peer Avg']]},
                            {'range': 'E3:G3',
                            'values': [['MGMT', tick, 'Peer Avg']]},
                            {'range': 'A25:C25',
                            'values': [['Ins & Inst', tick, 'Peer Avg']]},
                            {'range': 'E23:G23',
                            'values': [['Dividend', tick, 'Peer Avg']]},
                            {'range': 'A31:C31',
                            'values': [['Pub Sent', tick, 'Peer Avg']]},
                            {'range': 'E27:G27',
                            'values': [['Analyst', tick, 'Peer Avg']]},
                            {'range': 'E31:G31',
                            'values': [['ESG', tick, 'Peer Avg']]},
                             ])

# Loops below populate lists of stats that will be batch imported into the sheet.
# All loops are similar in structure except for Dividend, Analyst, and ESG 
# which require special handling.

    # Each category will have 3 lists 
    v_names = [] # name of stat
    v_stats = [] # value of stat
    v_peer = [] # value of peer stat
    for name in companies[tick].df_value.index:
        stat = companies[tick].df_value.loc[name][0]
        peer_stat = peer_group.df_value.loc[name][0]
        v_names.append([name]) # enclosing in list due to API batch requirement
        v_stats.append([stat])
        v_peer.append([peer_stat])

    m_names = []
    m_stats = []
    m_peer = []
    for name in companies[tick].df_mgmt.index:
        stat = companies[tick].df_mgmt.loc[name][0]
        peer_stat = peer_group.df_mgmt.loc[name][0]
        m_names.append([name])
        m_stats.append([stat])
        m_peer.append([peer_stat])

    i_names = []
    i_stats = []
    i_peer = []
    for name in companies[tick].df_ins.index:
        stat = companies[tick].df_ins.loc[name][0]
        peer_stat = peer_group.df_ins.loc[name][0]
        i_names.append([name])
        i_stats.append([stat])
        i_peer.append([peer_stat])
    
    # Special handling for Dividend loop
    d_names = []
    d_stats = []
    d_peer = []
    for name in companies[tick].div_dfs[0].index:
        stat = companies[tick].div_dfs[0].loc[name][0]
        d_names.append([name])
        d_stats.append([stat])

        if not peer_group.div_dfs[0].empty:
            peer_stat = peer_group.div_dfs[0].loc[name][0]

        else:
            peer_stat = 'n/a'

        d_peer.append([peer_stat])

    p_names = []
    p_stats = []
    p_peer = []
    for name in companies[tick].df_pub_sent.index:
        stat = companies[tick].df_pub_sent.loc[name][0]
        peer_stat = peer_group.df_pub_sent.loc[name][0]
        p_names.append([name])
        p_stats.append([stat])
        p_peer.append([peer_stat])

    # Special handling for Analyst stats (No loop needed)
    a_names = [['wb_score'], ['fwd_pe']]
    a_stats = [[companies[tick].analyst_data[2]], [companies[tick].analyst_data[3]]]
    a_peer = [[peer_group.analyst_data[2]], [peer_group.analyst_data[3]]]

    # Special handling for ESG loop
    e_names = []
    e_stats = []
    e_peer = []
    for name in companies[tick].df_esg.index:
        stat = companies[tick].df_esg.loc[name][0]
        e_names.append([name])
        e_stats.append([stat])

        if not peer_group.df_esg.empty:
            peer_stat = peer_group.df_esg.loc[name][0]

        else:
            peer_stat = 'n/a'

        e_peer.append([peer_stat])

    # Batch updating all stats and stat names to metrics sheet using lists from above
    ws_metrics.batch_update([
                            {'range': 'A4:A23',
                            'values': v_names},
                            {'range': 'B4:B23',
                            'values': v_stats},
                            {'range': 'C4:C23',
                            'values': v_peer},

                            {'range': 'E4:E21',
                            'values': m_names},
                            {'range': 'F4:F21',
                            'values': m_stats},
                            {'range': 'G4:G21',
                            'values': m_peer},

                            {'range': 'A26:A29',
                            'values': i_names},
                            {'range': 'B26:B29',
                            'values': i_stats},
                            {'range': 'C26:C29',
                            'values': i_peer},

                            {'range': 'E24:E25',
                            'values': d_names},
                            {'range': 'F24:F25',
                            'values': d_stats},
                            {'range': 'G24:G25',
                            'values': d_peer},

                            {'range': 'A32:A34',
                            'values': p_names},
                            {'range': 'B32:B34',
                            'values': p_stats},
                            {'range': 'C32:C34',
                            'values': p_peer},

                            {'range': 'E28:E29',
                            'values': a_names},
                            {'range': 'F28:F29',
                            'values': a_stats},
                            {'range': 'G28:G29',
                            'values': a_peer},

                            {'range': 'E32:E36',
                            'values': e_names},
                            {'range': 'F32:F36',
                            'values': e_stats},
                            {'range': 'G32:G36',
                            'values': e_peer},
                            ])
#& END: preperation for batch import of stats and stat names******************

    print('Beautifying the "Metrics" sheet.')
    
    # Formatting cells
    format_cell_range(ws_metrics, 'A1:A36', fmt_bold_italic)
    format_cell_range(ws_metrics, 'E1:E36', fmt_bold_italic)
    sleep(2)
    format_cell_range(ws_metrics, 'A3:G3', fmt_bold_blue)
    set_column_width(ws_metrics, 'D', 20)
    sleep(2)

    for column in ['A', 'B', 'C', 'E', 'F', 'G']:
        set_column_width(ws_metrics, column, 93)
        sleep(1)

    format_cell_range(ws_metrics, 'D3:D36', fmt_blue_background)
    format_cell_range(ws_metrics, 'E23:G23', fmt_bold_blue)
    sleep(2)
    format_cell_range(ws_metrics, 'E27:G27', fmt_bold_blue)
    format_cell_range(ws_metrics, 'E31:G31', fmt_bold_blue)
    sleep(2)
    format_cell_range(ws_metrics, 'A25:C25', fmt_bold_blue)
    format_cell_range(ws_metrics, 'A31:C31', fmt_bold_blue)
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

def gs_analyst(tick, companies, ws_analyst):
    """Pulls in data and formats the "Scores" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        ws_scores (WorkSheet): gspread WorkSheet object
    """
    print('Creating "Analyst" sheet.')

    a1 = [['Ratings over last 3 months']]
    d1 = [['Ratings over last 30 days']]
    a3_b3 = [['Rating', 'Total']]
    d3_g3 = [['Date', 'Rating', 'Date', 'Rating']]

    # Loop adds "3mo ratings over time" data to lists. Lists will be part of batch update
    call_type = []
    rot_3mo = []
    for call in companies[tick].analyst_data[1].index:
        call_type.append([call])
        rot_3mo.append([int(companies[tick].analyst_data[1].loc[call][0])]) # must convert to python int for Google API compatibility

    # Analyst 30 day rating will be split into two sets of 15
    # Loops will add data to lists and lists will be used as part of batch update
    first_15_dates = []
    first_15_calls = []
    for date in companies[tick].analyst_data[0].index[:15]:
        first_15_dates.append([date])
        first_15_calls.append([companies[tick].analyst_data[0].loc[date][0]])

    second_15_dates = []
    second_15_calls = []
    for date in companies[tick].analyst_data[0].index[15:]:
        second_15_dates.append([date])
        second_15_calls.append([companies[tick].analyst_data[0].loc[date][0]])

    ws_analyst.batch_update([
                            {'range': 'A1',
                            'values': a1},
                            {'range': 'D1',
                            'values': d1},
                            {'range': 'A3:B3',
                            'values': a3_b3},
                            {'range': 'D3:G3',
                            'values': d3_g3},
                            {'range': 'A4:A8',
                            'values': call_type},
                            {'range': 'B4:B8',
                            'values': rot_3mo},
                            {'range': 'D4:D18',
                            'values': first_15_dates},
                            {'range': 'E4:E18',
                            'values': first_15_calls},
                            {'range': 'F4:F18',
                            'values': second_15_dates},
                            {'range': 'G4:G18',
                            'values': second_15_calls},
                            ])

    sleep(1)
    print('Fancifying the "Analyst" sheet.')
    format_cell_range(ws_analyst, 'B4:B8', left_align)
    format_cell_range(ws_analyst, 'A4:A8', right_align)
    format_cell_range(ws_analyst, 'A1:G1', fmt_bold_blue)
    sleep(3)
    ws_analyst.format('A3:G3', {'textFormat': {"fontSize": 11, 'bold': True}})
    format_cell_range(ws_analyst, 'D4:D18', fmt_italic)
    format_cell_range(ws_analyst, 'F4:F18', fmt_italic)
    sleep(3)

    for row in [row for row in range(4, 9) if row % 2]:
        format_cell_range(ws_analyst, f'A{row}:B{row}', fmt_grey_background)
        sleep(1)

    for row in [row for row in range(4, 19) if row % 2]:
        format_cell_range(ws_analyst, f'D{row}:G{row}', fmt_grey_background)
        sleep(1)

    format_cell_range(ws_analyst, 'A3:G3', fmt_yellow_background)
    set_column_width(ws_analyst, 'A', 75)
    set_column_width(ws_analyst, 'B', 174)
    sleep(3)
    set_column_width(ws_analyst, 'C', 20)
    set_column_width(ws_analyst, 'D', 77)
    set_column_width(ws_analyst, 'E', 78)
    sleep(3)
    set_column_width(ws_analyst, 'F', 77)
    set_column_width(ws_analyst, 'G', 78)
    sleep(2)

    format_cell_range(ws_analyst, 'C1:C18', fmt_dkgrey_background)
    ws_analyst.format('A1', {'textFormat': {"fontSize": 14, 'bold': True}})
    ws_analyst.format('D1', {'textFormat': {"fontSize": 14, 'bold': True}})
    sleep(3)
    print('"Analyst" sheet complete.')

def gs_news(tick, companies, peer_group, ws_news):
    """Pulls in data and formats the "News" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        ws_news (WorkSheet): gspread WorkSheet object
    """
    print('Creating "News" sheet.')

    industry = companies[tick].df_basic.loc['industry'][0]
    sector = companies[tick].df_basic.loc['sector'][0]

    c_titles = []
    c_links = []
    for index in companies[tick].news_dfs[0].index:
        c_titles.append([companies[tick].news_dfs[0].loc[index]['title']])
        c_links.append([companies[tick].news_dfs[0].loc[index]['link']])

    i_titles = []
    i_links = []
    for index in peer_group.news_dfs[2].index:
        i_titles.append([peer_group.news_dfs[2].loc[index]['title']])
        i_links.append([peer_group.news_dfs[2].loc[index]['link']])
        
    i_titles = i_titles[:10] # getting rid of all but 10 most recent titles & links
    i_links = i_links[:10]

    s_titles = []
    s_links = []
    for index in peer_group.news_dfs[1].index:
        s_titles.append([peer_group.news_dfs[1].loc[index]['title']])
        s_links.append([peer_group.news_dfs[1].loc[index]['link']])
        
    s_titles = s_titles[:10] # getting rid of all but 10 most recent titles & links
    s_links = s_links[:10]

    ws_news.batch_update([
                          {'range': 'A1',
                           'values': [[f"{tick}: Today's Company News"]]},
                          {'range': 'A2:B2',
                           'values': [["Headline", "Link"]]},
                          {'range': 'A3:A22',
                           'values': c_titles},
                          {'range': 'B3:B22',
                           'values': c_links},

                          {'range': 'A23',
                           'values': [[f"{industry}: Today's News"]]},
                          {'range': 'A24:B24',
                           'values': [["Headline", "Link"]]},
                          {'range': 'A25:A34',
                           'values': i_titles},
                          {'range': 'B25:B34',
                           'values': i_links},

                          {'range': 'A35',
                           'values': [[f"{sector}: Today's News"]]},
                          {'range': 'A36:B36',
                           'values': [["Headline", "Link"]]},
                          {'range': 'A37:A46',
                           'values': s_titles},
                          {'range': 'B37:B46',
                           'values': s_links},
                         ])
                    
    set_column_width(ws_news, 'A', 900)
    set_column_width(ws_news, 'B', 150)
    ws_news.format('A1', {'textFormat': {"fontSize": 16, 'bold': True}})
    ws_news.format('A2:B2', {'textFormat': {"fontSize": 12, 'bold': True}})

    ws_news.format('A23', {'textFormat': {"fontSize": 16, 'bold': True}})
    ws_news.format('A24:B24', {'textFormat': {"fontSize": 12, 'bold': True}})

    ws_news.format('A35', {'textFormat': {"fontSize": 16, 'bold': True}})
    ws_news.format('A36:B36', {'textFormat': {"fontSize": 12, 'bold': True}})
    
    for row in [row for row in range(3, 23) if row % 2]:
        format_cell_range(ws_news, f'A{row}:B{row}', fmt_grey_background)
        sleep(1)

    for row in [row for row in range(25, 35) if row % 2]:
        format_cell_range(ws_news, f'A{row}:B{row}', fmt_grey_background)
        sleep(1)

    for row in [row for row in range(37, 47) if row % 2]:
        format_cell_range(ws_news, f'A{row}:B{row}', fmt_grey_background)
        sleep(1)

    for blue_set in ['A1:B1', 'A23:B23', 'A35:B35']:
        format_cell_range(ws_news, blue_set, fmt_blue_background)
        sleep(1)

    for yellow_set in ['A2:B2', 'A24:B24', 'A36:B36']:
        format_cell_range(ws_news, yellow_set, fmt_yellow_background)
        sleep(1)