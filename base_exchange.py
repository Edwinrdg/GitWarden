from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Optional, Any


class BaseExchange(ABC):
    """
    抽象基类，定义了所有交易所API应实现的通用接口
    """

    @abstractmethod
    def __init__(
            self,
            api_key: str,
            api_secret: str,
            base_url: str,
            ws_url: str,
            logger: Optional[logging.Logger] = None,
            config: Optional[Dict] = None
    ):
        """
        初始化交易所API
        
        Args:
            api_key: API密钥
            api_secret: API密钥对应的密钥
            base_url: REST API基础URL
            ws_url: WebSocket API URL
            logger: 日志记录器，如果为None则使用默认日志记录器
            config: 配置信息，包含交易对精度等设置
        """
        pass

    @abstractmethod
    async def close(self):
        """关闭API连接，清理资源"""
        pass

    @abstractmethod
    async def get_price(self, symbol: str) -> dict:
        """
        获取指定交易对的当前价格
        
        Args:
            symbol: 交易对，如 "BTC"
            
        Returns:
            价格信息，包含price和timestamp
        """
        pass

    @abstractmethod
    async def get_funding_rate(self, symbol: str) -> dict:
        """
        获取指定交易对的当前资金费率
        
        Args:
            symbol: 交易对，如 "BTC"
            
        Returns:
            资金费率信息，包含funding_rate和timestamp
        """
        pass

    @abstractmethod
    async def place_order(
            self,
            symbol: str,
            side: str,
            order_type: str = "MARKET",
            size: float = None,
            price: float = None,
            tif: str = 'gtc',
            is_close = False
    ) -> Dict:
        """
        下单
        
        Args:
            symbol: 交易对，如 "BTC"
            side: 交易方向，"BUY"或"SELL"
            order_type: 订单类型，"MARKET"或"LIMIT"
            size: 交易数量
            price: 价格，仅限价单需要
            tif: 订单类型
            is_close: 是否为平仓，历史遗留，不要使用
        Returns:
            订单信息
        """
        pass

    @abstractmethod
    async def get_order_status(self,  order_id: str, symbol: str=None) -> Dict:
        """
        获取订单状态
        
        Args:
            order_id: 订单ID
            symbol: 交易对，如 "BTCUSDT"  (有些交易所需要传入symbol，有些不需要)
            
        Returns:
            订单状态信息
            status_res = {
            'success': False,  # 请求状态
            'total_size': '',  # 订单总size
            'price': '',  # 订单价格
            'left_size': '',  # 订单剩余size
            'status': 'unknown',  # 订单状态   open/finished (转换)
            'finish_status': None,  # 订单结束状态(取消: cancelled, 完成：filled)
            'raw_response': response.json()
        }
        """
        pass

    @abstractmethod
    async def get_position(self, symbol: str) -> Optional[Dict]:
        """
        获取指定交易对的当前持仓
        
        Args:
            symbol: 交易对，如 "BTC"
            
        Returns:
            持仓信息，如果无持仓则返回None
        """
        pass

    @abstractmethod
    async def get_positions(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有持仓
        
        Returns:
            所有持仓信息，格式为 {symbol: position_data}
        """
        pass

    @abstractmethod
    async def close_position(self, symbol: str, size: Optional[float] = None, order_type="LIMIT", price="", side: str=None) -> Dict:
        """
        平仓
        
        Args:
            symbol: 交易对，如 "BTC"
            size: 平仓数量，如果为None则全部平仓
            order_type: 订单类型，"MARKET"或"LIMIT"
            price: 价格，仅限价单需要
            side: 持仓方向 （是当前的持仓方向 long 为BUY, short 为 SELL）
            
        Returns:
            平仓结果
        """
        pass

    @abstractmethod
    async def cancel_order(self, symbol: str, order_id: str) -> Dict:
        """
        取消订单
        
        Args:
            symbol: 交易对，如 "BTC"
            order_id: 订单ID
            
        Returns:
            取消结果
        """
        pass

    @abstractmethod
    async def get_depth(self, symbol: str) -> Optional[Dict]:
        """
        获取市场深度数据
        
        Args:
            symbol: 交易对，如 "BTC"
            
        Returns:
            深度数据，包含bids和asks
        """
        pass

    # @abstractmethod
    # async def get_depths_rest(self, symbol: str):
    #     """
    #     通过REST API获取深度数据
    #
    #     Args:
    #         symbol: 交易对，如 "BTC"
    #     """
    #     pass

    @abstractmethod
    async def get_klines(self, symbol, interval='1m', limit=50):
        """获取所有k线数据"""
        pass
    @abstractmethod
    async def update_depths(self):
        """更新所有深度数据"""
        pass

    @abstractmethod
    async def start_ws_price_stream(self):
        """启动WebSocket价格数据流"""
        pass
