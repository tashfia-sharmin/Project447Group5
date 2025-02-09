import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_validation(input_file="data.csv", train_ratio=0.8, random_seed=27):
    # Load the dataset
    df = pd.read_csv(input_file)

    # Split into training and validation sets
    train_df, val_df = train_test_split(df, train_size=train_ratio, random_state=random_seed, shuffle=True)

    # Save the split data
    train_df.to_csv("train_split.csv", index=False)
    val_df.to_csv("validation_split.csv", index=False)

    print(f"Training set size: {len(train_df)}")
    print(f"Validation set size: {len(val_df)}")

# Run the split function
split_train_validation()