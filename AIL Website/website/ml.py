import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv('C:\\Users\\mbede\\Desktop\\AIL Website\\website\\gradePredict.csv')

X = df.drop('book_id', axis=1)
y = df['book_id']

label_encoder = LabelEncoder()
X['specialty'] = label_encoder.fit_transform(X['specialty'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=10)


knn = KNeighborsClassifier(n_neighbors=1)


knn.fit(X_train, y_train)

predictions = knn.predict(X_test)


accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

new_data = pd.DataFrame ({
    'course_id': [4007],
    'grade': [100],
    'specialty': ['HTML/CSS'],
    'difficulty': [0],
    'pass': [0]
})

new_data['specialty'] = label_encoder.transform(new_data['specialty'])


prediction = knn.predict(new_data)
print("Predicted Value:", prediction)

model_knn = 'knn_model.pkl'
with open(model_knn, 'wb') as file:
    pickle.dump(knn, file)
    