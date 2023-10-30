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

## RFQ in quote token terms
```python
quote = client.get_quote('BTC', 'USD', 5, 'two_way', is_quote_token_quantity=True)
```

## New Order Endpoint
A new faster endpoint is now available to place orders.
The same can be used as mentioned in the below sample.
Optional argument 'v3'. 
If the argument is not passed, the old order (v1/order) endpoint is used.

```python
from falconx import FalconxClient
client = FalconxClient(key=KEY, secret=SECRET, passphrase=PASSPHRASE)
client.place_order('ETH', 'USD', 0.1, 'sell', 'market', v3=True)
```

# About FalconX
FalconX is an institutional digital asset brokerage. 
