from config_kiloex import kiloconfigs
import market_trade_kiloex
import api_kiloex
from config import SYMBOL_TO_PRODUCT_ID, DEFAULT_CHAIN, SLIPPAGE
import logging

logger = logging.getLogger(__name__)

class TradeHandler:
    def __init__(self):
        self.config = kiloconfigs[DEFAULT_CHAIN]
    
    def get_product_id(self, symbol):
        """根据交易对获取产品ID"""
        product_id = SYMBOL_TO_PRODUCT_ID.get(symbol.upper())
        if not product_id:
            raise ValueError(f"Unsupported symbol: {symbol}")
        return product_id
    
    def execute_trade(self, trade_data):
        """执行市价交易"""
        try:
            # 获取产品ID
            product_id = self.get_product_id(trade_data['symbol'])
            
            # 获取当前市场价格
            market_price = api_kiloex.index_price(product_id)
            logger.info(f"Current market price for {trade_data['symbol']}: {market_price}")
            
            # 交易参数
            is_long = trade_data['side'].lower() == 'buy'
            leverage = float(trade_data['leverage'])
            margin = float(trade_data['margin'])
            
            # 设置市价单的可接受价格（考虑滑点）
            # 做多时，接受高于市价的成交价格
            # 做空时，接受低于市价的成交价格
            acceptable_price = (
                market_price * (1 + SLIPPAGE) if is_long 
                else market_price * (1 - SLIPPAGE)
            )
            
            logger.info(f"Executing {'long' if is_long else 'short'} position: "
                       f"margin={margin}, leverage={leverage}, "
                       f"acceptable_price={acceptable_price}")
            
            # 执行市价交易
            tx_hash = market_trade_kiloex.open_market_increase_position(
                config=self.config,
                product_id=product_id,
                margin=margin,
                leverage=leverage,
                is_long=is_long,
                acceptable_price=acceptable_price,
                referral_code=bytearray(32)
            )
            
            trade_result = {
                'tx_hash': tx_hash.hex(),
                'symbol': trade_data['symbol'],
                'side': 'LONG' if is_long else 'SHORT',
                'market_price': market_price,
                'acceptable_price': acceptable_price,
                'leverage': leverage,
                'margin': margin,
                'status': 'submitted'
            }
            
            logger.info(f"Trade submitted successfully: {trade_result}")
            return trade_result
            
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}", exc_info=True)
            raise