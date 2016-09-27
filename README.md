# campus-crime : A Repository for Crime-Analysis on College Campuses

Campus Crime Statistics from 2008-2015:

To clone this repo:

```git clone https://github.com/patrickstocklin/campus-crime.git```

To start the Virtualenv and install dependencies:

```cd campus-crime```

```source bin/activate```

```pip install -r requirements.txt```

All preprocessed and postprocessed data can be found in the directory ```~/data```. There you can find the original zipped files containing the data dictionaries (Microsoft Word Docs) and .XLS spreadsheets. There are also directories for processed .XLS files in ~/data/ such as csv-files and sliced-csvs.

All scripts can be found in ```~/src```, such as python scripts to convert Excel Spreadsheets into .csv files, or to ingest the data into Pandas DataFrames.

