# company.py
"""Company class definitions and methods.
    Version 0.1
    Last updated 10/14/22
"""


class Company:
    """Class Company for creating Company objects."""

    def __init__(self, fullname, ticker, sector, industry, cap, price,
                       tca, tld, ptb, bvps, pe, pfcf, pts,
                       roe, roa, gpr, pm, cr, dte,
                       io, it, inst_o, inst_t,
                       div, div_y, div_h,
                       twits_perc, shrt_int,
                       company_news, sector_news, industry_news, news_sent,
                       ratings_list, rot_dict, wb_score):

        """
           Initializes each attribute of a Comapny.
        """
        # profile
        self._fullname = fullname # string - Full name of company pulled from df_profile
        self._ticker = ticker # string - Ticker symbol of company pulled from df_quote
        self._sector = sector
        self._industry = industry
        self._cap = cap # string - Market Cap of the company pulled from df_quote
        self._price = price # float - Current price of the stock pulled from df_quote 

        # value metrics
        self._tca = tca # numpy.float64 - Total current assets of the company -- pulled from df_balance
        self._tld = tld # numpy.float64 - Total long-term debt of the company -- pulled from df_balance
        self._ptb = ptb 
        self._bvps = bvps
        self._pe = pe
        self._pfcf = pfcf
        self._pts = pts

        # management metrics
        self._roe = roe
        self._roa = roa
        self._gpr = gpr
        self._pm = pm
        self._cr = cr
        self._dte = dte

        # insider metrics
        self._io = io
        self._it = it
        self._inst_o = inst_o
        self._inst_t = inst_t

        # dividend metrics
        self._div = div
        self._div_y = div_y
        self._div_h = div_h

        # sentiment metrics
        self._twits_perc = twits_perc
        self._shrt_int = shrt_int

        # news data
        self._company_news = company_news
        self._sector_news = sector_news
        self._industry_news = industry_news
        self._news_sent = news_sent

        # analyst ratings & opinions
        self._ratings_list = ratings_list
        self._rot_dict = rot_dict
        self._wb_score = wb_score

#        self._psatype_g3_d = psatype_g3_d if psatype_g3_d != 'radio' else 'radio'
#        self._custommonthly = custommonthly if custommonthly is not None else None
#        self._reportOrderSigma_d = reportOrderSigma_d if reportOrderSigma_d != [] else []
#        self._reportOrderMonthly_d = reportOrderMonthly_d if reportOrderMonthly_d != [] else []   

#************** profile properties
    @property
    def fullname(self):
        """return self._fullname value"""
        return self._fullname

    @property
    def ticker(self):
        """return self._ticker value"""
        return self._ticker

    @property
    def cap(self):
        """return self._cap value"""
        return self._cap

    @property
    def sector(self):
        """return self._sector value"""
        return self._sector

    @property
    def industry(self):
        """return self._industry value"""
        return self._industry

    @property
    def price(self):
        """return self._price value"""
        return self._price

#************** value properties
    @property
    def tca(self):
        """return self._tca value"""
        return self._tca

    @property
    def tld(self):
        """return self._tld value"""
        return self._tld

    @property
    def ptb(self):
        """return self._ptb value"""
        return self._ptb

    @property
    def bvps(self):
        """return self._bvps value"""
        return self._bvps

    @property
    def pe(self):
        """return self._pe value"""
        return self._pe

    @property
    def pfcf(self):
        """return self._pfcf value"""
        return self._pfcf

    @property
    def pts(self):
        """return self._pts value"""
        return self._pts

#************** management properties
    @property
    def roe(self):
        """return self._roe value"""
        return self._roe

    @property
    def roa(self):
        """return self._roa value"""
        return self._roa

    @property
    def gpr(self):
        """return self._gpr value"""
        return self._gpr

    @property
    def pm(self):
        """return self._pm value"""
        return self._pm

    @property
    def cr(self):
        """return self._cr value"""
        return self._cr

    @property
    def dte(self):
        """return self._dte value"""
        return self._dte

#************** insider properties
    @property
    def io(self):
        """return self._io value"""
        return self._io

    @property
    def it(self):
        """return self._it value"""
        return self._it

    @property
    def inst_o(self):
        """return self._inst_o value"""
        return self._inst_o

    @property
    def inst_t(self):
        """return self._inst_t value"""
        return self._inst_t

#************** dividend properties
    @property
    def div(self):
        """return self._div value"""
        return self._div

    @property
    def div_y(self):
        """return self._div_y value"""
        return self._div_y

    @property
    def div_h(self):
        """return self._div_h value"""
        return self._div_h

#************** sentiment properties
    @property
    def twits_perc(self):
        """return self._twits_perc"""
        return self._twits_perc

    @property
    def shrt_int(self):
        """return self._shrt_int"""
        return self._shrt_int

#************** news properties
    @property
    def company_news(self):
        """return self._company_news"""
        return self._company_news

    @property
    def sector_news(self):
        """return self._sector_news"""
        return self._sector_news

    @property
    def industry_news(self):
        """return self._industry_news"""
        return self._industry_news

    @property
    def news_sent(self):
        """return self._news_sent"""
        return self._news_sent

#************** analyst opinions & ratings properties
    @property
    def ratings_list(self):
        """return self._ratings_list"""
        return self._ratings_list

    @property
    def rot_dict(self):
        """return self._rot_dict"""
        return self._rot_dict

    @property
    def wb_score(self):
        """return self._wb_score"""
        return self._wb_score

















#* Start of Sigma & Monthly report order getters, setters, and methods

    # @property
    # def reportordersigma(self):
    #     """return self._reportOrderSigma_d value"""
    #     return self._reportOrderSigma_d

    # @reportordersigma.setter
    # def reportordersigma(self, new_order):
    #     """Set self._reportOrderSigma_d value"""
    #     self._reportOrderSigma_d = new_order

    # @property
    # def reportordermonthly(self):
    #     """return self._reportOrderMonthly value"""
    #     return self._reportOrderMonthly

    # @reportordermonthly.setter
    # def reportordermonthly(self, new_order):
    #     """Set self._reportOrderMonthly value"""
    #     self._reportOrderMonthly = new_order

    # def set_sigma_order(self):
    #     """Sets order for online Radio Sigma Reports. 
    #        Special handling for multiple reports is provided within the method.
    #     """
    #     # Determining the current number of reports the client has online
    #     cursor.execute(f"""
    #                     SELECT MAX("reportOrder") FROM client_sigma_index 
    #                     WHERE "clientID" = '{self.clientcompany}' AND "reportType" = 'radio'
    #                     """)
    #     query_result = cursor.fetchall() # returns list with one tuple, tuple contains results
       
    #     if query_result[0][0] == None: # case for new client with first reports
    #         for order in range(len(self.sigmatable)):
    #             self.reportordersigma.append(order + 1)

    #     else: # case for existing client with existing reports
    #         starting_position = query_result[0][0] # accessing contents of tuple to determine starting position
    #         for order in range(len(self.sigmatable)):
    #             self.reportordersigma.append(order + 1 + starting_position)

