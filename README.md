# smelloscope
### A Smell-O-Scope for sniffing stocks.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://facingwinter.com/misc2022/smelloscope2small.jpg">
  <source media="(prefers-color-scheme: light)" srcset="https://facingwinter.com/misc2022/smelloscope2small.jpg">
  <img alt="Shows a picture of Fry trying out the Smell-O-Scope." src="https://facingwinter.com/misc2022/smelloscope2small.jpg">
</picture>

The Smelloscope gives curiousity seekers a chance to get a long hard whiff of publicly traded companies.

By examining groups of similar stocks (like those in the same industry), the Smelloscope can help determine which stocks are fragarant and which are putrid.

### A Jupyter Notebook is where the action happens. From there, users can:
- Generate detailed scorecards for all companies in the Peer Group
- Examine 50+ metrics for every company
- View averages for every metric in the Peer Group
- Access company, industry, and sector news articles sourced from major websites
- View analyst ratings from the last 3 months
- View distilled SEC filings that are analyzed via a machine learning
- Export detailed reports to Google Sheets
- Export data to Excel

### How to get started:
1) Clone this repo, and create Python environment by following the "Installation Instructions" below
2) Launch Jupyter Lab and open the file **TheSmelloscope.ipynb**
3) Run the top cell in the notebook and then start exploring.

_______________________________________________________________________________________________________________________________________________________
## Installation Instructions:

After cloning this repo:

1) For Windows: <i>[Install Anaconda](https://docs.anaconda.com/anaconda/install/windows/)<br></i> 
   For Mac/Linux <i>[Install Miniconda x86_64 version](https://docs.conda.io/en/latest/miniconda.html)<br></i>

2) Create an virtual environment & install Python. To do this, you can run this line in your terminal: 
    >conda create -n YOUR_ENVIRONMENT_NAME python=3.9.6 -y

3) Activate the vitrual environment by entering this line in your terminal:
    >conda activate YOUR_ENVIRONMENT_NAME

4) Install the OpenBB SDK from the terminal using this line:
    >pip install openbb

**The following are only required if exporting to Google Sheets:**<br>
5) <i>Grab a free [Google Developer Account](https://developers.google.com/)<br></i>
6) Install gspread module from terminal using this line:
    >pip install openbb
7) Install gspread-formatting module from terminal using this line:
    >pip install gspread-formatting
 
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
