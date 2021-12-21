from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mean_squared_error, mean_absolute_percentage_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from config import unpickle_obj
from source.evaluation import plot_fit_curves

# Split dataset
df = unpickle_obj('dataset_influence-crew_7275')
labels = df['sales.price']
X_train, X_test, y_train, y_test = train_test_split(df, labels, random_state=5, train_size=0.8)

# Compile model
model = Sequential()
model.add(Dense(100, activation='relu'))  # Input layer
model.add(Dense(1))  # Output layer

model.compile(loss=mean_squared_error, optimizer=Adam(0.00001), metrics=[mean_absolute_percentage_error])

# Train model
hist = model.fit(X_train, y_train,
                 batch_size=4,
                 validation_split=0.1,
                 epochs=250)

# Evaluate model
plot_fit_curves(hist)
plot_fit_curves(hist, train_metric='mean_absolute_percentage_error', val_metric='val_mean_absolute_percentage_error')

