class CoinbaseAvailableBalance:
    value: float
    currency: str

    def __init__(self, value: str, currency: str) -> None:
        self.value: float = float(value)
        self.currency: str = currency

class CoinbaseHold:
    value: float
    currency: str

    def __init__(self, value: str, currency: str) -> None:
        self.value: float = float(value)
        self.currency: str = currency

class CoinbaseAccount:
    uuid: str
    name: str
    currency: str
    available_balance: CoinbaseAvailableBalance
    default: bool
    active: bool
    created_at: str
    updated_at: str
    deleted_at: str
    type: str
    ready: bool
    hold: CoinbaseHold
    retail_portfolio_id: str

    def __init__(
            self, 
            uuid: str, 
            name: str, 
            currency: str, 
            available_balance: dict, 
            default: bool, 
            active: bool, 
            created_at: str, 
            updated_at: str, 
            deleted_at: str, 
            type: str, 
            ready: bool, 
            hold: dict, 
            retail_portfolio_id: str
        ) -> None:

        self.uuid: str = uuid
        self.name: str = name
        self.currency: str = currency
        self.available_balance: CoinbaseAvailableBalance = CoinbaseAvailableBalance(**available_balance)
        self.default: bool = default
        self.active: bool = active
        self.created_at: str = created_at
        self.updated_at: str = updated_at
        self.deleted_at: str = deleted_at
        self.type: str = type
        self.ready: bool = ready
        self.hold: CoinbaseHold = CoinbaseHold(**hold)
        self.retail_portfolio_id: str = retail_portfolio_id
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} uuid={self.uuid} currency={self.currency} balance={self.available_balance.value} active={self.active} ready={self.ready}>"