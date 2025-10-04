"""Simple training script: loads CSV with features + label, trains RandomForest, saves model."""
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def load_data(path):
df = pd.read_csv(path)
# Expect: features columns + 'label' column (0 = false positive, 1 = planet)
return df


def main(args):
df = load_data(args.data)
X = df.drop(columns=[args.label_col])
y = df[args.label_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
print(classification_report(y_test, preds))

joblib.dump(clf, args.output)
print(f"Saved model to {args.output}")


if __name__ == '__main__':
parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True)
parser.add_argument('--output', default='models/baseline.pkl')
parser.add_argument('--label-col', default='label')
args = parser.parse_args()
main(args)
