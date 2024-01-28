import pandas as pd
import os
import sys


def main():
    if len(sys.argv) != 5:
        print("Incorrect number of arguments provided.")
        print("Correct Usage: python topsis.py <inputfile.csv> <'1,1,1,1'> <'+,+,-,+'> <result.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)
    if not input_file.endswith('.csv'):
        print(f"Incorrect file format for input: {input_file}")
        sys.exit(1)

    dataset = pd.read_csv(input_file)
    if dataset.shape[1] < 3:
        print("Input file must have at least 3 columns.")
        sys.exit(1)

    for i in range(1, len(dataset.columns)):
        dataset.iloc[:, i] = pd.to_numeric(dataset.iloc[:, i], errors='coerce').fillna(dataset.iloc[:, i].mean())
    try:
        weights = [int(w) for w in sys.argv[2].split(',')]
    except ValueError:
        print("Invalid format in weights. Please recheck.")
        sys.exit(1)

    impacts = sys.argv[3].split(',')
    if not all(imp in ['+', '-'] for imp in impacts):
        print("Impacts must be '+' or '-'. Please recheck.")
        sys.exit(1)

    if len(weights) != len(impacts) or len(dataset.columns) != len(weights) + 1:
        print("Mismatch in the number of columns, weights, and impacts.")
        sys.exit(1)

    output_file = sys.argv[4]
    if not output_file.endswith('.csv'):
        print("Incorrect file format for output.")
        sys.exit(1)
    if os.path.isfile(output_file):
        os.remove(output_file)

    apply_topsis(dataset, weights, impacts, output_file)

def apply_topsis(dataset, weights, impacts, output_file):
    dataset_normalized = normalize_dataset(dataset, weights)

    positive_ideal, negative_ideal = calculate_ideal_solutions(dataset_normalized, impacts)

    score = calculate_topsis_score(dataset_normalized, positive_ideal, negative_ideal)
    dataset['Topsis Score'] = score
    dataset['Rank'] = dataset['Topsis Score'].rank(method='max', ascending=False).astype(int)

    dataset.to_csv(output_file, index=False)

def normalize_dataset(dataset, weights):
    dataset_normalized = dataset.copy()
    for i in range(1, len(dataset.columns)):
        norm = (dataset.iloc[:, i]**2).sum()**0.5
        dataset_normalized.iloc[:, i] = (dataset.iloc[:, i] / norm) * weights[i-1]
    return dataset_normalized

def calculate_ideal_solutions(dataset, impacts):
    positive_ideal = []
    negative_ideal = []
    for i in range(1, len(dataset.columns)):
        if impacts[i-1] == '+':
            positive_ideal.append(dataset.iloc[:, i].max())
            negative_ideal.append(dataset.iloc[:, i].min())
        else:
            positive_ideal.append(dataset.iloc[:, i].min())
            negative_ideal.append(dataset.iloc[:, i].max())
    return positive_ideal, negative_ideal

# Calculate the TOPSIS score
def calculate_topsis_score(dataset, positive_ideal, negative_ideal):
    scores = []
    for index, row in dataset.iterrows():
        positive_distance = sum((row[1:] - positive_ideal)**2)**0.5
        negative_distance = sum((row[1:] - negative_ideal)**2)**0.5
        scores.append(negative_distance / (positive_distance + negative_distance))
    return scores

if __name__ == "__main__":
    main()
