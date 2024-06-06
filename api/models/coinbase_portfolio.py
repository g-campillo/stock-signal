from api.enums import PortfolioType

class CoinbasePortfolio:
    name: str
    uuid: str
    type: PortfolioType
    deleted: bool

    def __init__(self, name: str, uuid: str, type: str, deleted: bool) -> None:
        self.name: str = name
        self.uuid: str = uuid
        self.type: PortfolioType = PortfolioType.from_str(type)
        self.deleted: bool = deleted
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> name={self.name} uuid={self.uuid} type={self.type} deleted={self.deleted}>"