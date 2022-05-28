market_options = {
    "wazirx": {
        "markets": {"url": 'https://api.wazirx.com/api/v2/market-status',
                    "key": "",
                    "fn": lambda response: [i['baseMarket'] for i in response['markets']]},
        "tickers": {"url": 'https://api.wazirx.com/api/v2/tickers',
                    "per_fn": lambda k,v: (v['base_unit'],float(v['last'])) if v['quote_unit'] == 'inr' else None},
        "historical": {"url": 'https://x.wazirx.com/api/v2/k?market=%m&period=%p&limit=%l&timestamp=%t',
        
                    },
    
    
    "coinbase": {
        "markets": {"url": 'https://api.coinbase.com/v2/exchange-rates?currency=INR',
                    "pre_key": "['data']['rates'].keys()",
                    "fn": lambda x: [y.lower() for y in list(x)]},
        "tickers": {"url": 'https://api.coinbase.com/v2/exchange-rates?currency=INR',
                    "pre_key": "['data']['rates']",
                    "per_fn": lambda k, v: (k.lower(), 1.0/float(v))}
    },
}
}
