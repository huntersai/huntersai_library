import json
import example_utils
from hunterai_client import setup_client
from hyperliquid.utils import constants


def main():
    # Setup HunterAI client and Hyperliquid exchange
    client = setup_client()
    address, info, exchange = example_utils.setup(base_url=constants.TESTNET_API_URL, skip_ws=True)

    # Specify the cryptocurrency to trade
    symbol = "ETH"

    try:
        # Step 1: Get trade signal from HunterAI
        print(f"Fetching trade signal for {symbol}...")
        signal = client.predict(symbol)
        print(f"Trade Signal from HunterAI for {symbol}: {signal}")

        # Step 2: Ensure signal is actionable (BUY or SELL)
        if signal not in ["BUY", "SELL"]:
            print(f"No actionable signal for {symbol}. Skipping trade.")
            return

        # Step 3: Get the user state and print out positions
        user_state = info.user_state(address)
        positions = []
        for position in user_state["assetPositions"]:
            positions.append(position["position"])
        if positions:
            print("Open positions:")
            for position in positions:
                print(json.dumps(position, indent=2))
        else:
            print("No open positions.")

        # Step 4: Place an order based on the signal
        is_buy = signal == "BUY"
        print(f"Placing {'BUY' if is_buy else 'SELL'} order for {symbol}...")
        order_result = exchange.order(symbol, is_buy, 0.2, None, {"market": {}})
        print("Order Result:", json.dumps(order_result, indent=2))

        # Step 5: Query the order status by oid
        if order_result["status"] == "ok":
            status = order_result["response"]["data"]["statuses"][0]
            if "resting" in status:
                oid = status["resting"]["oid"]
                print(f"Order is resting. Querying status for OID: {oid}...")
                order_status = info.query_order_by_oid(address, oid)
                print("Order Status:", json.dumps(order_status, indent=2))

                # Optionally cancel the order if required
                print(f"Canceling order for OID: {oid}...")
                cancel_result = exchange.cancel(symbol, oid)
                print("Cancel Result:", json.dumps(cancel_result, indent=2))
        else:
            print("Order execution failed. Please check the details.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

