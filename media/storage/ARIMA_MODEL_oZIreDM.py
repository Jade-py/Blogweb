import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

#ARIMA MODEL
data = {
    'Year': [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
             2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'Unemployment_Rate': [8.4, 8.5, 8.7, 8.6, 8.7, 8.3, 6.1, 8.3, 5.6, 8.1,
                          8.0, 8.1, 7.9, 7.8, 26.4, 22.9, 31.2, 5.1, 7.5, 23.6]
}
df = pd.DataFrame(data)
df.set_index('Year', inplace=True)

# Splitting the dataset into train and test sets
train = df[:8]
test = df[8:]

# ARIMA model (p=1, d=1, q=1)
model = ARIMA(train, order=(1, 1, 1))
model_fit = model.fit()

# Predicting and evaluating the model
predictions = model_fit.forecast(steps=len(test))
mse = mean_squared_error(test, predictions)
rmse = np.sqrt(mse)

print("RMSE: ", rmse)

# Plotting the results
plt.plot(train, label="Training Data")
plt.plot(test, label="Actual Unemployment Rate")
plt.plot(test.index, predictions, label="Predicted Unemployment Rate")
plt.xlabel("Year")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.show()

#LSTM MODEL
data = {
    'Year': [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
             2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    'Unemployment_Rate': [8.4, 8.5, 8.7, 8.6, 8.7, 8.3, 6.1, 8.3, 5.6, 8.1, 8.0,
                          8.1, 7.9, 7.8, 26.4, 22.9, 31.2, 5.1, 7.5, 23.6]
}
df = pd.DataFrame(data)
df.set_index('Year', inplace=True)

# Data preprocessing
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df)

# Train-test split
train_size = int(len(scaled_data) * 0.8)
train, test = scaled_data[:train_size], scaled_data[train_size:]

# Convert data to LSTM input format
def create_dataset(data, look_back=1):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

look_back = 1
X_train, y_train = create_dataset(train, look_back)
X_test, y_test = create_dataset(test, look_back)

X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# LSTM model
model = Sequential()
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2)

# Predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse scaling
train_predict = scaler.inverse_transform(train_predict)
y_train = scaler.inverse_transform([y_train])
test_predict = scaler.inverse_transform(test_predict)
y_test = scaler.inverse_transform([y_test])

# Evaluation
mse_train = mean_squared_error(y_train[0], train_predict[:, 0])
mse_test = mean_squared_error(y_test[0], test_predict[:, 0])

print(f'Train MSE: {mse_train:.2f}')
print(f'Test MSE: {mse_test:.2f}')

# Plot
plt.plot(df.index[:train_size], y_train[0], label="Training Data")
plt.plot(df.index[:train_size: -1], y_test[0], label="Actual Unemployment Rate")
plt.plot(df.index[:train_size: -1], test_predict[:, 0], label="Predicted Unemployment Rate")
plt.xlabel("Year")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.show()
