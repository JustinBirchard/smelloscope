# smelloscope
### A Smell-O-Scope for sniffing stocks.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://facingwinter.com/misc2022/smelloscope2small.jpg">
  <source media="(prefers-color-scheme: light)" srcset="https://facingwinter.com/misc2022/smelloscope2small.jpg">
  <img alt="Shows a picture of Fry trying out the Smell-O-Scope." src="https://facingwinter.com/misc2022/smelloscope2small.jpg">
</picture>

The Smelloscope allows scientists and curiousity seekers the ability to get a long hard whiff of publicly traded companies.

By examining groups of similar stocks (like those in the same industry), the Smelloscope can help determine which stocks are fragarant and which are putrid.

### A simple Jupyter Notebook is where all the action happens. From there, users can:
- Generate detailed scorecards for all companies in the Peer Group
- Examine 50+ metrics for every company
- View averages for every metric in the Peer Group
- Access company, industry, and sector news articles sourced from major websites
- View analyst ratings from the last 3 months
- View distilled SEC filings that are analyzed via a machine learning
- Export detailed reports to Google Sheets
- Export data to Excel

### How to use it:
Users should start by opening and editing **stocklist.py**. Within the file there are 20+ lists of pre-set Peer Groups. Simply uncomment one of the presets, or create your own new list of stocks. Save the file. Then launch Jupyter Lab and open the file **TheSmelloscope.ipynb**

Run the top cell in the notebook and that's it! From there you can choose which cells in the notebook you want to run.

_______________________________________________________________________________________________________________________________________________________
## Requirements:

<i>[Python](https://www.python.org/downloads/) 3.8.5 or newer<br></i>
<i>[OpenBB](https://docs.openbb.co/sdk/quickstart/installation) (a free, open source API)<br></i>
<i>[Anaconda](https://www.anaconda.com/products/distribution) (a free, open source resource for Python)<br></i>

**The following are only required if exporting to Google Sheets:**<br>
<i>Free [Google Developer Account](https://developers.google.com/)<br></i>
<i>gspread</i><br>
<i>gspread-formatting</i>
 
 _______________________________________________________________________________________________________________________________________________________
 # Documentation
 
<i>(Work in progress) Last update: 11/22/22</i><br>
 
 ### Glossary of stock terms and variable names used for metrics:<br> 
 https://tinyurl.com/smelloscope-glossary
 
 ### Scoring categories and formulas:<br> 
 https://tinyurl.com/smelloscope-scoring
 
 ### The repository contains six key files:
 - scope_it_out.py
 - company.py
 - sniffer.py
 - rare_exports.py
 - stocklist.py
 - TheSmelloscope.ipynb
 
 ### Brief explanation of each file:
 
**scope_it_out.py** is the engine of the program. It imports the **stocks** list from **stocklist.py** and iterates through each ticker in the list, gathering data, and instantiating Company and Peer Group objects.

**company.py** contains functions, methods, and definitions for Company and Peer Group objects. Each stock in the **stocks** list will become a Company object. The Company object holds all data and information relating to the company. A PeerGroup object is a subclass of Company and contains the average values of every metric. Company and PeerGroup methods are what allow for examination in **TheSmelloscope.ipynb**. These methods also allow for analyzation and scoring.

**sniffer.py** sniffer contains functions that are used to analyze and output scores for each Company. The master function is called **big_phat_whiff**, and it is called near the end of the **scope_it_out.py** script.

**rare_exports.py** contains functions that can be called in **TheSmelloscope.ipynb**. It is used to export data to a fancy-ass Google Sheet.

**stocklist.py** contains pre-set groups of stock lists. User should uncomment one of the presets, or create a new list of stocks and save file before launching **TheSmelloscope.ipynb**.

**TheSmelloscope.ipynb** is where all the action happens. The lab contains methods and functions for examining and exporting data.
 
 
## More coming soon, please contact thesmelloscope@gmail.com with questions/comments.

# Happy Sniffing!
