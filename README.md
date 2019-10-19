# Overview
This is the official API client for the FalconX API.

API Documentation: http://docs.falconx.io


# Quickstart

```python
from falconx_py import FalconxClient

fnx = FalconxClient(key=KEY, secret=SECRET, passphrase=PASSPHRASE)

quote = fnx.get_quote('BTC', 'USD', 5, 'two-way')

result = fnx.execute_quote(quote['fx_quote_id'], 'buy')
```

# Installation
```sh
pip install falconx-py
```

# About FalconX
FalconX is an institutional digital asset brokerage. 
