from data import *
from model import *
from constants import *
from tensorflow import keras
from keras.callbacks import EarlyStopping

FILE_TEST = "MAMe_toy_dataset.csv"
FILE_TRAIN = "MAMe_dataset.csv"


def train(model, data, y_vals):
    """
    Train the model
    @param model: the model to train
    @param data: the data to train the model
    """
    x_train = load_images(data[0])
    x_val = load_images(data[2])
    #dataGenerator = DataGenerator(data[0], y_vals[0], BATCH_SIZE)
    validationData = get_valSet(x_val, y_vals[2])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    early = EarlyStopping(monitor='val_loss', min_delta=1e-4, patience=10, verbose=1, mode='auto', restore_best_weights=True)

    mdl_fit = model.fit(x_train, y_vals[0], validation_data=validationData, shuffle=True,epochs=EPOCHS, batch_size=BATCH_SIZE, use_multiprocessing=True,workers=4,callbacks = [early])
    print_results_model(mdl_fit, epochs=16, batch_size=16)
    model.save('model_epochs'+str(EPOCHS)+ '_batchsize'+str(BATCH_SIZE)+'.h5')
    return model
    

def transform_labels(labels_dict, data):
    """
    Transform data strings to numerical labels
    @param labels_dict: dictionary with the labels
    @param data: the data to transform
    @return: the transformed data
    """
    y_train, y_test, y_val = [], [], []
    for x in data[3]:
        y = np.zeros(NUM_CLASSES)
        y[labels_dict[x]] = 1
        y_train.append(y)
    for x in data[4]:
        y = np.zeros(NUM_CLASSES)
        y[labels_dict[x]] = 1
        y_test.append(y)
    for x in data[5]:
        y = np.zeros(NUM_CLASSES)
        y[labels_dict[x]] = 1
        y_val.append(y)
    return (np.array(y_train), np.array(y_test), np.array(y_val))


if __name__ == '__main__':
    labels_dict = load_labels()
    # DATA = (names_images_train, names_images_test, names_images_val, y_train, y_test, y_val)
    data = load_data(FILE_TRAIN) # Data is splitted
    y_vals = transform_labels(labels_dict, data)
    model = get_baseModel()
    model = train(model, data, y_vals)
    #x_test = load_images(data[1])
    #result = predict_model(model, x_test, y_vals[1])
    #print("Total predictions correc: ", result , "%")