README for the Classifier Prediction Code

This script is designed to perform classification tasks using pre-trained classifiers (CLF_HCSO and CLF_CHT) on data extracted from various feature files. The process involves loading the data, making predictions using classifiers, and outputting the results in a CSV format.
Requirements:

    Python Libraries: The following Python libraries are required:
        pandas
        pickle
        numpy
        copy
        glob
    Pre-trained Models: The script uses two sets of pre-trained classifiers (CLF_HCSO and CLF_CHT), which are loaded from a pickle file (Random_forest_22_11.pkl).

Main Functions:
1. used_classifier(CLF_HCSO, CLF_CHT, DF)

This function applies two sets of classifiers (CLF_HCSO and CLF_CHT) on the input DataFrame DF and outputs a DataFrame of predictions.

    Input Parameters:
        CLF_HCSO: A list of pre-trained classifiers for the first stage of prediction.
        CLF_CHT: A list of pre-trained classifiers for the second stage of prediction.
        DF: The DataFrame containing the features to be used for prediction.

    Process:
        Extracts a predefined set of features (Index_RF) from the DataFrame DF.
        Uses CLF_HCSO classifiers to make initial predictions and stores them in DF_prediction.
        If the prediction is classified as 'Other', it uses the CLF_CHT classifiers to refine the prediction.
        Returns a final DataFrame (DF_final_prediction) with the predicted labels and associated probabilities.

    Output:
        A DataFrame containing the prediction results with columns for time, date, line, larva ID, predicted label, and prediction probability.

2. load_and_concat_files(path_pattern)

This function loads and concatenates multiple .pkl files from a specified directory pattern using glob.

    Input Parameters:
        path_pattern: A string representing the path pattern to search for .pkl files.
    Process:
        Finds all files matching the pattern.
        Loads each file as a DataFrame using pd.read_pickle().
        Concatenates the DataFrames column-wise.
    Output:
        A combined DataFrame from all the matching files.

Workflow:

    Load Pre-trained Models: The pre-trained classifiers are loaded from a pickle file (Random_forest_22_11.pkl) using pickle.load().

    Load Feature Data: The script defines paths to directories containing feature data for different conditions (e.g., hunch weak, bend large). It uses the function load_and_concat_files() to load and concatenate feature files from these directories.

    Concatenate Feature Data: The individual feature DataFrames (df_hunch, df_bend_t2, df_hunch_weak_t2) are concatenated into a single DataFrame (DF), which is passed to the classifier.

    Make Predictions: The used_classifier() function is called to predict labels for the concatenated DataFrame. The function uses the classifiers to assign labels and probabilities.

    Save Predictions: The resulting prediction DataFrame (DF_prediction) is saved as a CSV file (DF_prediction.csv).

Notes:

    The pre-trained classifiers should be stored in a pickle file, and the feature files should be available in the specified directories.
    Ensure that the paths for input and output directories (path_in, path_out, path_data) are properly defined before running the script.