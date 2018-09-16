# AnomalyDetection
A lot of work has been done in the field of anomaly detection especially in the field of cyber security and medical diagnosis. But, due to the ever-increasing threats to human health and network systems, it
is difficult to identify these. </br>
As a part of comparative analysis, I have implemented a number of algorithms on each dataset so as to come up with some modifications in parameters
and conditions in order to optimize the classification model.</br>
I implemented the work done in the following paper to enhance the performance of One-class Support Vector Machine on the datasets.</br>
The datasets used in this project are KDD Unsupervised dataset (network intrusion detection) and Breast cancer
dataset (Breast cancer diagnostics).</br>
## Data preprocessing
**Uniformation of data -**</bt>
The instances consist of various data types of feature values which might pose a problem where our algorithms will
need to work with numeric values for mathematical equations. Therefore, the initial step of pre-processing data is to
convert all the feature values into uniform type. Textual characters and alphanumeric values are converted into
numeric values for data uniformity for mathematical calculations.</br>
**Normalization of data -**</br>
The next step in pre-processing data is normalization of instances in order to avoid larger computational costs and
scale the values in order to achieve efficient weights and values.
## Feature extraction
**RandomForest-**</br>
RandomForest is a collection of decision trees where the dataset is divided randomly and each subset is fed
to every decision tree. The trees fit the data and intuitively, each decision tree provides weights to features and vote
the features according to their relevance and importance. The majority voted features among these are considered to
be highly discriminating features amongst others.</br>
RandomForests can compress very high amount of data and can deliver high quality models. As this uses a number of
trees for data fitting, it is very quick to train.</br>
**Principle component analysis-**</br>
PCA measures the data based on the principle components instead of basis vectors. It is a dimensionality
reduction technique where projections of all data points is taken on vector that has unique representation for each point
and maximizes variance.
### Algorithms implemented
#### Supervised Learning algorithms
##### 1. K-Nearest Neighbours
The goal of our project is to build a system which will return the result whether the data is normal or an
outlier/Anomaly. The main idea of kNN is to classify based on closet training data/examples of the feature
space/dataset. That’s why it’s one of the main reason behind choosing kNN in our project as it classifies the data
easily based on its neighbors’ value/properties.</br>
**- Cross validation**</br>
![image](https://user-images.githubusercontent.com/22276437/45594612-c34f2180-b952-11e8-99cf-7451e9729d65.png) </br>
To prevent overfitting without the requirement of a large testing set, cross validation is a best technique. It is
used to overcome the traditional process of partitioning the data into test data and training data in some ratio
(usually 30/70 or 40/60).</br>
##### 2. Multivariate Gaussian Model
##### 3. Multi-layer perceptron
#### Semi-supervised Learning algorithms
##### 1. One-class Support Vector Machine
##### 2. Eta One-class Support Vector Machine
