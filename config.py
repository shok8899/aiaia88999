import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 钱包配置
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# 交易配置
DEFAULT_CHAIN = os.getenv('DEFAULT_CHAIN', 'BNBTEST')  # 可选: BNBTEST, OTEST, MANTA, OPBNB, BNB
SLIPPAGE = float(os.getenv('SLIPPAGE', '0.001'))  # 默认滑点：0.1%

# 产品映射
SYMBOL_TO_PRODUCT_ID = {
    'ETHUSD': 1,
    'BTCUSD': 2,
    'BNBUSD': 3,
}