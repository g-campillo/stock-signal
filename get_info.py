import json
from typing import List

from api.services import CoinbaseService
from api.models import CoinbaseAccount, CoinbasePortfolio

if __name__ == "__main__":
    cb = CoinbaseService()
    accounts: List[CoinbaseAccount] = [CoinbaseAccount(**data) for data in cb.list_accounts().get("accounts")]
    
    print("Accounts")
    for account in accounts:
        print("--------------------------------------------------------")
        print(f"                 Name: {account.name}")
        print(f"               Active: {account.active}")
        print(f"                Ready: {account.ready}")
        print(f"              Balance: ${account.available_balance.value:.2f} {account.currency}")
        print(f"                 Hold: ${account.hold.value:.2f} {account.hold.currency}")
        print(f"           Created at: {account.created_at}")
        print(f"           Updated at: {account.updated_at}")
        print(f"           Deleted at: {account.deleted_at}")
        print(f"                 UUID: {account.uuid}")
        print(f"Reatil Portfolio UUID: {account.retail_portfolio_id}")
    
    print("--------------------------------------------------------")
    print("End Accounts\n\n\n")
    print("Portfolios")

    portfolios: List[CoinbasePortfolio] = [CoinbasePortfolio(**data) for data in cb.list_portfolios().get("portfolios")]
    for portfolio in portfolios:
        print("--------------------------------------------------------")
        print(f"Name: {portfolio.name}")
        print(f"Deleted: {portfolio.deleted}")
        print(f"UUID: {portfolio.uuid}")
        print(f"Type: {portfolio.type.name}")
    print("\nEnd Portfolios")
