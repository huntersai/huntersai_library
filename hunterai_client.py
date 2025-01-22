import json
import os
import requests
from eth_account.signers.local import LocalAccount
import eth_account


class HunterAIClient:
    def __init__(self, config_path="config.json", base_url=None, model_url=None):
        with open(config_path, "r") as f:
            config = json.load(f)
        self.api_key = config["api_key"]
        self.token = config["token"]
        self.account: LocalAccount = eth_account.Account.from_key(config["secret_key"])
        self.address = config.get("account_address", self.account.address)
        self.base_url = base_url or "https://api.hunterai.io"
        self.model_url = model_url or "https://grafana.hunterai.io/predict"
        print("Initialized with account address:", self.address)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-HAT-Token": self.token,
            "Content-Type": "application/json",
        }

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}, Response: {response.text}")
            raise

    def predict(self, symbol):
        """
        Use the HunterAI model to predict a buy or sell signal for a given cryptocurrency.
        """
        url = self.model_url
        payload = {"symbol": symbol}
        response = requests.post(url, json=payload, headers=self._headers())
        data = self._handle_response(response)

        # Assuming the response contains a 'signal' key with either "BUY" or "SELL"
        signal = data.get("signal", "UNKNOWN")
        print(f"Prediction for {symbol}: {signal}")
        return signal

    def get_crypto_data(self, symbol):
        """Retrieve real-time data for a specific cryptocurrency."""
        url = f"{self.base_url}/crypto/{symbol}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def get_trade_recommendation(self, symbol):
        """Get buy/sell recommendations for a cryptocurrency."""
        url = f"{self.base_url}/trade/recommendation/{symbol}"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)

    def execute_trade(self, action, symbol, amount):
        """Execute a trade action (BUY/SELL) for a cryptocurrency."""
        url = f"{self.base_url}/trade/execute"
        payload = {
            "action": action,
            "symbol": symbol,
            "amount": amount,
        }
        response = requests.post(url, json=payload, headers=self._headers())
        return self._handle_response(response)

    def get_balance(self):
        """Retrieve account balance."""
        url = f"{self.base_url}/account/balance"
        response = requests.get(url, headers=self._headers())
        return self._handle_response(response)


def setup_client(base_url=None, model_url=None):
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    return HunterAIClient(config_path=config_path, base_url=base_url, model_url=model_url)


if __name__ == "__main__":
    client = setup_client()

    # Example usage
    try:
        # Predict buy/sell signal
        signal = client.predict("BTC")
        print("Signal for BTC:", signal)

        # Optional: Execute trade based on the prediction
        if signal == "BUY":
            trade_result = client.execute_trade("BUY", "BTC", amount=1.0)
            print("Trade Result:", trade_result)
        elif signal == "SELL":
            trade_result = client.execute_trade("SELL", "BTC", amount=1.0)
            print("Trade Result:", trade_result)

        # Check balance
        balance = client.get_balance()
        print("Account Balance:", balance)

    except Exception as e:
        print("An error occurred:", e)
