# company.py
"""Company class and PeerGroup subclass definitions and methods.
    Version 0.4
    Last updated 10/22/22
"""

import pandas as pd
from dataclasses import dataclass, field
from IPython.display import display

@dataclass
class Company:
    """Class Company for creating Company objects."""

# Note that default_factory can take any function name as an argument so we could define a function above and then initialize object with it
    df_basic: pd.DataFrame = field(default_factory=pd.DataFrame) # DataFrame, shape=(6,1), holds basic company details
    df_value: pd.DataFrame = field(default_factory=pd.DataFrame) # DataFrame, shape=(18,1), holds value metrics
    df_mgmt: pd.DataFrame = field(default_factory=pd.DataFrame)# DataFrame, shape=(14,1), holds management metrics
    df_ins: pd.DataFrame = field(default_factory=pd.DataFrame)# DataFrame, shape=(4,1), holds insider & instituion data
    div_dfs: list = field(default_factory=list, repr=False) # List that holds 2 DataFrames containing dividend data
    df_pub_sent: pd.DataFrame = field(default_factory=pd.DataFrame) # DataFrame, shape=(3,1), holds public sentiment data
    news_dfs: list = field(default_factory=list, repr=False) # List that holds 3 DataFrames containing Company, Sector, & Industry news
    analyst_data: list = field(default_factory=list, repr=False) # List that holds 2 DataFrames containing Analyst ratings
    df_esg: pd.DataFrame = field(default_factory=pd.DataFrame) # DataFrame, shape=(27,1), holds ESG data a& metrics

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

@dataclass
class PeerGroup(Company):
    """Subclass PeerGroup for creating PeerGroup objects

    Args:
        Company (Object): Class Company Object
    """
    
    company_list: list = field(default_factory=list) # List of 1 or more Company objects


    def set_df_basic(self):
        """Set self.df_basic values"""

        self.df_basic['name'] = self.company_list[0].df_basic.loc['ticker'] + ' Peer Group Avg'
        self.df_basic['ticker'] = 'n/a'
        self.df_basic['sector'] = self.company_list[0].df_basic.loc['sector']
        self.df_basic['industry'] = self.company_list[0].df_basic.loc['industry']
        self.df_basic['cap'] = 'temp n/a'
        self.df_basic['price'] = 'temp n/a'

    def set_df_value(self):
        """Set self.df_value values"""

        result_list = []

        for metric in self.company_list[0].df_value.index:
            for company in self.company_list:
                result_list.append(company.df_value.loc[metric])
            
            sum = 0
            for value in result_list:
                sum += value

            self.df_value[metric] = sum / len(result_list)