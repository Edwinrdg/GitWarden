import aiohttp
import websockets
from typing import Optional, Dict, Any
from utils.proxy_manager import ProxyManager

class ExchangeAdapter:
    def __init__(
        self, 
        exchange_name: str,
        api_key: str,
        secret_key: str,
        symbol: str,
        base_config: Dict[str, Any],
        proxy_manager: ProxyManager,
        account_config: Dict[str, Any] = None  # 添加账号配置参数
    ):
        self.exchange_name = exchange_name
        self.api_key = api_key
        self.secret_key = secret_key
        self.symbol = symbol
        self.base_config = base_config
        self.proxy_manager = proxy_manager
        self.account_config = account_config or {}  # 保存账号配置
        
        # 获取交易所配置
        self.exchange_config = base_config['exchanges'][exchange_name]
        self.base_url = self.exchange_config['base_url']
        self.ws_url = self.exchange_config['ws_url']
        
        # 获取随机代理
        self.proxy = self.proxy_manager.get_random_proxy()
        
        # 初始化API客户端
        self._init_client()
        
    def _init_client(self):
        if self.exchange_name == 'edgex':
            from exchanges.edgex_api import EdgexAPI
            self.client = EdgexAPI(
                api_key=self.api_key,
                api_secret=self.secret_key,
                base_url=self.base_url,
                ws_url=self.ws_url,
                config={
                    'exchanges': {
                        'edgex': {
                            'account_id': self.account_config.get('account_id'),
                            'public_key_y_coordinate': self.account_config.get('public_key_y_coordinate')
                        }
                    }
                }
            )
        elif self.exchange_name == 'aster':
            from exchanges.aster_api import AsterAPI
            self.client = AsterAPI(
                api_key=self.api_key,
                api_secret=self.secret_key,
                base_url=self.base_url,
                ws_url=self.ws_url,
                config=self.account_config
            )
            
    async def get_ws_connection(self):
        """创建WebSocket连接"""
        if self.exchange_name == 'edgex':
            return await websockets.connect(
                self.ws_url,
                proxy=self.proxy
            )
        elif self.exchange_name == 'aster':
            return await websockets.connect(
                self.ws_url,
                proxy=self.proxy
            ) 