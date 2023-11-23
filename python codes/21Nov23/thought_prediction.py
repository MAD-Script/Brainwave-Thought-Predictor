import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

folder_path = "data/"
csv_files = os.listdir(folder_path)
data = []


def rescale_data(df, num_features=64):
    if len(df.columns) < num_features:

        #If not enough columns then pad with extras
        missing_cols = num_features - len(df.columns)
        df = pd.concat([df, pd.DataFrame(0, index=df.index, columns=range(missing_cols))], axis=1)
    elif len(df.columns) > num_features:

        #If too many columns then remove extras
        df = df[df.columns[:num_features]]
    return df

for csv_file in csv_files:
    df = pd.read_csv(os.path.join(folder_path, csv_file))
    df = rescale_data(df, num_features=64)

    # Get features
    features = df.values.flatten() 
    data.append(features)

X_train, X_test, y_train, y_test = train_test_split(data, csv_files, test_size=0.2, random_state=42)

model = KNeighborsClassifier(n_neighbors=9)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")

new_csv_data = []  
new_csv_data = rescale_data(new_csv_data, num_features=64)  #Check if new data has same no. of columns as training data
new_csv_features = new_csv_data.values.flatten()
similarity_scores = cosine_similarity([new_csv_features], X_train)


#Find the most similar csv
threshold = 0.9
similar_csv = [csv_files[i] for i, score in enumerate(similarity_scores[0]) if score >= threshold]
print("Similar Words:", similar_csv)