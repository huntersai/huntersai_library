import requests

class HunterAIClient:
    def __init__(self, api_key, token):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.hunterai.io"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-HAT-Token": self.token,
            "Content-Type": "application/json",
        }

    def get_crypto_data(self, symbol):
        """Retrieve real-time data for a specific cryptocurrency."""
        url = f"{self.base_url}/crypto/{symbol}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_trade_recommendation(self, symbol):
        """Get buy/sell recommendations for a cryptocurrency."""
        url = f"{self.base_url}/trade/recommendation/{symbol}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def execute_trade(self, action, symbol, amount):
        """Execute a trade action (BUY/SELL) for a cryptocurrency."""
        url = f"{self.base_url}/trade/execute"
        payload = {
            "action": action,
            "symbol": symbol,
            "amount": amount
        }
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_balance(self):
        """Retrieve account balance."""
        url = f"{self.base_url}/account/balance"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

# Example Usage
if __name__ == "__main__":
    client = HunterAIClient(api_key="your_api_key", token="your_hat_token")

    # Get cryptocurrency data
    btc_data = client.get_crypto_data("BTC")
    print("BTC Data:", btc_data)

    # Get trade recommendation
    eth_recommendation = client.get_trade_recommendation("ETH")
    print("ETH Recommendation:", eth_recommendation)

    # Execute a trade
    trade_result = client.execute_trade("BUY", "ETH", amount=1.0)
    print("Trade Result:", trade_result)

    # Check balance
    balance = client.get_balance()
    print("Account Balance:", balance)