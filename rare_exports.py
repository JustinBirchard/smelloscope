# rare_exports.py
#* Version 0.9.9.1
#* last updated 11/9/22

import datetime
import gspread
from time import sleep
gc = gspread.service_account(filename='smelloscope-bf9b919f41a7.json')
today = str(datetime.date.today())


def gs_report(tick, companies, peer_group):

    sh = gc.create(f'{tick} {today}')

    sh.share('ssrjustin@gmail.com', perm_type='user', role='writer')

    ws = sh.add_worksheet(title="Metrics", rows=100, cols=10)
    ws2 = sh.get_worksheet(0)
    sh.del_worksheet(ws2)

    price = companies[tick].df_basic.loc['price'][0]

    ws.update('A1', 'Price')
    ws.update('B1', price)

    ws.update('A3', 'Value Metrics')
    ws.update('B3', tick)
    ws.update('C3', 'Peer Avg')

    ws.update('E3', 'MGMT Metrics')
    ws.update('F3', tick)
    ws.update('G3', 'Peer Avg')

    ws.update('A25', 'Ins & Inst')
    ws.update('B25', tick)
    ws.update('C25', 'Peer Avg')

    ws.update('E23', 'Dividend')
    ws.update('F23', tick)
    ws.update('G23', 'Peer Avg')

    ws.update('A31', 'Pub Sent')
    ws.update('B31', tick)
    ws.update('C31', 'Peer Avg')

    ws.update('E27', 'Analyst')
    ws.update('F27', tick)
    ws.update('G27', 'Peer Avg')

    ws.update('E31', 'ESG')
    ws.update('F31', tick)
    ws.update('G31', 'Peer Avg')

    sleep(20)


    for i, name in enumerate(companies[tick].df_value.index):
        value = companies[tick].df_value.loc[name][0]
        ws.update(f'A{i + 4}', name)
        ws.update(f'B{i + 4}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_value.index):
        value = peer_group.df_value.loc[name][0]
        ws.update(f'C{i + 4}', value)
        sleep(1)
        
    for i, name in enumerate(companies[tick].df_mgmt.index):
        value = companies[tick].df_mgmt.loc[name][0]
        ws.update(f'E{i + 4}', name)
        ws.update(f'F{i + 4}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_mgmt.index):
        value = peer_group.df_mgmt.loc[name][0]
        ws.update(f'G{i + 4}', value)
        sleep(1)  
        
    for i, name in enumerate(companies[tick].df_ins.index):
        value = companies[tick].df_ins.loc[name][0]
        ws.update(f'A{i + 26}', name)
        ws.update(f'B{i + 26}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_ins.index):
        value = peer_group.df_ins.loc[name][0]
        ws.update(f'C{i + 26}', value)
        sleep(1)
        
    for i, name in enumerate(companies[tick].div_dfs[0].index):
        value = companies[tick].div_dfs[0].loc[name][0]
        ws.update(f'E{i + 24}', name)
        ws.update(f'F{i + 24}', value)
        sleep(2)

    if not peer_group.div_dfs[0].empty:
        for i, name in enumerate(companies[tick].div_dfs[0].index):
            value = peer_group.div_dfs[0].loc[name]
            ws.update(f'G{i + 24}', value[0])
            sleep(2)
            
    else:
        ws.update('G24', 'n/a')
        ws.update('G25', 'n/a')
        sleep(2)

    for i, name in enumerate(companies[tick].df_pub_sent.index):
        value = companies[tick].df_pub_sent.loc[name][0]
        ws.update(f'A{i + 32}', name)
        ws.update(f'B{i + 32}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_pub_sent.index):
        value = peer_group.df_pub_sent.loc[name][0]
        ws.update(f'C{i + 32}', value)
        sleep(1)

    ws.update('E28', 'wb_score')
    ws.update('F28', companies[tick].analyst_data[2])
    ws.update('E29', 'fwd_pe')
    ws.update('F29', companies[tick].analyst_data[3])
    ws.update('G28', peer_group.analyst_data[2])
    ws.update('G29', peer_group.analyst_data[3])
    sleep(6)

    for i, name in enumerate(companies[tick].df_esg.index):
        value = companies[tick].df_esg.loc[name][0]
        ws.update(f'E{i + 32}', name)
        ws.update(f'F{i + 32}', value)
        sleep(2)

    for i, name in enumerate(companies[tick].df_esg.index):
        value = peer_group.df_esg.loc[name][0]
        ws.update(f'G{i + 32}', value)
        sleep(1)