import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import KNeighborsClassifier

folder_path = "data/"
csv_files = os.listdir(folder_path)
data = []

def rescale_data(data_features, num_features=64):
    if len(data_features.columns) < num_features:
        missing_cols = num_features - len(data_features.columns)
        data_features = pd.concat([data_features, pd.DataFrame(0, index=data_features.index, columns=range(missing_cols))], axis=1)
    elif len(data_features.columns) > num_features:
        data_features = data_features[data_features.columns[:num_features]]
    return data_features

for csv_file in csv_files:
    df = pd.read_csv(os.path.join(folder_path, csv_file))
    df = rescale_data(df, num_features=64)

    # Get features
    features = df.values.flatten()
    data.append(features)

model = KNeighborsClassifier(n_neighbors=4)
model.fit(data, csv_files)  # Train the model on the entire dataset


new_csv_data = pd.read_csv("TestCSV/test.csv")
new_csv_data = rescale_data(new_csv_data, num_features=64)
new_csv_features = new_csv_data.values.flatten()

similarity_scores = cosine_similarity([new_csv_features], data)

threshold = 0.9
most_similar_csv = csv_files[np.argmax(similarity_scores)]
print("Most Similar CSV:", most_similar_csv)