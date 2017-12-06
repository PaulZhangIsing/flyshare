# Flyshare


Flyshare is a Pythonic data sharing and algorithmic trading library. 

- [Join our community!](https://groups.google.com/forum/#!forum/flyshare)
- Join our QQ discussion group: 589516242

## Getting Startted
### [Authentication](http://www.asiabigdata.org/registration/)

Get your free API key to start using the data collected from stock markets such as China, Hong Kong, USA, etc.

You can find your API key on your [account settings page](http://www.asiabigdata.org/login/).

#### Authenticating your requests
The Flyshare is free but you must have a API key in order to download data. To get your own API key, you will need to create a free  account and set your API key.

After importing the Flyshare module, you can set your API key with the following command: 
```
flyshare.ApiConfig.api_key = "YOURAPIKEY"
```

### Free Data
Flyshare has a vast collection of free and open data collected from a variety of organizations: 
central banks, governments, multinational organizations and more. 


## Installation

To install flyshare, run:

```bash
pip install flyshare
import flyshare as fs

# get data from the US market
fs.get_hist_data('AAPL')

# get data from the China market
fs.get_hist_data('600519')

# get data from the Hong Kong Market
fs.get_hist_data('0700.HK')

# select data source
fs.set_datasource()

```

## Usage

A good way to get started is to run the [flyshare examples](tutorial) in
a [Jupyter notebook](http://jupyter.org/). To do this, you first want to
start a Jupyter notebook server:

```bash
jupyter notebook
```

From the notebook list page, navigate to the [examples directory](tutorial)
and open a notebook. Execute the code in a notebook cell by clicking on it
and hitting Shift+Enter.


## Questions?

If you find a bug, feel free to [open an issue](https://github.com/duanrb/flyshare/issues) in this repository.


For a list of core developers and outside collaborators, see [the GitHub contributors list](https://github.com/duanrb/flyshare/graphs/contributors)