import pandas as pd
import numpy as np

# Function to add noise to numerical columns
def add_noise(column, noise_factor=0.05):
    if np.issubdtype(column.dtype, np.number):
        noise = np.random.normal(0, noise_factor, size=column.shape)  # Add noise based on the standard deviation
        return column + noise
    return column


def add_gaussian_noise(column, mu=0, sigma=1):
    if np.issubdtype(column.dtype, np.number):
        noise = np.random.normal(mu, sigma, size=column.shape)
        return column + noise
    return column


# Function to perturb categorical columns
def perturb_categories(column, perturbation_prob=0.05):
    unique_values = column.unique()
    perturbed = column.copy()
    for i in range(len(column)):
        if np.random.rand() < perturbation_prob:  # Random chance to perturb
            perturbed[i] = np.random.choice(unique_values)
    return perturbed

if __name__ == "__main__":
    df = pd.read_json("../data/original_data.json", orient='columns')
    
    batch_size = 44
    target_size = 3300
    current_size = df.shape[0]
    iterations = target_size // batch_size

    # Initialize the augmented DataFrame with the original 44 records
    df_augmented = df.copy()

    # Iteratively create new batches of 44 records, progressively adding more noise
    for i in range(1, iterations):
        # Duplicate the original 44 records
        df_new_batch = df.copy()

        # Increase noise factor with each iteration
        # noise_factor = 0.05 * i
        # perturb_prob = 0.05 * i

        sigma = 0.1 * i  # Start small and progressively increase the noise (standard deviation)
        perturb_prob = 0.05 * i  # Increase the chance of perturbation for categorical columns

        # Apply noise to numerical columns
        for col in df_new_batch.select_dtypes(include=[np.number]).columns:
            df_new_batch[col] = add_gaussian_noise(df_new_batch[col], mu=0, sigma=sigma)

        # Apply perturbation to categorical columns
        for col in df_new_batch.select_dtypes(include=['object']).columns:
            df_new_batch[col] = perturb_categories(df_new_batch[col], perturb_prob)

        # Append the new batch to the augmented DataFrame
        df_augmented = pd.concat([df_augmented, df_new_batch], ignore_index=True)

        # Stop once we have 2000 records
        if df_augmented.shape[0] >= target_size:
            df_augmented = df_augmented.iloc[:target_size]
            break

    # Check the final DataFrame
    print(df_augmented.head())
    print(f"Shape of augmented DataFrame: {df_augmented.shape}")
    
    json_data = df_augmented.to_json(orient='records', indent=4)

    # Optionally, save the JSON data to a file
    with open('../data/augmented_data_gaussian_noise_3300.json', 'w', encoding="utf-8") as file:
        file.write(json_data)

