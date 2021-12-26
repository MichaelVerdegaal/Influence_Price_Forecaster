from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import r2_score

from config import unpickle_obj, save_model
from source.evaluation import plot_fit_curves

# Split dataset
df = unpickle_obj('dataset_influence-crew_1728_augmented')
dtypes = unpickle_obj('dataset_influence-crew_dtypes')
labels = df.pop('sales.price')

X_train, X_test, y_train, y_test = train_test_split(df, labels, random_state=5, train_size=0.8)

# Compile model
model = Sequential()
model.add(Dense(500, activation='relu'))
model.add(Dense(1))

model.compile(loss=mean_squared_error, optimizer=Adam(0.00001))

# Train model
hist = model.fit(X_train, y_train,
                 batch_size=4,
                 validation_split=0.2,
                 epochs=500)

# Evaluate model
plot_fit_curves(hist)
test_results = model.evaluate(X_test, y_test)
print("Test loss", test_results)
y_pred = model.predict(X_test)
print("R2 score", r2_score(y_test, y_pred))

# Store model
save_model(model, f"model_influence_crew_{len(df)}")
