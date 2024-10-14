# DigiHaul Technical Test

### Purpose

This project houses the notebooks for building, and framework/structure for deploying a model to predict the probability of delay to a delivery from historic delivery data.

This README file explains how to run the notebooks, and explains the solution for deploying the model to production.

### Getting set up

This project uses pipenv to install dependencies. If you do not have pipenv installed you can install it in your base python environment with

```bash
pip install pipenv
```

Once installed, navigate to the project root folder and run
```bash
pipenv install
```

This will install all the requirements from the Pipfile.

Alternatively, if you do not wish to install pipenv, you can create a virtual environment with venv by running

```bash
python3 -m venv .venv

# Activate the environment with
source .venv/bin/activate # Linux
.venv/Scripts/activate # Windows
```
Then install from the requirements.txt file with

```bash
pip install -r requirements.txt
```

### Notebooks

#### data_exploration_cleaning.ipynb

This notebook performs exploratory analysis and feature engineering and cleaning steps, which would then be implemented in the features pipeline script `scripts/features.py` (see below)

#### modelling.ipynb

Takes the dataset created in `data_exploration_cleaning.ipynb` and performs model selection and hyper parameter tuning, evaluation and saves the model to the `/models` folder.

#### distancematrix_api.ipynb

This is an experiment in using an API to calculate expected journey times to compare to the available time between collection and delivery schedules, and fittin a LogisticRegression model to the resulting variable. Given the limitations of the free version of the API, only 1000 records were used for training, but the results do not seem to be at all useful for prediction, which is surprising - further investigation is needed.

## Deployment 
### Scripts

There are 2 script placeholder files (not implemented) in this project:
```
features.py
train.py
```

In deployment, `features.py` would perform ETL on the raw data and store the features in a feature store, using the `DatasetProcessor` class in `components.dataset_processor.py`

From there, `train.py` would pick up the data, create the required artefacts (`carrier_frequencies.pkl`, `labeller.pkl` and `power_transformer.pkl`), train and evaluate the model, then write all the artefacts to storage (normally S3 or equivalent) with a `latest` tag.

### App

`app.py` (not implemented) would be a Flask or FastAPI application that serves the model via http POST requests with the required fields in JSON format. It should perform transformations on the data using the artefacts created during training, as well as the `DatasetProcessor.transform()` method (although this requires modification for handling HTTP requests instead of a Pandas DataFrame object.)


The API should return a JSON response similar to the below.

```json
{
    "status": "string",
    "predcitions": [
        {"probability": "float"},
    ]
}
```

HTTP POST requests to the `/predict` endpoint trigger inferencing.

### Dockerfile

A simple Dockerfile to build the image from the project files.
The image exposes port 8000, allowing the model to be accessed viat HTTP requests.

### pipeline.yml

An <b>example</b> pipeline using GitHub Actions to build, test and push the Docker image to ECR when a pull request is created in the master branch.

### components/

Artefacts created during training that are needed during inference.

### tests/

Unit/integration testing of classes and functions (not implemented.)