havaintopallo
=============

Utilities for downloading & converting FMI data (observation time series only at this point).

Caveat developer
----------------

Please heed FMI's API usage limits and data licenses when using this software.

Usage (with `uv`)
-----------------

See https://docs.astral.sh/uv/ on how to install `uv`.

* Find the FMISID code for the location you're interested in. For example, Turku Artukainen is 100949.
  * See: https://www.ilmatieteenlaitos.fi/havaintoasemat
* Download some data:
  `uv run -m havaintopallo.tools.download_ptso_xml --fmisid=100949 --start-date=2025-01-01 --end-date=2025-03-01 --dest-dir=turku2025`
* Convert the arcane XML into JSONL (or CSV):
  * `uv run -m havaintopallo.tools.convert_ptso_xml turku2025/*.xml > turku2025.jsonl`
  * `uv run -m havaintopallo.tools.convert_ptso_xml -f csv turku2025/*.xml > turku2025.csv`
* Apply data science!

Usage (without `uv`)
--------------------

* Set up a Python 3.9+ virtualenv.
* Install requirements: `pip install -e .`
* Find the FMISID code for the location you're interested in. For example, Turku Artukainen is 100949.
  * See: https://www.ilmatieteenlaitos.fi/havaintoasemat
* Download some data: 
  `python3 -m havaintopallo.tools.download_ptso_xml --fmisid=100949 --start-date=2019-10-01 --end-date=2019-11-01 --dest-dir=turku`
* Convert the arcane XML into JSONL (or CSV):  
  * `python3 -m havaintopallo.tools.convert_ptso_xml turku/*.xml > turku.jsonl`  
  * `python3 -m havaintopallo.tools.convert_ptso_xml -f csv turku/*.xml > turku.csv`
* Apply data science!

Full example
------------

```shell
python3 -m havaintopallo.tools.download_ptso_xml --fmisid=100949 --start-date=2018-01-01 --end-date=2019-01-01 --dest-dir=turku-2018
python3 -m havaintopallo.tools.convert_ptso_xml -f csv turku-2018/*.xml > turku-2018.csv
```

```python
>>> import pandas as pd
>>> turku = pd.read_csv('turku-2018.csv', parse_dates=['timestamp']).drop('file', axis=1).dropna()
>>> turku.groupby('id').describe()
                        value
                        count          mean           std    min     25%      50%      75%      max
id
obs-obs-1-1-n_man     11098.0      5.602271      3.409701    0.0     1.0      8.0      8.0      9.0
obs-obs-1-1-p_sea     11098.0   1015.832114     14.102779  987.1  1006.0   1014.5   1027.0   1049.4
obs-obs-1-1-r_1h       1859.0      0.044970      0.179343    0.0     0.0      0.0      0.0      1.7
obs-obs-1-1-rh        11098.0     84.431519     11.838915   35.0    78.0     88.0     93.0     99.0
obs-obs-1-1-ri_10min  11098.0      0.044332      0.215897    0.0     0.0      0.0      0.0      4.0
obs-obs-1-1-snow_aws  11098.0      8.853938      5.775346    0.0     2.0     12.0     14.0     18.0
obs-obs-1-1-t2m       11098.0     -4.540377      5.383027  -20.0    -8.2     -3.8     -0.1      6.2
obs-obs-1-1-td        11098.0     -6.869553      6.247987  -23.4   -11.5     -6.2     -1.5      5.5
obs-obs-1-1-vis       11098.0  27964.171022  18914.855859  140.0  8942.5  26290.0  50000.0  50000.0
obs-obs-1-1-wawa      11098.0     23.213101     32.311110    0.0     0.0      0.0     61.0     86.0
obs-obs-1-1-wd_10min  11098.0    135.042080     99.813194    0.0    59.0    113.0    183.0    360.0
obs-obs-1-1-wg_10min  11098.0      5.045468      2.943088    0.0     2.9      4.5      6.5     19.0
obs-obs-1-1-ws_10min  11098.0      3.014832      1.638806    0.0     1.8      2.8      3.8     10.7
```
