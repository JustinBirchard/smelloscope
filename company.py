# company.py
"""Company class definitions and methods.
    Version 0.1
    Last updated 10/12/22
"""


class Company:
    """Class Company for creating Company objects."""

    def __init__(self, fullname, ticker, cap, price,
                       tca, tld):

        """
           Initializes each attribute of a Comapny.
        """
        # profile
        self._fullname = fullname # string - Full name of company pulled from df_profile
        self._ticker = ticker # string - Ticker symbol of company pulled from df_quote
        self._cap = cap # string - Market Cap of the company pulled from df_quote
        self._price = price # float - Current price of the stock pulled from df_quote 

        # value metrics
        self._tca = tca # numpy.float64 - Total current assets of the company -- pulled from df_balance
        self._tld = tld # numpy.float64 - Total long-term debt of the company -- pulled from df_balance

#        self._psatype_g3_d = psatype_g3_d if psatype_g3_d != 'radio' else 'radio'
#        self._custommonthly = custommonthly if custommonthly is not None else None
#        self._reportOrderSigma_d = reportOrderSigma_d if reportOrderSigma_d != [] else []
#        self._reportOrderMonthly_d = reportOrderMonthly_d if reportOrderMonthly_d != [] else []   

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
    def price(self):
        """return self._price value"""
        return self._price

    @property
    def tca(self):
        """return self._tca value"""
        return self._tca

    @property
    def tld(self):
        """return self._tld value"""
        return self._tld
  

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

    def set_sigma_order(self):
        """Sets order for online Radio Sigma Reports. 
           Special handling for multiple reports is provided within the method.
        """
        # Determining the current number of reports the client has online
        cursor.execute(f"""
                        SELECT MAX("reportOrder") FROM client_sigma_index 
                        WHERE "clientID" = '{self.clientcompany}' AND "reportType" = 'radio'
                        """)
        query_result = cursor.fetchall() # returns list with one tuple, tuple contains results
       
        if query_result[0][0] == None: # case for new client with first reports
            for order in range(len(self.sigmatable)):
                self.reportordersigma.append(order + 1)

        else: # case for existing client with existing reports
            starting_position = query_result[0][0] # accessing contents of tuple to determine starting position
            for order in range(len(self.sigmatable)):
                self.reportordersigma.append(order + 1 + starting_position)

