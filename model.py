from statsmodels.tsa.stattools import ccf
import statsmodels.api as sm

# Identify holidays in our range
from pandas.tseries.holiday import USFederalHolidayCalendar
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=dates.min(), end=dates.max())
df['is_holiday'] = df.index.isin(holidays).astype(int)

# Calculate Cross-Correlation between Holidays and Cashflow
# This tells us if the "shock" happens before or after the holiday date
cross_corr = ccf(df['cashflow'], df['is_holiday'])

# Print top lags to see where the correlation is highest
for i in range(-3, 4):
    corr = df['cashflow'].corr(df['is_holiday'].shift(i))
    print(f"Correlation at Lag {i}: {corr:.3f}")


# Create lead/lag features
df['h_lead'] = df['is_holiday'].shift(-1).fillna(0)
df['h_lag'] = df['is_holiday'].shift(1).fillna(0)

# We include the 'month_trend' as a regressor to handle the exponential growth
exog = df[['settlement_mult', 'h_lead', 'h_lag', 'month_trend']]
model = sm.tsa.ARIMA(df['cashflow'], exog=exog, order=(1,1,1))
results = model.fit()

print(results.summary())