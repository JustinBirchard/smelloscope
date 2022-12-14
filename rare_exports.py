# rare_exports.py
#* Smelloscope Version 1.3
#* file last updated 11/22/22
"""Exports Smelloscope data to a fancy Google Sheet.
   Use  gs_export within Smelloscope lab to initiate
   all other rare_exports functions.
   
   Google Sheets API Notes:
   One call allowed per second, otherwise get ExhaustedResource error.
   Specific format is required for batch updating rows vs columns
   For columns (eg, A1:A3), the format is [['A1 value'], ['A2 value'], ['A3 value]]
   For rows (eg, A1:C1), the format is [['A1', 'B1', 'C1']]
"""
import datetime
import gspread
from gspread_formatting import *
from time import sleep

#*********************** PUT YOUR SERVICE ACCOUNT FILE NAME HERE:
gc = gspread.service_account(filename='YOUR_SERVICE_ACCOUNT.json')
today = str(datetime.date.today())

# URLs for glossary and scoring documentation
glossary_url = 'tinyurl.com/smelloscope-glossary'
scoring_url = 'tinyurl.com/smelloscope-scoring'

# color dicts for batch_format
blue = {"red": 0.7, "green": 0.9, "blue": 1,}
yellow = {"red": 1, "green": 0.95, "blue": 0.8,}
grey = {"red": 0.94, "green": 0.94, "blue": 0.94,}
dkgrey = {"red": 0.59, "green": 0.59, "blue": 0.59,}

# gspread_formatting objects for text alignment
left_align = CellFormat(horizontalAlignment='LEFT')
right_align = CellFormat(horizontalAlignment='RIGHT')
center_align = CellFormat(horizontalAlignment='CENTER')

def gs_export(tick, companies, peer_group, custom='', emails=[]):
    """Calls all gs functions to export data. 
       Creates, populate, and formats the Google Sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        custom (str) (optional): str used to customize Google Sheet file name
        emails (list) (optional): A list of addresses to email to. 
                                  If empty list, user will be prompted.
    """
    gs_create(tick, custom, emails)
    gs_scores(tick, companies, peer_group, ws_scores)
    gs_metrics(tick, companies, peer_group, ws_metrics)
    gs_analyst(tick, companies, ws_analyst)
    gs_esg(tick, companies, ws_esg)
    gs_news(tick, companies, peer_group, ws_news)
    gs_sec(tick, companies, ws_sec)

def gs_create(tick, custom, emails):
    """Creates Google Spreadsheet, initializes Worksheets,
       and shares via email.

    Args:
        tick (str): ticker of company
        custom (str): submitted by user in Lab when calling gs_export method
        emails (list): A list of addresses to email to. 
                       If empty list, user will be prompted.
    """

    #! Note that variables for WorkSheet objects must be set to global.
    global ws_scores, ws_metrics, ws_analyst, ws_news, ws_esg, ws_sec, spreadsheet_name

    spreadsheet_name = f"{tick} {today}{custom}"

    print('*** This will take about 90 seconds ***\n')

    sh = gc.create(f'{tick} {today}{custom}') # creating spreadsheet object

    if emails != []:
        print(f'Creating Google Sheet called: "{spreadsheet_name}"\n')
        for address in emails:
            sh.share(address, perm_type='user', role='writer')
            print(f'Sharing with {address}\n')

    if emails == []:
        share = input("Do you want to share via email? (y/n): ")

        if share == 'y':
            email = input("Input email and press enter: ")
            print(f'\nCreating Google Sheet called: "{spreadsheet_name}"\n')
            sh.share(email, perm_type='user', role='writer')
            print(f'Sharing with {email}\n')

    # Adding worksheets
    ws_scores = sh.add_worksheet(title="Scores", rows=37, cols=14)
    ws_metrics = sh.add_worksheet(title="Metrics", rows=36, cols=7)
    ws_analyst = sh.add_worksheet(title="Analyst", rows=17, cols=7)
    ws_esg = sh.add_worksheet(title="ESG", rows=29, cols=2)
    ws_news = sh.add_worksheet(title="News", rows=46, cols=2)
    ws_sec = sh.add_worksheet(title="SEC", rows=200, cols=1)

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
    print('Creating "Scores" sheet...')
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

    # titles & values to be batch imported into columns
    a1_a10 = [[name], ['Score'], ['Price'], ['Date'], ['Ticker'], ['Sector'], ['Industry'], 
                   ['Peer Group'], ['# of Peers'], ['Top Scores in Group']]

    a17 = [[f'{tick} Detailed Scorecard']]

    b2_b9 = [[total_score], [price], [today], [tick], [sector], 
                   [industry], [peer_str], [no_of_peers]]

#* Begin Detailed Score Card section (rows 18 to 37)
#& Each scoring category requires 3 lists:
#&                                     "questions" will hold the question IDs, 
#&                                     "outof" holds the available points for each question, 
#&                                     "scores" will hold the scores for each question
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

        # Shifting the "category total" value from last element to first in score lists
        for l in [lists[0], lists[2]]:
            l.insert(0, l.pop())

    #* End Detailed Score Card section (rows 18 to 37)
    #* Begin Top Scores in Group section (rows 11 to 16)

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
                            'values': [row16]},])
    sleep(1)
    print('Gussying up the "Scores" sheet...')

    # List of dicts holds formatting data
    formats = [{"range": "A1:N1",
                "format": {
                "textFormat": {"bold": True, "fontSize": 36,},
                "backgroundColor": blue,
                "borders": {"top": {"style": "SOLID_THICK"},}
                        },},
                {"range": "A10:N10",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 24,},
                "backgroundColor": blue,
                "borders": {"top": {"style": "SOLID_THICK"},},
                        },},
                {"range": "A17:N17",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 24,},
                "backgroundColor": blue,
                "borders": {"top": {"style": "SOLID_THICK"},},
                        },},
                {"range": "A2:N3",
                "format": {
                "textFormat": {"bold": True, "fontSize": 16,},
                "backgroundColor": yellow,
                        },},
                {"range": "A11:N11",
                "format": {
                "textFormat": {"bold": True,},
                "backgroundColor": yellow,
                        },},
                {"range": "B2",
                "format": {
                "textFormat": {"bold": True, "fontSize": 30,},
                        },},
                {"range": "I2:K2",        
                "format": {
                "textFormat": {"fontSize": 12,},
                        },},]
    
    # Loops below will append formatting data to formats list
    for row in [18, 21, 24, 27, 30, 33, 36]:
        formats.append({"range": f"A{row}:N{row}",
                    "format": {
                    "textFormat": {"bold": True},
                    "backgroundColor": yellow,},})

    for row in [row for row in range(4, 10) if row % 2]:
        formats.append({"range": f"A{row}:N{row}",
                    "format": {
                    "backgroundColor": grey,},})

    for row in [row for row in range(12, 17) if not row % 2]:
        formats.append({"range": f"A{row}:N{row}",
                    "format": {
                    "backgroundColor": grey,},})

    for border_range, position in zip(["A1:A37", "N1:N37", "A37:N37"], ["left", "right", "bottom"]):
        formats.append({"range": border_range,
                    "format": {
                    "borders": {position: {"style": "SOLID_THICK"},}},})   

    # Using loop to append additional dicts to formats list
    for row in [20, 23, 26, 29, 32, 35]:
        formats.append({"range": f"A{row}:N{row}",
                    "format": {
                    "backgroundColor": dkgrey,},},)

        # Setting row height while we're here
        set_row_height(ws_scores, str(row), 10)
        sleep(1)

    # Loop to append border formats for the corners
    for corner, side in zip(['A1', 'A10', 'A17', 'N1', 'N10', 'N17'], 
                          ["left", "left", "left", "right", "right", "right"]):
        formats.append({"range": corner,
                        "format": {"borders": {side: {"style": "SOLID_THICK"},
                                   "top": {"style": "SOLID_THICK"},}},})

    for bottomcorner, side in zip(['A37', 'N37'], ["left", "right"]):
        formats.append({"range": bottomcorner,
                        "format": {"borders": {side: {"style": "SOLID_THICK"},
                                   "bottom": {"style": "SOLID_THICK"},}},})

    # Batch formatting using formats dict
    ws_scores.batch_format(formats)
    sleep(1)

    # Misc formatting that can't be done in batch
    ws_scores.format('A2:A3', {'textFormat': {"fontSize": 14, 'bold': True}})
    ws_scores.format('B4:B7', {'textFormat': {"fontSize": 12, 'bold': True}})
    sleep(2)

    for column in ['A', 'B', 'C', 'D', 'D', 
                   'E', 'F', 'G', 'H', 'I', 
                   'J', 'K', 'L', 'M', 'N']:
        set_column_width(ws_scores, column, 72)
        sleep(1)

    format_cell_range(ws_scores, 'B2:B3', left_align)
    format_cell_range(ws_scores, 'B9', left_align)
    sleep(2)

    # Formatting messes with hyperlink so batch updating scoring_url here:
    ws_scores.batch_update([{'range': 'I2',
                            'values': [['Scoring Formulas:']]},
                            {'range': 'K2',
                            'values': [[scoring_url]]},])

    print('"Scores" sheet complete!\n')

def gs_metrics(tick, companies, peer_group, ws_metrics):
    """Pulls in data and formats the "Metrics" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        ws_metrics (WorkSheet): gspread WorkSheet object
    """
    print('Now creating "Metrics" sheet...')
    price = companies[tick].df_basic.loc['price'][0]

    # Batch updating headers and stock price
    ws_metrics.batch_update([
                            {'range': 'A1:B1',
                            'values': [['Price', price]]},
                            {'range': 'A2',
                            'values': [['Glossary:']]},
                            {'range': 'B2',
                            'values': [[glossary_url]]},
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
    sleep(1)

#* Loops below populate lists of stats that will be batch imported into the sheet.
#* All loops are similar in structure except for Dividend, Analyst, and ESG 
#* which require special handling.

    # Each category will have 3 lists 
    v_names = [] # name of stat
    v_stats = [] # value of stat
    v_peer = [] # value of peer stat
    for name in companies[tick].df_value.index:
        stat = companies[tick].df_value.loc[name][0]
        peer_stat = peer_group.df_value.loc[name][0]
        v_names.append([name]) # enclosing in list to satisfy API batch requirement
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
    sleep(1)
    print('Beautifying the "Metrics" sheet...')

    # BATCH FORMATTING BEGIN:
    formats = [{"range": "A2",
                "format": {
                "textFormat": {"fontSize": 12,},
              },},
                {"range": "A4:A36",
                "format": {
                "textFormat": {"bold": True, "italic": True,},
              },},
                {"range": "E1:E36",
                "format": {
                "textFormat": {"bold": True, "italic": True,},
               },},
                {"range": "A3:G3",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": blue,
               },},
                {"range": "E23:G23",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": blue,
                },},
                {"range": "E27:G27",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": blue,
                },},
                {"range": "E31:G31",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": blue,
                },},
                {"range": "A25:C25",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": blue,
                },},
                {"range": "A31:C31",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": blue,
                },},
                {"range": "D3:D36",        
                "format": {"backgroundColor": blue,},},
                {"range": "A1:B1",        
                "format": {"textFormat": {"bold": True, "fontSize": 18,},},},]

    # Using loops to append dicts to formats list
    for row in [x for x in range(4, 37) if not x % 2]:
        formats.append({"range": f"A{row}:C{row}",        
                        "format": {"backgroundColor": grey,},})

    for row in [x for x in range(4, 37) if not x % 2]:
        formats.append({"range": f"E{row}:G{row}",        
                        "format": {"backgroundColor": grey,},})      

    ws_metrics.batch_format(formats)
    # BATCH FORMATTING END

    # Setting column widths
    set_column_width(ws_metrics, 'D', 20)
    sleep(1)

    for column in ['A', 'B', 'C', 'E', 'F', 'G']:
        set_column_width(ws_metrics, column, 93)
        sleep(1)

    print('"Metrics" sheet has been completed!\n')
    sleep(1)

def gs_analyst(tick, companies, ws_analyst):
    """Pulls in data and formats the "Analyst" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        ws_analyst (WorkSheet): gspread WorkSheet object
    """
    print('Now creating "Analyst" sheet...')

    a1 = [['Ratings over last 3 months']]
    d1 = [['Ratings over last 30 days']]
    a2_b2 = [['Rating', 'Total']]
    d2_g2 = [['Date', 'Rating', 'Date', 'Rating']]

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
                            {'range': 'A2:B2',
                            'values': a2_b2},
                            {'range': 'D2:G2',
                            'values': d2_g2},
                            {'range': 'A3:A7',
                            'values': call_type},
                            {'range': 'B3:B7',
                            'values': rot_3mo},
                            {'range': 'D3:D17',
                            'values': first_15_dates},
                            {'range': 'E3:E17',
                            'values': first_15_calls},
                            {'range': 'F3:F17',
                            'values': second_15_dates},
                            {'range': 'G3:G17',
                            'values': second_15_calls},
                            ])
    sleep(1)

    print('Fancifying the "Analyst" sheet...')
    
    # BEGIN batch formatting
    formats = [{"range": "A1:G1",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 14,},
                "backgroundColor": blue,},
             },
               {"range": "A2:G2",        
                "format": {
                "textFormat": {"bold": True, "fontSize": 11,},
                "backgroundColor": yellow,},
             },
               {"range": "C1:C17",        
                "format": {"backgroundColor": dkgrey,},},
               {"range": "D3:D17",        
                "format": {"textFormat": {"italic": True},},},
               {"range": "F3:F17",        
                "format": {"textFormat": {"italic": True},},},
              ]

    for row in [row for row in range(3, 18) if not row % 2]:
        formats.append({"range": f"A{row}:B{row}",        
                        "format": {"backgroundColor": grey,},
                       },)

    for row in [row for row in range(3, 18) if not row % 2]:
        formats.append({"range": f"D{row}:G{row}",        
                        "format": {"backgroundColor": grey,},
                       },)

    ws_analyst.batch_format(formats)
    # END Batch formatting

    # Manually formatting cells
    set_column_width(ws_analyst, 'A', 75)
    set_column_width(ws_analyst, 'B', 174)
    sleep(2)
    set_column_width(ws_analyst, 'C', 20)
    set_column_width(ws_analyst, 'D', 77)
    set_column_width(ws_analyst, 'E', 78)
    sleep(3)
    set_column_width(ws_analyst, 'F', 77)
    set_column_width(ws_analyst, 'G', 78)
    sleep(2)
    format_cell_range(ws_analyst, 'A3:A7', right_align)
    format_cell_range(ws_analyst, 'B3:B7', left_align)
    sleep(2)
    print('"Analyst" sheet complete!\n')

def gs_esg(tick, companies, ws_esg):
    """Pulls in data and formats the "ESG" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        ws_esg (WorkSheet): gspread WorkSheet object
    """
    print('Onto the "ESG" sheet....')

    # Special condition for if ESG is not available for a company
    if isinstance(companies[tick].df_full_esg, str):
        ws_esg.update_cell(1, 1, f'Sorry, ESG data is not available for {tick}')
        set_column_width(ws_esg, 'A', 200)
        sleep(2)
        print('Sorry, ESG data was not available. Moving on...\n')

    else:
        # Iterating thru values in df_full_esg and adding them to list for batch update
        esg_name = []
        esg_value = []
        for name in companies[tick].df_full_esg.index:
            esg_name.append([name])
            esg_value.append([companies[tick].df_full_esg.loc[name][0]])

        ws_esg.batch_update([
                            {'range': 'A1',
                            'values': [[f"{tick}: Full ESG Report"]]},
                            {'range': 'A2:B2',
                            'values': [["ESG Category", "Value"]]},
                            {'range': 'A3:A29',
                            'values': esg_name},
                            {'range': 'B3:B29',
                            'values': esg_value},
                            ])
        sleep(1) 
        print('Giving the "ESG" sheet some love...')

        # BEGIN batch formatting
        formats = [{"range": "A1:B1",        
                    "format": {
                    "textFormat": {"bold": True, "fontSize": 17,},
                    "backgroundColor": blue,},
                },
                {"range": "A2:B2",       
                    "format": {
                    "textFormat": {"bold": True, "fontSize": 12,},
                    "backgroundColor": yellow,},
                },]

        # Formatting the cells
        for row in [row for row in range(3, 30) if row % 2]:
            formats.append({"range": f"A{row}:B{row}",        
                            "format": {"backgroundColor": grey,},},)

        ws_esg.batch_format(formats)
        # END batch formatting

        # Manually formatting
        set_column_width(ws_esg, 'A', 155)
        set_column_width(ws_esg, 'B', 155)
        sleep(2)
        format_cell_range(ws_esg, 'A3:A29', right_align)
        format_cell_range(ws_esg, 'B3:B29', center_align)
        sleep(2)
        print('All done with the "ESG" sheet!\n')

def gs_news(tick, companies, peer_group, ws_news):
    """Pulls in data and formats the "News" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        peer_group (PeerGroup): PeerGroup object
        ws_news (WorkSheet): gspread WorkSheet object
    """
    print(""""Now we're onto the "News" sheet...""")

    industry = companies[tick].df_basic.loc['industry'][0]
    sector = companies[tick].df_basic.loc['sector'][0]

    # Lists are populated with Company, Industry, and Sector headlines and links
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
    sleep(1)
    print('Freshening up the "News" sheet...')
    
    # BEGIN Batch format
    # Using loops to populate formats list
    formats = []
    for row in [row for row in range(3, 23) if row % 2]:
        formats.append({"range": f"A{row}:B{row}", 
                        "format": {"backgroundColor": grey,},},)

    for row in [row for row in range(25, 35) if row % 2]:
        formats.append({"range": f"A{row}:B{row}", 
                        "format": {"backgroundColor": grey,},},)

    for row in [row for row in range(37, 47) if row % 2]:
        formats.append({"range": f"A{row}:B{row}", 
                        "format": {"backgroundColor": grey,},},)

    for blue_set in ['A1:B1', 'A23:B23', 'A35:B35']:
        formats.append({"range": blue_set,        
                        "format": {
                        "textFormat": {"bold": True, "fontSize": 16,},
                        "backgroundColor": blue,},},)

    for yellow_set in ['A2:B2', 'A24:B24', 'A36:B36']:
        formats.append({"range": yellow_set,        
                        "format": {
                        "textFormat": {"bold": True, "fontSize": 12,},
                        "backgroundColor": yellow,},},)
    
    ws_news.batch_format(formats)
    # END Batch format

    # Manually formatting cells
    set_column_width(ws_news, 'A', 900)
    set_column_width(ws_news, 'B', 150)
    sleep(2)
    print('"News" sheet is complete!\n')

def gs_sec(tick, companies, ws_sec):
    """Pulls in data and formats the "SEC" sheet.

    Args:
        tick (str): company ticker
        companies (dict): dict of company objects
        ws_sec (WorkSheet): gspread WorkSheet object
    """
    print('Just one more! Now creating the "SEC" sheet...')

    # Special case for if SEC data is not available
    if isinstance(companies[tick].sec_analysis[0], str):
        ws_sec.update_cell(1, 1, f'Sorry, SEC data is not available for {tick}')
        set_column_width(ws_sec, 'A', 275)
        sleep(2)
        print(f'"SEC" Sheet complete!\n')
        print(f'Your shiny new spreadsheet "{spreadsheet_name}" has been assembled!')

    else:
        # All SEC info will be displayed in one column
        # So itereating through values sec_analysis and values and titles to one list
        sec_all_one_column = []

        for index in companies[tick].sec_analysis[0].index:
            sec_all_one_column.append([f"Category: {companies[tick].sec_analysis[0].loc[index][0]}"])
            sec_all_one_column.append([f"Good news? {companies[tick].sec_analysis[0].loc[index][1]}"])
            sec_all_one_column.append(["Sentence Analyzed:"])
            sec_all_one_column.append([companies[tick].sec_analysis[0].loc[index][2]])

        number_of_columns = len(sec_all_one_column) # used to dynamically set range for formatting

        ws_sec.batch_update([
                            {'range': 'A1',
                            'values': [[f"{tick}: SEC Analysis with help of machine learning"]]},
                            {'range': f'A3:A{number_of_columns + 2}',
                            'values': sec_all_one_column},
                             ])

        print('Making the "SEC" sheet look nice...')

        # BEGIN Batch formatting
        formats = [{"range": "A1",        
                    "format": {
                    "textFormat": {"bold": True, "fontSize": 24,},
                    "backgroundColor": blue,},},
                   {"range": "A2",        
                    "format": {
                    "backgroundColor": dkgrey,},}]
        
        # Appending formats with more dicts
        for row in range(3, number_of_columns + 2, 4):
            formats.append({"range": f"{row}",        
                            "format": {
                            "textFormat": {"bold": True, "underline": True, "fontSize": 12,},
                            "backgroundColor": yellow,},},)

        for row in range(4, number_of_columns + 2, 4):
            formats.append({"range": f"{row}",        
                            "format": {"backgroundColor": yellow,},},)

        for row in range(5, number_of_columns + 2, 4):
            formats.append({"range": f"{row}",        
                            "format": {"backgroundColor": grey,},},)

        ws_sec.batch_format(formats)
        # END Batch formatting
        sleep(1)

        # Manually formatting cells
        set_column_width(ws_sec, 'A', 1875)
        set_row_height(ws_sec, '2', 11)
        sleep(2)

        print(f'"SEC" Sheet complete!\n')
        print(f'New spreadsheet "{spreadsheet_name}" has been assembled!')