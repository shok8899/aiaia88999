# Kiloex TradingView Webhook

这是一个用于接收 TradingView 信号并在 Kiloex 上自动执行交易的 Webhook 服务器。

## 安装

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 配置环境变量:
```bash
cp .env.example .env
```
编辑 .env 文件，填入你的配置信息：
- WALLET_ADDRESS: 你的钱包地址
- PRIVATE_KEY: 你的私钥
- DEFAULT_CHAIN: 使用的链 (BNBTEST, OTEST, MANTA, OPBNB, BNB)
- SLIPPAGE: 滑点设置

## TradingView 配置

1. Alert 设置中的 Webhook URL:
```
http://your_server:5000/webhook
```

2. Alert 消息格式 (JSON):
```json
{
    "symbol": "ETHUSD",
    "side": "buy",
    "leverage": 2,
    "margin": 20
}
```

## 支持的交易对

- ETHUSD (ID: 1)
- BTCUSD (ID: 2)
- BNBUSD (ID: 3)

## 运行服务器

```bash
python webhook_server.py
```

## 特性

- 市价单交易
- 自动滑点保护
- 完整的参数验证
- 详细的错误日志