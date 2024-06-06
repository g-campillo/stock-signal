from typing import List, Dict

from api.models import CoinbasePortfolio


class CoinbaseBalances:
    value: float
    currency: str

    def __init__(self, value: str, currency: str) -> None:
        self.value: float = float(value)
        self.currency: str = currency
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.value} currency={self.currency}>"

class CoinbasePosition:
    asset: str
    account_uuid: str
    total_balance_fiat: float
    total_balance_crypto: float
    available_to_trade_fiat: float
    allocation: float
    cost_basis: CoinbaseBalances
    asset_img_url: str
    is_cash: bool
    average_entry_price: float
    asset_uuid: str
    available_to_trade_crypto: float
    unrealized_pnl: float

    def __init__(
            self, 
            asset: str, 
            account_uuid: str, 
            total_balance_fiat: float, 
            total_balance_crypto: float, 
            available_to_trade_fiat: float, 
            allocation: float, 
            cost_basis: Dict, 
            asset_img_url: str, 
            is_cash: bool, 
            average_entry_price: float, 
            asset_uuid: str, 
            available_to_trade_crypto: float, 
            unrealized_pnl: float
    ) -> None:
        self.asset: str = asset
        self.account_uuid: str = account_uuid
        self.total_balance_fiat: float = total_balance_fiat
        self.total_balance_crypto: float = total_balance_crypto
        self.available_to_trade_fiat: float = available_to_trade_fiat
        self.allocation: float = allocation
        self.cost_basis: CoinbaseBalances = CoinbaseBalances(**cost_basis)
        self.asset_img_url: str = asset_img_url
        self.is_cash: bool = is_cash
        self.average_entry_price: float = average_entry_price
        self.asset_uuid: str = asset_uuid
        self.available_to_trade_crypto: float = available_to_trade_crypto
        self.unrealized_pnl: float = unrealized_pnl

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} asset={self.asset} account_uuid={self.account_uuid} total_balance_crypto={self.total_balance_crypto:.8f}>"

class CoinbasePortfolioBalances:
    total_balance: CoinbaseBalances
    total_futures_balance: CoinbaseBalances
    total_cash_equivalent_balance: CoinbaseBalances
    total_crypto_balance: CoinbaseBalances
    futures_unrealized_pnl: CoinbaseBalances
    perp_unrealized_pnl: CoinbaseBalances

    def __init__(self, total_balance: Dict, total_futures_balance: Dict, total_cash_equivalent_balance: Dict, total_crypto_balance: Dict, futures_unrealized_pnl: Dict, perp_unrealized_pnl: Dict) -> None:
        self.total_balance: CoinbaseBalances = CoinbaseBalances(**total_balance)
        self.total_futures_balance: CoinbaseBalances = CoinbaseBalances(**total_futures_balance)
        self.total_cash_equivalent_balance: CoinbaseBalances = CoinbaseBalances(**total_cash_equivalent_balance)
        self.total_crypto_balance: CoinbaseBalances = CoinbaseBalances(**total_crypto_balance)
        self.futures_unrealized_pnl: CoinbaseBalances = CoinbaseBalances(**futures_unrealized_pnl)
        self.perp_unrealized_pnl: CoinbaseBalances = CoinbaseBalances(**perp_unrealized_pnl)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

class CoinbaseBreakdownPortfolio:
    portfolio: CoinbasePortfolio
    portfolio_balances: CoinbasePortfolioBalances
    spot_positions: List[CoinbasePosition]
    perp_positions: List[CoinbasePosition]
    futures_positions: List[CoinbasePosition]

    def __init__(self, portfolio: Dict, portfolio_balances: Dict, spot_positions: List[Dict], perp_positions: List[Dict], futures_positions: List[Dict]) -> None:
        self.portfolio: CoinbasePortfolio = CoinbasePortfolio(**portfolio)
        self.portfolio_balances: CoinbasePortfolioBalances = CoinbasePortfolioBalances(**portfolio_balances)
        self.spot_positions: List[CoinbasePosition] = [CoinbasePosition(**spot_position) for spot_position in spot_positions]
        self.perp_positions: List[CoinbasePosition] = [CoinbasePosition(**perp_position) for perp_position in perp_positions]
        self.futures_positions: List[CoinbasePosition] = [CoinbasePosition(**future_position) for future_position in futures_positions]
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

class CoinbasePortfolioBreakdown:
    breakdown: CoinbaseBreakdownPortfolio

    def __init__(self, breakdown: Dict) -> None:
        self.breakdown: CoinbaseBreakdownPortfolio = CoinbaseBreakdownPortfolio(**breakdown)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"