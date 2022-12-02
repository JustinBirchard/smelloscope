#stocklist.py
#* Version 1.1
#* Last update 11/22/22
"""
   Used to create stocks list.

   User should create a stocks list or uncomment one of the presets
   below before running the Smelloscope lab.
   
   stocks list will be imported into scope_it_out.py when running the
   Smelloscope lab.

   Save changes after editing this file.
"""
#*******************************************************************
#*   Tips for choosing tickers for your stocks list:
#*           
#*           1) Tickers should be peers. They can be direct competitors, in the same
#*              industry, or at the very least they should be in the same sector.
#*
#*              Technically, you can choose any group you'd like, but the scoring
#*              system will not be accurate if the companies in the stocks list
#*              are not similar in some way.
#*
#*           2) There must be at least two tickers in your stocks list.
#*
#*           3) There is no maximum, however if you are using the free version
#*              of Financial Modeling Prep's API, you are limited to 250 requests 
#*              per day. Each ticker in stocks list will use 2 FMP API requests.
#*            
#*           4) Tickers in stocks list must be at least 5 years old.
#*
#*           5) Currently, the program is not able to process banking and financial 
#*              institution stocks like JPM, LLY, and BAC. This will be corrected 
#*              in the future.

#?------------------------------------------------------------------------------------
#? BEGIN preset stocks lists
#?------------------------------------------------------------------------------------

#* Biomedical
# stocks = ['CRSP', 'GSK', 'BMY', 'AMGN', 'GILD', 'REGN', 'VRTX', 
#           'BIIB', 'ILMN', 'GMAB', 'ALNY', 'SGEN', 'DNLI', 'EXEL', 'BCRX']

#* Car & Auto
# stocks = ['PCAR', 'RACE', 'HMC', 'STLA', 'TTM', 'F', 'GM']

#* Clothing and apparel
# stocks = ['SFIX', 'QRTEA', 'GOOS', 'PLCE', 'BKE', 'VIPS', 'URBN', 'AEO']

#* Computer games
# stocks = ['ATVI', 'EA', 'TTWO']

#* Computer Software & Games
# stocks = ['MSFT', 'EA', 'TTWO', 'ATVI', 'VEEV', 'ORCL', 'CRM', 
#           'ADBE', 'SAP', 'VMW', 'ADSK', 'SNPS', 'CDNS', 'SHOP', 'SQ']

#* Computer hardware & semiconductors
# stocks = ['STM', 'MCHP', 'ON', 'TSEM', 'MPWR', 'INTC', 'AVGO', 'AMAT', 
#           'ADI', 'MU', 'NXPI', 'ENPH', 'MRVL', 'TSM', 'AMD', 'IBM', 'NVDA', 'TXN']

#* Consumer Products - Misc Discretionary
# stocks = ['SPB', 'PBH', 'CL', 'CHD', 'CLX', 'CENT', 'CENTA', 'FNKO', 'ALTO']

#* DRUG MANUFACTURERS
# stocks = ['ZTS', 'HZNP', 'ABT', 'GSK', 'VRTX', 'REGN', 'SNY', 
#           'BMY', 'TAK', 'NBIX', 'UTHR', 'JAZZ', 'CTLT', 'IONS']

#* Entertainment/Media conglomerate
# stocks = ['DIS', 'FUN', 'FWONK', 'FWONA', 'PAR', 'PSO', 'MTN', 
#           'IGT', 'SEAS', 'MSGS', 'RCL', 'CCL', 'CMCSA', 'NFLX']

#* Financial services
# stocks = ['MA', 'WEX', 'EFX', 'WU', 'V', 'ACN', 'SPGI', 'ADP', 
#           'FISV', 'FIS', 'GPN', 'BR', 'FLT', 'PYPL', 'INTU']

#* Health & Hospital Technology
#stocks = ['TDOC', 'VEEV', 'EVH', 'MDRX', 'RCM', 'PINC', 'OMCL', 'NXGN',
#          'AMN', 'ICLR', 'VTRS', 'CRL', 'NVCR', 'HQY', 'ITCI', 'HAE', 'GRFS', 'NTRA']

#* Internet commerce
# stocks = ['ETSY', 'SHOP', 'EBAY', 'AMZN', 'W', 'OSTK', 'BABA', 'ZS']

#* Internet, Data, Information
stocks = ['GOOGL', 'FDS', 'SWCH', 'META', 'SHOP', 'BIDU', 
          'TTD', 'ZS', 'ETSY', 'AKAM', 'ZG', 'LTRPB']

#* Oil and Fuel
# stocks = ['COP', 'XOM', 'CVX', 'MPC', 'HES', 'PSX', 'VLO', 'EQNR', 'BP', 'PBF']

#* REITS - Healthcare related
# stocks = ['VTR', 'OHI', 'MPW', 'HR', 'SUI', 'PEAK', 'DOC']

#* REITS - Storage
# stocks = ['PSA', 'EXR', 'CUBE', 'LSI']

#* Semi-Conductor related
# stocks = ['STM', 'ON', 'NXPI', 'TXN', 'MCHP', 'ST', 'TEL', 'MRVL', 'ENPH']

#* Toys/Games/Hobbies
# stocks = ['ATVI', 'EA', 'TTWO', 'HAS', 'MAT', 'JAKK', 'GME']

#* 50 heaviest weighted stocks from S&P 500 minus Financials
# stocks = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 
#           'UNH', 'XOM', 'JNJ', 'NVDA', 'CVX', 
#           'V', 'PG', 'HD', 'MA', 'PFE',
#           'ABBV', 'PEP', 'KO', 'COST', 'META', 
#           'MCD', 'WMT', 'TMO', 'AVGO', 'CSCO', 
#           'DIS', 'ABT', 'COP', 'BMY', 'ACN', 
#           'DHR', 'VZ', 'NEE', 'LIN', 'TXN', 
#           'AMGN', 'RTX', 'HON', 'PM', 'CRM', 
#           'CMCSA', 'ADBE', 'CVS', 'T', 'IBM', 
#           'UPS', 'NKE', 'CAT', 'QCOM', 'LOW']

# Total Scores from 11/8/22
# GOOGL 60, COP 50, PFE 49, QCOM 49, MSFT 48, CSCO 47, 
# UPS 47, CVX 45, ADBE 45, META 43, CAT 43, XOM 43

#* 2nd tier of 50 heaviest weighted stocks from S&P 500 minus Financials
# stocks = ['NKE', 'INTC', 'ORCL', 'NFLX', 'MDT',
#           'DE', 'SPGI', 'INTU', 'SBUX', 'GILD',
#           'AMD', 'PLD', 'ADP', 'APD', 'AMT', 
#           'BA', 'GE', 'TMUS', 'PYPL', 'ITW',
#           'BSX', 'MDLZ', 'MPC', 'ISRG', 'EOG',
#           'TJX', 'AMAT', 'MO', 'MMC', 'REGN',
#           'VRTX', 'NOC', 'ADI', 'SLB', 'LRCX',
#           'TGT', 'NOW', 'SYK', 'WM', 'GM',
#           'MMM', 'SO', 'ZTS', 'CSX', 'ETN',
#           'BDX', 'MU', 'FISV', 'PXD', 'CL']

# Total Scores from 11/8/22
# MPC 52, EOG 52, AMAT 50, LRCX 48, TJX 48, DE 48, 
# FISV 47, VRTX 45, PXD 44, NKE 43, REGN 43, GM 43

#?------------------------------------------------------------------------------------
#? END preset stocks lists
#?------------------------------------------------------------------------------------


# If Smelloscope lab crashes and says "Stock is not 5 years old", you can add it to 
# the set below to prevent hang-ups in the future.
# Set of stocks that are not yet 5 years old:
young_stocks = {'DDOG', 'CRWD', 'RIVN', 'LCID', 'NIO', 'LI', 'ONEM', 
                'CANO', 'MRVI', 'CERE', 'NARI', 'DNA', 'BEAM', 'VIR', 
                'IMCR', 'PCVX', 'RLAY', 'UBER', 'DOCS', 'PGNY', 'MEDP', 
                'OGN', 'SNOW', 'DASH', 'ASAI', 'REYN', 'RLX', 'VZIO', 
                'HNST', 'ZM', 'SRAD', 'DLO', 'MRNA', 'BNTX', 'GDRX', 
                'PGNY',  'ONEM', 'GDRX', 'SGFY', 'TXG', 'PRVA', 'AGTI', 
                'CERT', 'MPLN', 'SDGR', 'PHR', 'CHWY', 'FIGS', 'CURV', 
                'POSH', 'RVLV', 'AVTR', 'ESAB', 'REZI'}

# List of financial stocks that cannot currently be processed by the Smelloscope:
financial_stocks = {'JPM', 'BAC', 'LLY', 'MRK', 'WFC', 
                    'UNP', 'GS', 'SCWB', 'ELV', 'LMT',
                    'MS', 'BLK', 'BKNG', 'PNC', 'CI',
                    'CB', 'C', 'AXP', 'PGR', 'DUK',
                    'HUM', 'NMYT', 'LADR', 'KREF', 'BRSP',
                    'TRTX', 'STWD', 'TWO', 'CNO', 'PRI', 
                    'AEL', 'NWLI', 'KCLI', 'RDN', 'HMN'}