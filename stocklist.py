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
                'CERT', 'MPLN', 'SDGR', 'PHR'}

#* 50 heaviest weighted stocks from S&P 500 minus Financials
# stocks = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'UNH', 'XOM', 'JNJ', 'NVDA', 'CVX', 'V', 'PG', 'HD', 'MA', 'PFE', 'ABBV', 'PEP', 'KO', 'COST', 'META', 'MCD', 'WMT', 'TMO', 'AVGO', 'CSCO', 'DIS', 'ABT', 'COP', 'BMY', 'ACN', 'DHR', 'VZ', 'NEE', 'LIN', 'TXN', 'AMGN', 'RTX', 'HON', 'PM', 'CRM', 'CMCSA', 'ADBE', 'CVS', 'T', 'IBM', 'UPS', 'NKE', 'CAT', 'QCOM', 'LOW']
# JPM, BAC, LLY, MRK, WFC
#? UNP, GS, SCWB, ELV

#* Health & Hospital Winners:
# stocks = ['PINC', 'OMCL', 'NXGN']
# PINC 45, OMCL 38, NXGN 37

# stocks = ['PINC', 'OMCL', 'NXGN', 'MDRX', 'VEEV', 'EVH']
# PINC 49, OMCL 40, NXGN 40

#* Health & Hospital Technology
# stocks = ['VEEV', 'TDOC', 'EVH', 'MDRX', 'HQY', 'RCM', 'PINC', 'OMCL', 'NXGN']
# PINC 50, OMCL 49, NXGN 48, MDRX 42, VEEV 37, EVH 37

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
# stocks = ['FLT', 'MA']
# MA 42, FLT 40

# Winners of previous round
# stocks = ['FLT', 'MA', 'ACN', 'FISV']
# FLT 45, MA 44, FISV 41, ACN 40

#* Financial services
# stocks = ['MA', 'WEX', 'EFX', 'WU', 'V', 'ACN', 'SPGI', 'ADP', 'FISV', 'FIS', 'GPN', 'BR', 'FLT', 'PYPL', 'INTU']
# FLT 49, MA 42, ACN 42, FISV 42 on 11/7

# stocks = ['INTC', 'TSM', 'TXN']
# TSM 39, TXN 38, INTC 35

# stocks = ['INTC', 'TSM', 'AMD', 'NVDA', 'TXN']
# TSM 46, AMD 44, TXN 39, INTC 37, NVDA 25

#* Winners for Semiconducter and related
# stocks = ['STM', 'ON', 'TSM']
# STM 58, ON 40, TSM 40

# stocks = ['STM', 'ON']
# STM 57, ON 41

# winners of previous round
# stocks = ['STM', 'ON', 'TSM', 'AMAT', 'MCHP', 'AVGO']
# STM 57, ON 44, TSM 42

#* Computer hardware & semiconductors
# stocks = ['INTC', 'MCHP', 'ON', 'TSEM', 'MPWR', 'STM', 'AVGO', 'AMAT', 'ADI', 'MU', 'NXPI', 'ENPH', 'MRVL', 'TSM', 'AMD', 'IBM', 'NVDA', 'TXN']
# STM 61, ON 55, TSM 50, AMAT 45, MCHP 41, AVGO 41

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
# stocks = ['MSFT', 'SAP']
# MSFT 42, SAP 41

# Winners from previous round
# stocks = ['MSFT', 'SAP', 'SNPS', 'ADBE', 'CRM']
# MSFT 43, SAP 39, ADBE 38, CRM 38, SNPS 37

# Computer Software & Games
# stocks = ['ATVI', 'EA', 'TTWO', 'MSFT', 'VEEV', 'ORCL', 'CRM', 'ADBE', 'SAP', 'VMW', 'ADSK', 'SNPS', 'CDNS', 'SHOP', 'SQ']
# MSFT 46, SAP 42, SNPS 42, ADBE 41, CRM 40 on 11/6

#* Winners 11/6 for Internet, Data, Information, Software
# stocks = ['GOOGL', 'META']
# GOOGL 46, META 38 11/6

# Winners of previous round
# stocks = ['GOOGL', 'META', 'BIDU', 'ZD']
# GOOGL 50, META 50, BIDU 39 on 11/6

#* Internet, Data, Information
# stocks = ['GOOGL', 'FDS', 'SWCH', 'META', 'SHOP', 'BIDU', 'TTD', 'ZS', 'ETSY', 'AKAM', 'ZG']
# GOOGL 63, META 54, BIDU 46, 

#* Internet, Data, Information, Internet Software
# stocks = ['GOOGL', 'LTRPB', 'MSFT', 'AAPL', 'CRM', 'ADBE', 'INTU', 'ORCL', 'SAP', 'VMW', 'ADSK', 'SNPS', 'CDNS', 'FDS', 'SWCH', 'META', 'SHOP', 'BIDU', 'TTD', 'ZS', 'ETSY', 'AKAM', 'ZG']
# GOOGL 65, META 53, BIDU 49, MSFT 46, SNPS 45 on 11/6

#* Consumer Products - Misc Discretionary
# stocks = ['SPB', 'PBH', 'CL', 'CHD', 'CLX', 'CENT', 'CENTA', 'FNKO', 'ALTO']
# SPB 27 on 11/6

#* DRUG MANUFACTURERS
#stocks = ['ZTS', 'HZNP', 'ABT', 'GSK', 'VRTX', 'REGN', 'SNY', 'BMY', 'TAK', 'NBIX', 'UTHR', 'JAZZ', 'CTLT', 'IONS']
# ZTS 29, ABT 48, SNY 47, GSK 45, HZNP 44  on 11/6

#* Medical Services
# stocks = ['TDOC', 'AMN', 'ICLR', 'VTRS', 'CRL', 'NVCR', 'HQY', 'ITCI', 'HAE', 'GRFS', 'NTRA']

#* Toys/Games/Hobbies
# stocks = ['ATVI', 'EA', 'TTWO', 'HAS', 'MAT', 'JAKK']


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
# stocks = ['EQNR', 'PBF', 'CVX']
# EQNR 56, PBF 53, CVX 47

# Winners of previous round
# stocks = ['EQNR', 'PBF', 'VLO', 'COP', 'XOM', 'CVX']
# EQNR 60, PBF 52, CVX 48

#* Oil and Fuel
# stocks = ['COP', 'XOM', 'CVX', 'MPC', 'HES', 'PSX', 'VLO', 'EQNR', 'BP', 'PBF']
# EQNR 66, PBF 54, VLO 50, COP 49, XOM 49, CVX 49


#! stocks not available on Financial Modeling Prep API:
# DDOG, CRWD, RIVN, LCID, NIO, LI, ONEM, CANO, MRVI, CERE, NARI, DNA, BEAM
# VIR, IMCR, PCVX, RLAY, UBER, DOCS, PGNY, MEDP, OGN, SNOW, DASH, ASAI, REYN
# RLX, VZIO, HNST, ZM, SRAD, DLO

