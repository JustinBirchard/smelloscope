# company.py
"""Company class definitions and methods.
    Version 0.3
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

    def data_to_excel(self):
        """Combine selected data into a new dataframe and output to excel file.
        """
        group = [self.df_basic, self.df_value, self.df_mgmt, 
                self.df_ins, self.div_dfs[0], self.df_pub_sent, self.analyst_data[1]]

        combined_dict = {}

        for dataframe in group:
            for row in dataframe.index:
                combined_dict[row] = dataframe.loc[row][0]

        # Creating df out of dict, transposing, exporting to excel. Filename will output to root folder with filename: [TICKER].xlsx
        pd.DataFrame(combined_dict, index=['Values']).T.to_excel(self.df_basic.loc['ticker'][0] + '.xlsx')


    def display_dfs(self):
        """View selected dataframes in Jupyter Lab or IPython
        """
        group = [self.df_basic, self.df_value, self.df_mgmt, 
                self.df_ins, self.div_dfs[0], self.df_pub_sent, 
                self.analyst_data[0], self.analyst_data[1], self.df_esg]

        for df in group:
            display(df)