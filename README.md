# Overview
This is the official python client for the FalconX API.

API Documentation: http://docs.falconx.io

# Installation
```sh
pip install falconx
```

# Quickstart

```python
from falconx import FalconxClient

client = FalconxClient(key=KEY, secret=SECRET, passphrase=PASSPHRASE)
quote = client.get_quote('BTC', 'USD', 5, 'two_way')
result = client.execute_quote(quote['fx_quote_id'], 'buy')
```

# About FalconX
FalconX is an institutional digital asset brokerage. 
