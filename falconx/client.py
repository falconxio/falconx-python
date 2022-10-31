import base64
import hashlib
import hmac
import time

import requests
from requests import Response
from requests.auth import AuthBase


class FalconxClient:
    """
    Client for querying the FalconX API using http REST
    """

    def __init__(self,
                 key=None,
                 secret=None,
                 passphrase=None,
                 url='https://api.falconx.io/v1/'):
        self.url = url
        if key and secret and passphrase:
            self.auth = FXRfqAuth(key, secret, passphrase)
        else:
            raise Exception('key, secret and passphrase are necessary for authentication')
        self.session = requests.Session()
        self.session.auth = self.auth

    def _process_response(self, response: Response):
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': response.status_code, 'text': response.text}

    def get_trading_pairs(self):
        """
        Get a list of trading pairs you are eligible to trade
        :return: (list[dict])
            Example: [{'base_token': 'BTC', 'quote_token': 'USD'}, {'base_token': 'ETH', 'quote_token': 'USD'}]
        """
        response = self.session.get(self.url + 'pairs')
        return self._process_response(response)

    def get_quote(self, base, quote, quantity, side, client_order_id=None):
        """
        Get a two_way, buy or sell quote for a token pair.
        :param base: (str) base token e.g. BTC, ETH
        :param quote: (str) quote token e.g. USD, BTC
        :param quantity: (float, Decimal)
        :param side: (str) 'two_way', 'buy', 'sell'
        :return: (dict) Example:
            {
              "status": "success",
              "fx_quote_id": "00c884b056f949338788dfb59e495377",
              "buy_price": 12650,
              "sell_price": null,
              "token_pair": {
                "base_token": "BTC",
                "quote_token": "USD"
              },
              "quantity_requested": {
                "token": "BTC",
                "value": "10"
              },
              "side_requested": "buy",
              "t_quote": "2019-06-27T11:59:21.875725+00:00",
              "t_expiry": "2019-06-27T11:59:22.875725+00:00",

              "is_filled": false,
              "side_executed": null,
              "price_executed": null,
              "t_execute": null,
              "client_order_id": "d6f3e1fa-e148-4009-9c07-a87f9ae78d1a"
            }
        """

        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {
            'token_pair': {
                'base_token': base,
                'quote_token': quote
            },
            'quantity': {
                'token': base,
                'value': str(quantity)
            },
            'side': side,
            "client_order_id": client_order_id
        }

        response = self.session.post(self.url + 'quotes', json=params)
        return self._process_response(response)

    def place_order(self, base, quote, quantity, side, order_type, time_in_force=None, limit_price=None, slippage_bps=None, client_order_id=None):
        """
        Get a two_way, buy or sell quote for a token pair.
        :param base: (str) base token e.g. BTC, ETH
        :param quote: (str) quote token e.g. USD, BTC
        :param quantity: (float, Decimal)
        :param side: (str) 'buy', 'sell'
        :param order_type: (str) 'market', 'limit'
        :param time_in_force: (str) 'fok' [only required for limit orders]
        :param limit_price: (float, Decimal) [only required for limit orders]
        :param slippage_bps: (float, Decimal) [only valid for fok limit orders]
        :return: (dict) Example:
            {
                "status": "success",
                "fx_quote_id": "00c884b056f949338788dfb59e495377",
                "buy_price": 8545.12,
                "sell_price": null,
                "platform": "api",
                "token_pair": {
                    "base_token": "BTC",
                    "quote_token": "USD"
                },
                "quantity_requested": {
                    "token": "BTC",
                    "value": "10"
                },
                "side_requested": "buy",
                "t_quote": "2019-06-27T11:59:21.875725+00:00",
                "t_expiry": "2019-06-27T11:59:22.875725+00:00",
                "is_filled": true,
                "gross_fee_bps": 8,
                "gross_fee_usd": 101.20,
                "rebate_bps": 3,
                "rebate_usd": 37.95,
                "fee_bps": 5,
                "fee_usd": 63.25,
                "side_executed": "buy",
                "trader_email": "trader@company.com",
                "order_type": "limit",
                "time_in_force": "fok",
                "limit_price": 8547.11,
                "slippage_bps": 2,
                "error": null,
                "client_order_id": "d6f3e1fa-e148-4009-9c07-a87f9ae78d1a"
            }
        """

        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {
            'token_pair': {
                'base_token': base,
                'quote_token': quote
            },
            'quantity': {
                'token': base,
                'value': str(quantity)
            },
            'side': side,
            'order_type': order_type,
            'time_in_force': time_in_force,
            'limit_price': limit_price,
            'slippage_bps': slippage_bps,
            "client_order_id": client_order_id
        }

        response = self.session.post(self.url + 'order', json=params)
        return self._process_response(response)

    def execute_quote(self, fx_quote_id, side):
        """
        Execute the quote.
        :param fx_quote_id: (str) the quote id received via get_quote
        :param side: (str) must be either buy or sell
        :return: dict[str,] same as object received from get_quote
            Example:
                {
                    'buy_price': 294.0,
                    'error': None,
                    'fx_quote_id': 'fad0ac687b1e439a92a0bafd92441e48',
                    'is_filled': True,
                    'price_executed': 294.0,
                    'quantity_requested': {'token': 'ETH', 'value': '0.10000'},
                    'sell_price': 293.94,
                    'side_executed': 'buy',
                    'side_requested': 'two_way',
                    'status': 'success',
                    't_execute': '2019-07-03T21:45:10.358335+00:00',
                    't_expiry': '2019-07-03T21:45:17.198692+00:00',
                    't_quote': '2019-07-03T21:45:07.198688+00:00',
                    'token_pair': {'base_token': 'ETH', 'quote_token': 'USD'}
                }

        """

        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {
            'fx_quote_id': fx_quote_id,
            'side': side
        }

        response = self.session.post(self.url + 'quotes/execute', json=params, auth=self.auth)
        return self._process_response(response)

    def get_quote_status(self, fx_quote_id):
        """
        Check the status of a quote already requested.
        :param fx_quote_id: (str) the quote id received via get_quote
        :return: dict]; Same quote object as returned by get_quote
            Example:
                {
                  "status": "success",
                  "fx_quote_id": "00c884b056f949338788dfb59e495377",
                  "buy_price": 12650,
                  "sell_price": null,
                  "platform": "api",
                  "token_pair": {
                    "base_token": "BTC",
                    "quote_token": "USD"
                  },
                  "quantity_requested": {
                    "token": "BTC",
                    "value": "10"
                  },
                  "side_requested": "buy",
                  "t_quote": "2019-06-27T11:59:21.875725+00:00",
                  "t_expiry": "2019-06-27T11:59:22.875725+00:00",

                  "is_filled": false,
                  "side_executed": null,
                  "price_executed": null,
                  "t_execute": null,
                  "trader_email": "trader1@company.com"
                }
        """
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        return self._process_response(self.session.get(self.url + 'quotes/{}'.format(fx_quote_id)))

    def get_executed_quotes(self, t_start, t_end, platform=None):
        """
        Get a historical record of executed quotes in the time range.
        :param t_start: (str) time in ISO8601 format (e.g. '2019-07-02T22:06:24.342342+00:00')
        :param t_end: (str) time in ISO8601 format (e.g. '2019-07-03T22:06:24.234213+00:00'
        :param platform: possible values -> ('browser', 'api', 'margin')
        :return: list[dict[str,]]
            Example:
                [{'buy_price': 293.1, 'error': None, 'fx_quote_id': 'e2e1758f1a094a2a85825b592e9fc0d9',
                'is_filled': True, 'price_executed': 293.1, 'platform': 'browser', 'quantity_requested': {'token': 'ETH', 'value': '0.10000'},
                'sell_price': 293.03, 'side_executed': 'buy', 'side_requested': 'two_way', 'status': 'success',
                't_execute': '2019-07-03T14:02:56.539710+00:00', 't_expiry': '2019-07-03T14:03:02.038093+00:00',
                't_quote': '2019-07-03T14:02:52.038087+00:00',
                'token_pair': {'base_token': 'ETH', 'quote_token': 'USD'}, 'trader_email': 'trader1@company.com'},

                {'buy_price': 293.1, 'error': None, 'fx_quote_id': 'fc17a0d884444a0db5a7d9568c6c3f70',
                'is_filled': True, 'price_executed': 293.03, 'platform': 'api', 'quantity_requested': {'token': 'ETH', 'value': '0.10000'},
                'sell_price': 293.03, 'side_executed': 'sell', 'side_requested': 'two_way', 'status': 'success',
                't_execute': '2019-07-03T14:02:46.480337+00:00', 't_expiry': '2019-07-03T14:02:50.454222+00:00',
                't_quote': '2019-07-03T14:02:40.454217+00:00', 'token_pair': {'base_token': 'ETH', 'quote_token': 'USD'},
                'trader_email': 'trader2@company.com'}]

        """
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {'t_start': t_start, 't_end': t_end, 'platform': platform}
        return self._process_response(self.session.get(self.url + 'quotes', params=params))

    def get_balances(self, platform=None):
        """
        Get account balances.
        :param platform: possible values -> ('browser', 'api', 'margin')
        :return: list[dict[str, float]]
            Example:
                [
                    {'balance': 0.0, 'token': 'BTC', 'platform': 'browser'},
                    {'balance': -1.3772005993291505, 'token': 'ETH', 'platform': 'api'},
                    {'balance': 187.624207, 'token': 'USD', 'platform': 'api'}
                ]
        """
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        return self._process_response(self.session.get(self.url + 'balances', params={'platform': platform}))

    def get_transfers(self, t_start=None, t_end=None, platform=None):
        """
        Get a historical record of deposits/withdrawals between the given time range.

        :param t_start: (str) time in ISO8601 format (e.g. '2019-07-02T22:06:24.342342+00:00')
        :param t_end: (str) time in ISO8601 format (e.g. '2019-07-03T22:06:24.234213+00:00'
        :param platform: possible values -> ('browser', 'api', 'margin')
        :return: list[dict[str,]]
            Example:
                [
                  {
                    "type": "deposit",
                    "platform": "api",
                    "token": "BTC",
                    "quantity": 1.0,
                    "t_create": "2019-06-20T01:01:01+00:00"
                  },
                  {
                    "type": "withdrawal",
                    "platform": "midas",
                    "token": "BTC",
                    "quantity": 1.0,
                    "t_create": "2019-06-22T01:01:01+00:00"
                  }
                ]

        """
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {'t_start': t_start, 't_end': t_end, 'platform': platform}
        return self._process_response(self.session.get(self.url + 'transfers', params=params))

    def get_trade_volume(self, t_start, t_end):
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {'t_start': t_start, 't_end': t_end}
        return self._process_response(self.session.get(self.url + 'get_trade_volume', params=params))

    def get_30_day_trailing_volume(self):
        response = self.session.get(self.url + 'get_30_day_trailing_volume')
        return self._process_response(response)

    def get_trade_limits(self, platform):
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        return self._process_response(self.session.get(self.url + 'get_trade_limits/{}'.format(platform)))

    def submit_withdrawal_request(self, token, amount, platform):
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        params = {'token': token, 'amount': amount, 'platform': platform}
        return self._process_response(self.session.post(self.url + 'withdraw', params=params))

    def get_rate_limits(self):
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        response = self.session.get(self.url + 'rate_limit')
        return self._process_response(response)

    def get_trade_sizes(self):
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        response = self.session.get(self.url + 'trade_sizes')
        return self._process_response(response)

    def get_total_balances(self):
        if not self.auth:
            raise Exception("Authentication is required for this API call")

        response = self.session.get(self.url + 'balances/total')
        return self._process_response(response)

    def get_derivatives(self, trade_status=None, product_type=None, market_list=None):
        """
        Get all derivative trade data with current mark-to-market data.

        Args:
            trade_status: possible values -> ('open', 'closed', 'settled', 'defaulted')
            product_type: possible values -> ('ndf', 'call_option', 'put_option', 'irs', 'option')
            market_list: comma separated list, e.g. 'BTC-USD,ETH-USD'
        Return:
            list[dict]
            # Example Response =>
            [
                {
                    "counterparty_margin_percent": {
                        "value": 15.0,
                        "token": "USD"
                    },
                    "daily_mark": {
                        "value": -2.0,
                        "token": "USD"
                    },
                    "delta": -262.0,
                    "effective_date": null,
                    "fixing_expiry_time": "4pm NYC",
                    "market": "BTC/USD",
                    "maturity_date": "2022-02-26T00:00:00+00:00",
                    "option_type": "put",
                    "premium": {
                        "token": "USD",
                        "value": 100000.00
                    },
                    "product": "option",
                    "quantity": 100.0,
                    "side": "sell",
                    "status": "open",
                    "spot_reference_price": {
                        "token": "USD",
                        "value": 20010.0
                    },
                    "strike_price": {
                        "token": "USD",
                        "value": 20000.0
                    },
                    "trade_date": "2022-02-26T00:03:00+00:00",
                    "trade_id": "13db3a3f832e444a90435e900d1c3222",
                    "trade_notional": {
                        "token": "USD",
                        "value": 2001000.0
                    },
                    "trader": "william@client.co",
                    "trading_entity": "solios",
                    "vega": {
                        "value": -272.0
                        "token": "USD"
                    }
                }
            ]
        """
        if not self.auth:
            raise Exception('Authentication is required for this API call')

        params = {
            'trade_status': trade_status,
            'product_type': product_type,
            'market_list': market_list,
        }

        return self._process_response(self.session.get(self.url + 'derivatives', params=params))

# Authentication class for requests library
class FXRfqAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        request_body = request.body.decode() if request.body else ''
        message = timestamp + request.method + request.path_url + request_body
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'FX-ACCESS-SIGN': signature_b64,
            'FX-ACCESS-TIMESTAMP': timestamp,
            'FX-ACCESS-KEY': self.api_key,
            'FX-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
