import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):

    file = open(filename)
    reader = csv.reader(file)
    next(reader)

    evidence, labels= [], []
    month = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'June':5,'Jul':6,'Aug':7,'Sep':8,'Oct':9,'Nov':10,'Dec':11,}

    for row in reader:
        evidence.append(list(map(float, row[:10])) + [month[row[10]]] + list(map(float,row[11:15])) + [1 if row[15] == 'Returning_Visitor' else 0, 1 if row[16] == 'TRUE' else 0])
        labels.append(1 if row[17] == 'TRUE' else 0)
    
    return (evidence, labels)


def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors = 1)
    
    X_training = [row for row in evidence]
    y_training = [row for row in labels]

    model.fit(X_training, y_training)

    return model


def evaluate(labels, predictions):
    sensitivity = specificity = positive = negative = 0
    for label, prediction in zip(labels, predictions) :
        if label == 1 : 
            positive += 1
            if label == prediction : sensitivity += 1

        else :
            negative += 1
            if label == prediction : specificity += 1

    return (sensitivity/positive, specificity/negative)

if __name__ == "__main__":
    main()
