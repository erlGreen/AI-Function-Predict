import tensorflow as tf
import numpy as np
# import tkinter.filedialog as tk
# import easygui
import matplotlib.pyplot as plt
from dataProcessing import dataProcessing
from functions import Buy, Sell

sequence = 100
maxfilenr = 20
# input("Press enter and choose file")
restore = input("Restore model?(y/n)\n")
if restore == "y":
    file = "./model.mdl"
    model = tf.keras.models.load_model(file)
    print("model restored")
else:
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(20, input_shape=(None, 3 * sequence,), return_sequences=True))
    model.add(tf.keras.layers.LSTM(20, return_sequences=False))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer="sgd", loss="mean_squared_error")
mode = input("Train or predict? (t/p)\n")
if mode == "t":
    for i in range(0, 2):
        processedData = dataProcessing(maxfilenr, 0)
        processedData.generateData(sequence)
        x_data = processedData.input
        y_data = processedData.output
        x_data = np.reshape(x_data, (x_data.shape[0], 1, x_data.shape[1]))
        model.fit(x_data, y_data, epochs=100)
else:
    filename = "./test.csv"
    processedData = dataProcessing(0, filename)
    processedData.generateData(sequence)
    x_data = processedData.input
    y_data = processedData.output
    x_data = np.reshape(x_data, (x_data.shape[0], 1, x_data.shape[1]))
    predictions = model.predict(x_data)
    predictionsTable = [item for sublist in predictions for item in sublist]
    predictionsTable[:] = [x * processedData.normalizeValue for x in predictionsTable]
    processedData.values[:] = [x * processedData.normalizeValue for x in processedData.values]
    plt.plot(list(range(0, len(processedData.values))), processedData.values, "b-", list(range(sequence, len(predictionsTable) + sequence)), predictionsTable, "r-")
    plt.show()
    nrOfActions = 0
    money = 10 * processedData.values[sequence - 1]
    startingMoney = money
    for i in range(0, len(predictionsTable)):
        if processedData.values[i + sequence - 1] < predictionsTable[i] and money > processedData.values[i + sequence - 1]:
            money, nrOfActions = Buy(money, nrOfActions, processedData.values[i + sequence - 1])
        else:
            if processedData.values[i + sequence - 1] > predictionsTable[i] and nrOfActions > 0:
                money, nrOfActions = Sell(money, nrOfActions, processedData.values[i + sequence - 1])
    money += nrOfActions * processedData.values[len(processedData.values) - 1]
    gain = 100 * money / startingMoney
    print("Total gain is " + str(gain - 100) + "%")
model.save("model.mdl")
print("model saved")
