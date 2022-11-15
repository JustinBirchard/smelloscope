#stocklist.py
"""User selected stock list. Will be imported into scope_it_out.py

   Use one of the pre-made peer groups below or make your own by
   choosing between two and infinity stocks.

   Save changes before running TheSmelloscope.
"""

young_stocks = {'DDOG', 'CRWD', 'RIVN', 'LCID', 'NIO', 'LI', 'ONEM', 
                'CANO', 'MRVI', 'CERE', 'NARI', 'DNA', 'BEAM', 'VIR', 
                'IMCR', 'PCVX', 'RLAY', 'UBER', 'DOCS', 'PGNY', 'MEDP', 
                'OGN', 'SNOW', 'DASH', 'ASAI', 'REYN', 'RLX', 'VZIO', 
                'HNST', 'ZM', 'SRAD', 'DLO', 'MRNA', 'BNTX', 'GDRX', 
                'PGNY',  'ONEM', 'GDRX', 'SGFY', 'TXG', 'PRVA', 'AGTI', 
                'CERT', 'MPLN', 'SDGR', 'PHR', 'CHWY', 'FIGS', 'CURV', 
                'POSH', 'RVLV', 'AVTR'}

stocks = ['PSA', 'EXR', 'CUBE', 'LSI']

# stocks = ['VTR', 'PLD', 'AMT', 'CCI', 'PSA', 'WELL', 'SBAC', 'DLR', 'VICI', 'ARE', 'EXR',
#           'WPC', 'IRM', 'PEAK', 'HST', 'GLPI', 'BXP', 'REXR', 'LAMR', 'CUBE', 'LSI',
#           'COLD', 'OHI', 'MPW', 'EGP', 'FR', 'STAG', 'KRC', 'RHP', 'VNO', 'HR', 'TRNO',
#           'CUZ', 'APLE', 'NSA', 'DOC', 'HIW', 'IIPR', 'OFC', 'DEI', 'SBRA', 'OUT']

# stocks = ['VTR', 'OHI', 'MPW', 'HR', 'SUI', 'PEAK', 'DOC']

# stocks = ['SFIX', 'QRTEA', 'GOOS', 'PLCE', 'BKE', 'VIPS', 'URBN', 'AEO']

# stocks = ['RBA', 'EXLS', 'TNET']

# stocks = ['RBA', 'CPRT', 'LQDT', 'WU', 'WEX', 'WNS', 'MMS', 'EXLS', 'TNET']

#* Winners!
# stocks = ['QCOM', 'AMAT']
# GOOGL 51, QCOM 45, AMAT 36

#* Winners of the run-off for 100 heaviest
# stocks = ['GOOGL', 'QCOM', 'MSFT', 'MPC', 'TJX', 'AMAT']
# GOOGL 50, QCOM 48, AMAT 45, MSFT 43, TJX 41

#* Winners of top 100 heaviest weighted stocks on S&P
#stocks = ['MPC', 'EOG', 'AMAT', 'LRCX', 'TJX', 'DE', 'FISV', 'VRTX', 'PXD', 'NKE', 'REGN', 'GM',
#          'GOOGL', 'COP', 'PFE', 'QCOM', 'MSFT', 'CSCO', 'UPS', 'CVX', 'ADBE', 'META', 'CAT', 'XOM']
# GOOGL 51, QCOM 48, MSFT 48, MPC 45, TJX 45, AMAT 44

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

# 11/8
# GOOGL 60, COP 50, PFE 49, QCOM 49, MSFT 48, CSCO 47, UPS 47, CVX 45, ADBE 45, META 43, CAT 43, XOM 43



# JPM, BAC, LLY, MRK, WFC
#? UNP, GS, SCWB, ELV


#* 2nd tier 50 heaviest weighted stocks from S&P 500 minus Financials
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

# 11/8
# MPC 52, EOG 52, AMAT 50, LRCX 48, TJX 48, DE 48, FISV 47, VRTX 45, PXD 44, NKE 43, REGN 43, GM 43

# LMT, MS, BLK, BKNG, PNC, CI, CB, C, AXP, PGR, DUK, HUM


#* Health & Hospital Winners:
# stocks = ['PINC', 'OMCL', 'NXGN', 'AMN', 'RCM', 'VEEV']
# PINC 45, OMCL 38, NXGN 37

# stocks = ['PINC', 'OMCL', 'NXGN', 'MDRX', 'VEEV', 'EVH']
# PINC 47, OMCL 38, NXGN 40

#* Health & Hospital Technology
#stocks = ['TDOC', 'VEEV', 'EVH', 'MDRX', 'RCM', 'PINC', 'OMCL', 'NXGN',
#          'AMN', 'ICLR', 'VTRS', 'CRL', 'NVCR', 'HQY', 'ITCI', 'HAE', 'GRFS', 'NTRA']

# PINC 48, OMCL 47, NXGN 46, MDRX 41, VEEV 35, EVH 35

# stocks = ['ETSY', 'SHOP', 'EBAY']
# ETSY 39, EBAY 38, SHOP 29

#* Biomedial Winners:
# stocks = ['EXEL', 'VRTX', 'GSK', 'REGN']
# EXEL 41, VRTX 39, GSK 39, REGN 36

# winners of previous round
# stocks = ['EXEL', 'REGN', 'VRTX', 'GSK', 'BIIB', 'CRSP']
# EXEL 44, VRTX 42, GSK 42, REGN 39

#* Biomedical
# stocks = ['CRSP', 'GSK', 'BMY', 'AMGN', 'GILD', 'REGN', 'VRTX', 'BIIB', 'ILMN', 'GMAB', 'ALNY', 'SGEN', 'DNLI', 'EXEL', 'BCRX']
# EXEL 47, REGN 46, VRTX 45, GSK 44, BIIB 42, CRSPR 31

#* Winners for Financial services
# stocks = ['ACN', 'MA']
# ACN 41, MA 36 

# Winners of previous round
# stocks = ['ACN', 'FLT', 'MA', 'FISV']
# ACN 47, MA 42, FLT 41, FISV 37 11/8

#* Financial services
# stocks = ['MA', 'WEX', 'EFX', 'WU', 'V', 'ACN', 'SPGI', 'ADP', 'FISV', 'FIS', 'GPN', 'BR', 'FLT', 'PYPL', 'INTU']
# ACN 49, FLT 45, MA 41, FISV 38 11/8

# stocks = ['INTC', 'TSM', 'TXN']
# TSM 39, TXN 38, INTC 35

# stocks = ['INTC', 'TSM', 'AMD', 'NVDA', 'TXN']
# TSM 46, AMD 44, TXN 39, INTC 37, NVDA 25

#* Winners for Semiconducter and related
# stocks = ['STM', 'TSM']
# STM 54, TSM 39 11/8

# stocks = ['STM', 'AMAT', 'TSM']
# STM 53, TSM 39, AMAT 35 11/8

# winners of previous round
# stocks = ['STM', 'ON', 'AMAT', 'TSM', 'INTC']
# STM 58, AMAT 44, TSM 41, INTC 40, ON 37 11/8

#* Computer hardware & semiconductors
# stocks = ['INTC', 'MCHP', 'ON', 'TSEM', 'MPWR', 'STM', 'AVGO', 'AMAT', 'ADI', 'MU', 'NXPI', 'ENPH', 'MRVL', 'TSM', 'AMD', 'IBM', 'NVDA', 'TXN']
# STM 59, ON 50, AMAT 50, TSM 48, INTC 41 11/8

# stocks = ['EA', 'TTWO']
# EA 33, TTWO 26

# stocks = ['ATVI', 'TTWO']
# ATVI 32, TTWO 33

# stocks = ['ATVI', 'EA']
# ATVI 32, EA 29

#* Computer games
# stocks = ['ATVI', 'EA', 'TTWO']
# ATVI 34, EA 31, TTWO 29

#* Winners for Computer Software
# stocks = ['MSFT', 'ADBE']
# MSFT 37, SAP 35 11/8

# Winners from previous round
# stocks = ['MSFT', 'SNPS', 'ADBE', 'CRM']
# MSFT 42, ADBE 41, CRM 38, SNPS 37 11/8

# Computer Software & Games
# stocks = ['MSFT', 'EA', 'TTWO', 'ATVI', 'VEEV', 'ORCL', 'CRM', 'ADBE', 'SAP', 'VMW', 'ADSK', 'SNPS', 'CDNS', 'SHOP', 'SQ']
# MSFT 45, SNPS 45, ADBE 43, CRM 41 on 11/8

#* Winners 11/13
# stocks = ['GOOGL', 'META', 'MSFT', 'AAPL']

#* Winners 11/6 for Internet, Data, Information, Software
# stocks = ['GOOGL', 'META']
# GOOGL 50, META 37 11/7

# Winners of previous round
# stocks = ['GOOGL', 'META', 'BIDU', 'AKAM']
# GOOGL 53, META 48, BIDU 41, AKAM 31 on 11/7

#* Internet, Data, Information
# stocks = ['GOOGL', 'FDS', 'SWCH', 'META', 'SHOP', 'BIDU', 'TTD', 'ZS', 'ETSY', 'AKAM', 'ZG']
# GOOGL 67, META 49, BIDU 44, AKAM 43 on 11/7

#* Internet, Data, Information, Internet Software
# stocks = ['GOOGL', 'LTRPB', 'MSFT', 'AAPL', 'CRM', 'ADBE', 'INTU', 'ORCL', 'SAP', 'VMW', 'ADSK', 'SNPS', 'CDNS', 'FDS', 'SWCH', 'META', 'SHOP', 'BIDU', 'TTD', 'ZS', 'ETSY', 'AKAM', 'ZG']
# GOOGL 62, MSFT 51, SNPS 50, META 48, ADBE 46, CRM 44 11/7

#* Consumer Products - Misc Discretionary
# stocks = ['SPB', 'PBH', 'CL', 'CHD', 'CLX', 'CENT', 'CENTA', 'FNKO', 'ALTO']
# SPB 27 on 11/6

#* DRUG MANUFACTURERS
#stocks = ['ZTS', 'HZNP', 'ABT', 'GSK', 'VRTX', 'REGN', 'SNY', 'BMY', 'TAK', 'NBIX', 'UTHR', 'JAZZ', 'CTLT', 'IONS']
# ZTS 29, ABT 48, SNY 47, GSK 45, HZNP 44  on 11/6

#* Medical Services
# stocks = ['TDOC', 'AMN', 'ICLR', 'VTRS', 'CRL', 'NVCR', 'HQY', 'ITCI', 'HAE', 'GRFS', 'NTRA']

#* Toys/Games/Hobbies
# stocks = ['ATVI', 'EA', 'TTWO', 'HAS', 'MAT', 'JAKK'] MNSO?


#* Winners of Entertainment/Media conglomerate
# stocks = ['DIS', 'IGT', 'PAR', 'FWONA', 'SEAS', 'MTN']
# IGT 46, DIS 38, SEAS 37

#* Entertainment/Media conglomerate
# stocks = ['DIS', 'FUN', 'FWONK', 'FWONA', 'PAR', 'PSO', 'MTN', 'IGT', 'SEAS', 'MSGS']
# IGT 46, PAR 41, FWONA 38, SEAS 37, MTN 37, DIS 36

#* Computer software/information
# stocks = ['GOOGL', 'LTRPB', 'MSFT', 'AAPL', 'CRM', 'ADBE', 'INTU', 'ORCL', 'SAP', 'VMW', 'ADSK', 'SNPS', 'CDNS', 'SHOP']
# GOOGL 67, MSFT 48 on 11/6

#* Car & Auto
# stocks = ['PCAR', 'RACE', 'HMC', 'STLA', 'TTM', 'F', 'GM']


#* Small group for testing
# stocks = ['INTC', 'AMD']

#* Huge group for testing
#stocks = ['MA', 'V', 'ACN', 'SPGI', 'ADP', 'FISV', 'FIS', 'GPN', 'BR', 'FLT', 'PYPL', 
#          'MSFT', 'AAPL', 'GOOGL', 'ORCL', 'NOW', 'VMW', 'QLYS', 'CVLT', 'PRGS',
#          'INTC', 'AMD', 'IBM', 'NVDA', 'MCHP', 'TXN', 'ADI']


#* Winners Oil & Fuel
# stocks = ['EQNR', 'PBF']
# EQNR 52, PBF 49

# Winners of previous round
# stocks = ['EQNR', 'VLO', 'PBF']
# EQNR 49, PBF 49, VLO 41


#* Oil and Fuel
# stocks = ['COP', 'XOM', 'CVX', 'MPC', 'HES', 'PSX', 'VLO', 'EQNR', 'BP', 'PBF']
# EQNR 65, VLO 54, PBF 52


#! stocks not available on Financial Modeling Prep API:
# DDOG, CRWD, RIVN, LCID, NIO, LI, ONEM, CANO, MRVI, CERE, NARI, DNA, BEAM
# VIR, IMCR, PCVX, RLAY, UBER, DOCS, PGNY, MEDP, OGN, SNOW, DASH, ASAI, REYN
# RLX, VZIO, HNST, ZM, SRAD, DLO

