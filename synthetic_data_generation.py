import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Setup Dates
dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
df = pd.DataFrame(index=dates)

# 2. Define the Month-End Exponential Trend
# We calculate the day of the month (1 to 31) and apply an exponential curve
df['day_of_month'] = df.index.day
df['month_trend'] = np.exp(df['day_of_month'] / 10)  # Adjust divisor for steepness

# 3. Handle the "Settlement Multiplier" (Weekend/Holiday logic)
# Count how many days of "activity" settle on a given day
df['is_business_day'] = df.index.dayofweek < 5
# Simple logic: Friday-Sunday activity settles on Monday (3 days)
df['settlement_mult'] = 1
df.loc[df.index.dayofweek == 0, 'settlement_mult'] = 3
df.loc[df.index.dayofweek >= 5, 'settlement_mult'] = 0 # No flow on weekends

# 4. Combine: Base Flow * Trend * Multiplier + Noise
base_volume = 50
noise = np.random.normal(0, 5, len(df))
df['cashflow'] = (base_volume * df['month_trend'] * df['settlement_mult']) + noise

# Ensure no negative flows
df['cashflow'] = df['cashflow'].clip(lower=0)

# 5. Plotting Functionality
fig, ax1 = plt.subplots(figsize=(15, 7))

# Primary Axis: Cashflow
ax1.set_xlabel('Date')
ax1.set_ylabel('Cashflow Volume', color='tab:blue', fontsize=12)
ax1.plot(df.index, df['cashflow'], color='tab:blue', label='Daily Cashflow', linewidth=1.5)
ax1.tick_params(axis='y', labelcolor='tab:blue')
plt.show()