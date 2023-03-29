# Gathering data from Kibana

To get account name and count of each for an operation:

1. Go to [Kibana Lens](https://kibana.bts.mobi/app/lens).

2. Type your search term in into the search bar, i.e. `operation_history.op_object.pool.keyword : 1.19.301` gets all operations for pool 1.19.301.
3. Drag a field from the list that says availible fields, in this case `account_history.account.keyword`, into the "Add or Drag and Drop a Field" dock for the horizonal axis.
4. Click on the field you just dropped, and select your desired `Number of Values`, as the default is 5, and those more than that number are grouped into an `Other` category in the final CSV.
5. Click on "Add or Drag and Drop a Field" on the vertical axis, and select "Count".
6. Click the "Download As CSV" button in the top right corner.
7. This downloads a file named "unsaved.csv", which you may rename to something more useful.

# Parsing data

Everything from here on presumes you have a working python3 installation on a linux box (see [here](https://www.python.org/downloads/)), the scripts may or may not work on windows or macOS; cross-platform capabilities have not been tested.

It helps to have a basic python understanding for the following steps.

1. Create a folder in your working directory, and add all of the CSV files to the folder, along with `parse_csv.py`.
2. Open `parse_csv.py` in your favorite text editor, and scroll down to line 28-33.
3. Some info about the usage of the script:
 - `data` is a dictionary with keys of the CSV file names, where each value is a dictionary with keys for the horizontal axis and values of the vertical axis.
 - `data2` is a dictionary with keys that label the data within and values of a list of account ids or a dictionary of account ids paired with occurrence numbers.
4. Modify the script to work with your filenames and data.
5. Run the script.  Open a terminal in the current directory (e.g. the one with `parse_csv.py`) and run `python3 parse_csv.py`
6. This will generate (if successful) a file in that directory named `final_data.json`

If the python program does not run successfully and throws a `Traceback`, follow the following general steps for correction:

 - If you see a `KeyError` or `IndexError`: This means that you did not correctly index a dictionary.  Check for typos in your CSV filenames.
 - If you see a `SyntaxError`, this means that you did not write correct python code.  The `Traceback` often points to the problem area, so check for unclosed brackets, double operators (i.e. `*+`), or other typos.

Now that the data is in JSON format, add `tranche.py` to your working directory, and open it in your text editor.

There are several constants as the top of this script, each are explained as follows:

 - `HONEST`: This stores the number of tokens you intend to distribute
 - `DIFFERENT`: This is a True/False Boolean for if your tranches should be different for each group or not. 
 - `PERCENTS`: The percentage of the total supply to go the a given tranche.  They are in the same order as you declared them in `parse_csv.py`.
 - `PRECISION`: the asset precision of your token.

Run `tranche.py`.

You should now have a file named `amt_data.json` that contains the amounts (in graphene terms) to be send to each user, review this thoroughly.

# Sending tranches

Add the rest of the files to your current folder, and make sure that you read and trust `signing_bitshares.py` and `send_tranche.py`.

Triple-check _**everything**_, then check it again, and then, and only then, run `python3 send_tranche.py`.  It will ask for your WIF and username, and then confimation before each transaction.
