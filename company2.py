# company.py
"""Company class definitions and methods.
    Version 0.2
    Last updated 10/18/22
"""
import pandas as pd
from IPython.display import display

class Company:
    """Class Company for creating Company objects."""

    def __init__(self, df_basic, df_value, df_mgmt, df_ins,
                       div_dfs, df_pub_sent, news_dfs, 
                       analyst_data, df_esg):

        """
           Initializes each attribute of a Comapny.
        """

        self._df_basic = df_basic # DataFrame, shape=(6,1), holds basic company details
        self._df_value = df_value # DataFrame, shape=(18,1), holds value metrics
        self._df_mgmt = df_mgmt # DataFrame, shape=(14,1), holds management metrics
        self._df_ins = df_ins # DataFrame, shape=(4,1), holds insider & instituion data
        self._div_dfs = div_dfs # List that holds 2 DataFrames containing dividend data
        self._df_pub_sent = df_pub_sent # DataFrame, shape=(3,1), holds public sentiment data
        self._news_dfs = news_dfs # List that holds 3 DataFrames containing Company, Sector, & Industry news
        self._analyst_data = analyst_data # List that holds 2 DataFrames containing Analyst ratings
        self._df_esg = df_esg # DataFrame, shape=(27,1), holds ESG data a& metrics








#        self._psatype_g3_d = psatype_g3_d if psatype_g3_d != 'radio' else 'radio'
#        self._custommonthly = custommonthly if custommonthly is not None else None
#        self._reportOrderSigma_d = reportOrderSigma_d if reportOrderSigma_d != [] else []
#        self._reportOrderMonthly_d = reportOrderMonthly_d if reportOrderMonthly_d != [] else []   

#************** profile properties
    @property
    def df_basic(self):
        """return self._df_basic value"""
        return self._df_basic

    @property
    def df_value(self):
        """return self._df_value value"""
        return self._df_value

    @property
    def df_mgmt(self):
        """return self._df_mgmt value"""
        return self._df_mgmt

    @property
    def df_ins(self):
        """return self._df_ins value"""
        return self._df_ins

    @property
    def div_dfs(self):
        """return self._div_dfs value"""
        return self._div_dfs

    @property
    def df_pub_sent(self):
        """return self._df_pub_sent value"""
        return self._df_pub_sent

    @property
    def news_dfs(self):
        """return self._news_dfs value"""
        return self._news_dfs

    @property
    def analyst_data(self):
        """return self._analyst_data value"""
        return self._analyst_data

    @property
    def df_esg(self):
        """return self._df_esg value"""
        return self._df_esg













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

