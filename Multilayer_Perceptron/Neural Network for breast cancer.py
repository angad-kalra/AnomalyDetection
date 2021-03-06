import pandas
import tensorflow as tf
import pandas as pd
import numpy as np
from time import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from numpy import array
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA as sklearnPCA
from sklearn import preprocessing
import matplotlib.pyplot as plt


def readData(path, all_feature):


    kdd_data = pandas.read_csv(path, header=None)

    if(all_feature):
        return kdd_data
    else:

        numeric_kdd_data = kdd_data[numeric_vals].astype(float)
        return numeric_kdd_data


def perform_one_hot_encoding(kdd_training_data, kdd_test_data):

    label_encoder = LabelEncoder()
    enc = OneHotEncoder(sparse=False)
    training_out = kdd_training_data
    testing_out = kdd_test_data

    kdd_training_data['label']=kdd_training_data['label'].apply(lambda x : "attack." if(x != "normal.") else "normal.")# if x != "normal.")
    kdd_test_data['label']=kdd_test_data['label'].apply(lambda x : "attack." if x != "normal." else "normal.")

    for col in text_cols:

        data = kdd_training_data[[col]].append(kdd_test_data[[col]])
        print("unique shit in ", col, len(np.unique(data.values)),np.unique(data.values))

        label_encoder.fit(data.values.ravel())

        kdd_training_data[col] = label_encoder.transform(kdd_training_data[col])


        kdd_test_data[col] = label_encoder.transform(kdd_test_data[col])

    for col in text_cols:

        data = kdd_training_data[[col]].append(kdd_test_data[[col]])
        enc.fit(data)
        temp = enc.transform(kdd_training_data[[col]])
        # print(col)
        # print(temp)
        # print([i for i in data[col].value_counts().index])

        temp = pd.DataFrame(temp, columns=[(col + "_" + str(i)) for i in data[col].value_counts().index])
        # In side by side concatenation index values should be same
        # Setting the index values similar to the X_train data frame
        temp = temp.set_index(kdd_training_data.index.values)
        # adding the new One Hot Encoded varibales to the train data frame
        training_out = pd.concat([training_out, temp], axis=1)
        training_out.drop(col, axis=1, inplace=True)



        # fitting One Hot Encoding on test data

        temp1 = enc.transform(kdd_test_data[[col]])
        # changing it into data frame and adding column names
        temp1 = pd.DataFrame(temp1, columns=[(col + "_" + str(i)) for i in data[col]
                            .value_counts().index])
        # Setting the index for proper concatenation
        temp1 = temp1.set_index(kdd_test_data.index.values)
        # print(temp1)
        # adding the new One Hot Encoded varibales to test data frame
        testing_out = pd.concat([testing_out, temp1], axis=1)
        testing_out.drop(col, axis=1, inplace=True)


    return training_out, testing_out

def preprocess_data(kdd_data):
    cols = list(kdd_data.columns.values)
    # labels = kdd_data['label'].copy()
    # labels[labels!='normal.'] = 'attack.'
    # labels.value_counts()
    x = kdd_data.values

    sklearn_pca = sklearnPCA(n_components=10)
    kdd = pd.DataFrame(sklearn_pca.fit_transform(preprocessing.normalize(x, norm='l2')))

    # kdd = pd.DataFrame(MinMaxScaler(feature_range=(0, 100)).fit_transform(sklearn_pca.fit_transform(preprocessing.normalize(x, norm='l2'))))
    # kdd = pd.DataFrame()

    return kdd

def train_neural_net(training_data, testing_data):


    # Make results reproducible
    seed = 1234
    np.random.seed(seed)
    tf.set_random_seed(seed)


#     dataset = pd.read_csv('Iris_Dataset.csv')
#     dataset = pd.get_dummies(dataset, columns=['Species']) # One Hot Encoding
    values = list(training_data.columns.values)
    count = 2

    print("col values ", values)
    print("values[-count:]",values[-count:])
    print("values[1 : -count]",values[1 : -count])

    #need to determine col names dynamically


    y = training_data[values[-count:]]
    y_train = np.array(y, dtype='float32')
    y2 = testing_data[values[-count:]]
    y_test = np.array(y2, dtype = 'float32')
    # print(y_test, len(y_test))

    X = training_data[values[1:-count]]
    X_train = np.array(X, dtype='float32')
    X2 = testing_data[values[1 : -count]]
    X_test = np.array(X2, dtype = 'float32')


    # Shuffle Data
    indices = np.random.choice(len(X_train), len(X_train), replace=False)
    # print(indices)
    X_train_values = X_train[indices]
    y_train_values = y_train[indices]

    # print(X_train_values)
    # print(y_train_values)
    # exit()

    indices = np.random.choice(len(X_test), len(X_test), replace=False)
    X_test_values = X_test[indices]
    y_test_values = y_test[indices]

    # Session
    sess = tf.Session()

    # Interval / Epochs
    interval = 50
    epoch = 1000

    num_of_features = len(values) - count -1
    print(num_of_features)
    # Initialize placeholders
    X_data = tf.placeholder(shape=[None, num_of_features], dtype=tf.float32)
    print(X_data.shape)
    y_target = tf.placeholder(shape=[None, count], dtype=tf.float32)
    print(y_target.shape)


    # Input neurons : 4
    # Hidden neurons : 8
    # Output neurons : 3
    hidden_layer_nodes = num_of_features + 10

    # Create variables for Neural Network layers
    w1 = tf.Variable(tf.random_normal(shape=[num_of_features,hidden_layer_nodes], stddev=0.03)) # Inputs -> Hidden Layer
    b1 = tf.Variable(tf.random_normal(shape=[hidden_layer_nodes]))   # First Bias

    w2 = tf.Variable(tf.random_normal(shape=[hidden_layer_nodes, hidden_layer_nodes], stddev=0.03)) # Inputs -> Hidden Layer
    b2 = tf.Variable(tf.random_normal(shape=[hidden_layer_nodes]))   # First Bias

    w3 = tf.Variable(tf.random_normal(shape=[hidden_layer_nodes,count], stddev=0.03)) # Hidden layer -> Outputs
    b3 = tf.Variable(tf.random_normal(shape=[count]))   # Second Bias

    # Operations
    # hidden_output1 = tf.placeholder(shape= [None, hidden_layer_nodes], dtype=tf.float32)



    hidden_output1 = tf.nn.relu(tf.add(tf.matmul(X_data, w1), b1))
    print("hidden_output1 shape" , hidden_output1.shape)
    hidden_output2 = tf.nn.relu(tf.add(tf.matmul(hidden_output1, w2), b1))
    print("hidden_output2 shape" , hidden_output2.shape)


    # w3_clipped = tf.clip_by_value(final_output, 1e-10, 0.9999999)

    final_output = tf.nn.softmax(tf.add(tf.matmul(hidden_output2, w3), b3))

    print("final_output shape" , hidden_output2.shape)


    # Cost Function
    final_output_clipped = tf.clip_by_value(final_output, 1e-10, 0.9999999)

    loss = -tf.reduce_mean(tf.reduce_sum(y_target * tf.log(final_output_clipped)
                         + (1 - y_target) * tf.log(1 - final_output_clipped), axis=1))

    # loss = tf.reduce_mean(-tf.reduce_sum(tf.squeeze(y_target) * tf.squeeze(tf.log(final_output_clipped)), axis=0))
    # loss = tf.reduce_mean(tf.squared_difference(tf.squeeze(y_target),
    #        tf.squeeze(final_output_clipped)))

    # Optimizer
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss)

    # Initialize variables
    init = tf.global_variables_initializer()
    sess.run(init)
    print(X_train_values[0:1,:].shape)
    print(y_train_values[0:1,:].shape)
    # Training

    # for i in range(5):
    #     curr_W, curr_b, curr_loss,final = sess.run([w1, b1, loss, tf.log(final_output)], feed_dict={X_data: X_train_values[0:1,:], y_target: y_train_values[0:1,:]})
    #     print("Iteration %d W: %s b: %s loss: %s %s"%(i, curr_W, curr_b, curr_loss,final))

    print('Training the model...')
    for i in range(1, (epoch + 1)):
        # curr_W, curr_b, curr_loss,final,hidden_output11, w21, b21, X_data1, softmax_inp, y_tar = sess.run([w1, b1, loss, final_output, hidden_output1, w2, b2, X_data, tf.add(tf.matmul(hidden_output1, w2), b2), y_target], feed_dict={X_data: X_train_values[i:i+1,:], y_target: y_train_values[i:i+1,:]})
        # print("Iteration %d \nW: %s \nb: %s \nloss: %s \n\n\n\n final: %s \nhidden:%s \nw2: %s\n b2: %s \nX_data: %s\n softmaxin %s \n y_val %s"%(i, curr_W, curr_b, curr_loss,final,hidden_output11, w21, b21, X_data1,softmax_inp,y_tar))
        sess.run(optimizer, feed_dict={X_data: X_train_values, y_target: y_train_values})

        # if i % interval == 0:
            # print(sess.run(hidden_output, feed_dict={X_data: X_train_values[0:1,:], y_target: y_train_values[0:1,:]}))
            # for i in range(5):
                # curr_W, curr_b, curr_loss,final,hidden_output1, w21, b21, X_data1 = sess.run([w1, b1, loss, tf.log(final_output), hidden_output, w2, b2, X_data], feed_dict={X_data: X_train_values[0:1,:], y_target: y_train_values[0:1,:]})
                # print("Iteration %d W: %s b: %s loss: %s %s %s %s %s %s"%(i, curr_W, curr_b, curr_loss,final,hidden_output1, w21, b21, X_data1))

            # print("final_output ",sess.run(final_output, feed_dict={X_data: X_train_values[0:1,:], y_target: y_train_values[0:1,:]}))
        print('Epoch', i, '|', 'Loss:', sess.run(loss, feed_dict={X_data: X_train_values, y_target: y_train_values}))


    # Prediction
    # print()
    predicted_list = []
    positive = 0
    negative = 0

    print(y_test_values)
    for i in range(len(X_test_values)):

        fout = sess.run([final_output_clipped], feed_dict={X_data: [X_test_values[i]]})
        print("final_output " , fout)

        predicted_class = np.rint(sess.run(final_output_clipped, feed_dict={X_data: [X_test_values[i]]}))
        p_l = predicted_class.tolist()[0]
        predicted_list.append(p_l)
        actual = y_test_values[i:i+1,-count:].tolist()
        print(actual[0],p_l)
        if actual[0] == p_l:
            positive += 1
        else:
            negative += 1
        # print('Actual:',actual , 'Predicted:',predicted_class )

    print("accuracy ",positive/(positive + negative), "positive predictions ", positive, "negative prediction ", negative)



if __name__ == '__main__':
    #Change path here to actual file path.
    data = readData("/home/arpit/Downloads/KDD/breast-cancer-unsupervised-ad.csv", True)
    data = data.sample(frac=1).reset_index(drop=True)
    data.hist()
    print("data describe ", data.describe())

    total_rows = len(data.index)
    training_count = int(total_rows * 0.7)
    training = data[0:training_count]
    testing = data[training_count:368]
    print("testing shape", testing.shape)
    print(training.shape)
    print(testing)

    data_cols = data.columns.values[0:-1]
    print("data cols", data_cols)

    text_cols = data.columns.values[-1]
    print("text cols", text_cols)

    # train_textout, test_textout = perform_one_hot_encoding(training[text_cols], testing[text_cols])

    sklearn_pca = sklearnPCA(n_components=10)
    # processed_training = pd.DataFrame(sklearn_pca.fit_transform(training[data_cols].values))
    # processed_testing = pd.DataFrame(sklearn_pca.fit_transform(testing[data_cols].values))
    processed_training = pd.DataFrame(preprocessing.normalize(training[data_cols]))
    processed_testing = pd.DataFrame(preprocessing.normalize(testing[data_cols]))




    final_training = pd.concat([processed_training, pd.get_dummies(training[text_cols])],axis = 1)
    # print("training " , final_training, pd.get_dummies(testing[text_cols]).values.shape)


    tmp = pd.DataFrame(pd.get_dummies(testing[text_cols]).values, index = [i for i in range(0,111)], columns = ['n', 'o'])
    # print("tmp " , tmp)
    final_testing = pd.concat([processed_testing, tmp],axis = 1)

    #save preprocessed data in below file location
    final_training.to_csv(path_or_buf = "/home/arpit/Downloads/KDD/train_full.csv")
    final_testing.to_csv(path_or_buf="/home/arpit/Downloads/KDD/test_full.csv")

    #Actual training is done here and after training code will run teting automatically and should give outlier accuracy in output
    train_neural_net(final_training, final_testing)
