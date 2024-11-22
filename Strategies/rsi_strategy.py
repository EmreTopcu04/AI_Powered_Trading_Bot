from .strategy_interface import TradingStrategy
import pandas as pd

class RSIStrategy(TradingStrategy):
    def __init__(self, stop_loss, smoothing_period=14):
        super().__init__(stop_loss, smoothing_period)

    def decide_action(self, row, df):
        """Train the model on the updated data and predict the action for the given row."""
        # Train the model on the updated data
        self.train_model(df, ['rsi', 'adx', 'macd', 'Close', 'Volume'], self.label_logic)
        
        # Extract features for prediction
        features = self._get_features(row, ['rsi', 'adx', 'macd', 'Close', 'Volume'])
        
        # Predict and return the action (Buy, Sell, Hold)
        prediction = self.model.predict(features)[0]
        print(f"Predicted action: {prediction}")
        print("Dataframe tail:", df.tail())
        return prediction

    def label_logic(self, row):
        """Labeling logic specific to RSI strategy."""
        # Apply smoothing to RSI
        row_df = pd.DataFrame([row])


        smoothed_rsi = row_df['rsi'].rolling(window=self.smoothing_period).mean().iloc[-1]

        if smoothed_rsi < 30:
            return "Buy"
        elif smoothed_rsi > 70:
            return "Sell"
        return "Hold"
