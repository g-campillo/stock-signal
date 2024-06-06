### Environment variables
Create a file named `.env` with the following variables:

```
# Coinbase API
COINBASE_API_KEY=""
COINBASE_API_SECRET=""
COINBASE_TRANSACTION_ACCOUNT_UUID=""
COINBASE_PORTFOLIO_UUID=""
COINBASE_API_URL="https://api.coinbase.com"
COINBASE_API_BASE_PATH="api/v3"
COINBASE_MIN_DOLLAR_AMOUNT="1.00"

# Logging
LOG_LEVEL="INFO"
```

* The `API_KEY` and `API_SECRET` are created by you
* The `COINBASE_TRANSACTION_ACCOUNT_UUID` and `COINBASE_PORTFOLIO_UUID` can be retrevied by running the following command

```bash 
 python get_info.py
```

<br>
<br>

### Setting up the program
1. Create the virtual environment
```bash 
python -m venv .venv
```
2. Activate the virtual environment
```bash
source .venv/bin/activate
```
3. Upgrade your local pip
```bash
pip install --upgrade pip
```
4. Install all requirements
```bash
pip install -r requirements.txt
```

<br>
<br>

### Running the program

To run the api on port 80, you may have to use `sudo`

```bash
sudo $(which gunicorn) -w 2 -b 0.0.0.0:80 main:app
```

<br>

Otherwise you can ommit the usage of `sudo`

```bash
gunicorn -w 2 -b 0.0.0.0:80 main:app
```