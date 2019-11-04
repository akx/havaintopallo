havaintopallo
=============

Utilities for downloading & converting FMI data (observation time series only at this point).

Caveat developer
----------------

Please heed FMI's API usage limits and data licenses when using this software.

Usage
-----

* Set up a Python 3.6+ virtualenv.
* Install requirements: `pip install -r requirements.txt`
* Download some data:  
  `python3 -m havaintopallo.tools.download_ptso_xml --fmisid=100949 --start-date=2019-10-01 --end-date=2019-11-01 --dest-dir=turku`
* Convert the arcane XML into JSONL (or CSV):  
  * `python3 -m havaintopallo.tools.convert_ptso_xml turku/*.xml > turku.jsonl`  
  * `python3 -m havaintopallo.tools.convert_ptso_xml -f csv turku/*.xml > turku.csv`
* Apply data science!
