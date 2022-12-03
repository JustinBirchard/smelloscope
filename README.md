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

#### MASSIVE Shout out to the brilliant, helpful, friendly folks at OpenBB for making their [amazing SDK available, free, and open source!](https://docs.openbb.co/sdk/quickstart/installation)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://facingwinter.com/misc2022/small_openbb_logo.png">
  <source media="(prefers-color-scheme: light)" srcset="https://facingwinter.com/misc2022/small_openbb_logo.png">
  <img alt="Shows OpenBB logo." src="https://facingwinter.com/misc2022/small_openbb_logo.png">
</picture>

Visit [OpenBB.co](https://openbb.co/) for more info.

_______________________________________________________________________________________________________________________________________________________
## Smelloscope Installation Instructions:

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


### How to use the Smelloscope:
1) From the virtual environment created using instructions above, launch Jupyter Lab and open the file **TheSmelloscope.ipynb**
3) Run the top cell in the notebook and then start exploring!

 _______________________________________________________________________________________________________________________________________________________
 # Documentation
 
<i>(Work in progress) Last update: 12/3/22</i><br>
 
 ### Glossary of stock terms and variable names used for metrics:<br> 
 https://tinyurl.com/smelloscope-glossary
 
 ### Scoring categories and formulas:<br> 
 https://tinyurl.com/smelloscope-scoring
 
 ### The root contains 6 key files and one directory:
 - TheSmelloscope.ipynb
 - scope_it_out.py
 - objective_lens.py
 - company.py
 - sniffer.py
 - rare_exports.py
 - config folder which contains smello.toml and an init file

 ### Brief explanation of each file:

**TheSmelloscope.ipynb** is where all the action happens. The lab contains methods and functions for examining and exporting data.

**scope_it_out.py** is the engine. It imports the user selected stocks from **smello.toml** via the **objective_lens.group_selection** function. The script iterates through each ticker in the list, gathering data, and instantiating **Company** and **PeerGroup** objects.

**objective_lens.py** imports the config module and defines **group_selection**, a function that returns a list of user selected stocks.

**company.py** contains functions, methods, and definitions for **Company** and **PeerGroup** objects. Each stock in the user selected group will become a Company object. The Company object holds all data relating to the company. A PeerGroup object is a subclass of Company and contains the average values of every metric. Company and PeerGroup methods are what allow for examination in **TheSmelloscope.ipynb**. These methods also allow for analyzation and scoring.

**sniffer.py** sniffer contains functions that are used to analyze and output scores for each Company. The master function is called **big_phat_whiff**, and it is called near the end of the **scope_it_out.py** script.

**rare_exports.py** contains functions that can be called in **TheSmelloscope.ipynb**. It is used to export data to a fancy-ass Google Sheet.

**smello.toml** is the configuration file where advanced users can define custom stock groups and industry presets. Within the same folder is the init file which uses module **tomli** to make smello.toml accessible globally.
 
## More coming soon, please contact thesmelloscope@gmail.com with questions/comments.

# Happy Sniffing!
