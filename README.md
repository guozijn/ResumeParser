# ResumeParser

A utility to make handling many resumes easier by automatically pulling contact information, required skills and custom text fields. These results are then surfaced as a convenient summary CSV.

## Quick Start Guide

```bash
# Install requirements
pip install -r requirements.txt

# Retrieve language model from spacy
python -m spacy download en_core_web_sm
python -m spacy download zh_core_web_sm

# Run code (with default configurations)
cd bin/
python main.py

# Review output
open ../data/output/resume_summary.csv

```

## Getting started

### Repo structure

 - `bin/main.py`: Code entry point
 - `confs/confs.yaml.template`: Configuration file template
 - `data/input/example_resumes`: Example resumes, which are parsed w/ default configurations
 - `data/output/resume_summary.csv`: Results from parsing example resumes

### Python Environment

Python code in this repo utilizes packages that are not part of the common library. To make sure you have all of the 
appropriate packages, please use `pip` to install the `requirements.txt` file. For more details, please see the [pip 
documentation](https://pip.pypa.io/en/stable/user_guide/#requirements-files)

### Configuration file

This program utilizes a configuration file to set program parameters. You can run this program with the default
parameters view sample output, but you'll probably want to create a config file and modify it to get the most value
from this program.

```bash

# Create configuration file from template
scp confs/confs.yaml.template confs/confs.yaml

# Modify confs to match your needs
open confs/confs.yaml
```

The configuration file has a few parameters you can tweak:
 - `resume_directory`: A directory containing resumes you'd like to parse
 - `summary_output_directory`: Where to place the .csv file, summarizing your resumes
 - `data_schema_dir`: The directory to store table schema. This is mostly for development purposes
 - `skills`: A YAML list of skills. Each element in this list can either be a string (e.g. `skill1` or
 `machine learning`), or a list aliases for the same skill (e.g. `[skill2_alias_A, skill2_alias_B]` or `[ml,
 machine learning, machine-learning]`)
 - `universities`: A YAML list of universities you'd like to search for


## Resume Screening with Supervised Learning

Resume screening is a classic binary classification problem that can be solved using supervised learning algorithms.

### Add labels to resume_summary.csv

Open the resume_summary.csv, add the label column, and fill in the data of 0 or 1 in it. 1 indicates that the screening passes, and 0 indicates that the screening fails.

```bash
# Run training code
cd bin/
python training.py

In this example, we assume that the dataset contains two columns: 'text' which contains the text of resumes, and 'label' which contains the labels (1 for passed screening, 0 for failed screening). We use TF-IDF for feature extraction and Logistic Regression for training and prediction. Finally, we print the accuracy and classification report of the model.
```

### Prediction

After training, you can perform inference (or prediction) using the trained model. Here are the general steps for performing inference with a trained model:

Prepare the data for prediction: Obtain the resumes you want to predict on. These data should have the same format and features as the training data. If you've converted resume text into feature vectors, you'll need to process the new resume text using the same method.

Feature extraction: Extract features from the resumes you want to predict on. This typically involves using the same method (such as TF-IDF) to convert text into feature vectors.

Perform prediction with the trained model: Input the extracted feature vectors into the trained model, and use the model's predict method to make predictions. The model will output the predicted class (passed screening or failed screening).

Interpret the prediction results: Based on the model's prediction, you'll know which category the new resume is classified into. You can interpret the prediction results or take further actions as needed.

Here's a simple example code demonstrating how to perform inference with the trained model:

```bash
```
