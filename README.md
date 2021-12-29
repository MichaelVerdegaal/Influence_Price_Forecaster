# Price forecaster
![](https://img.shields.io/badge/python-v3.8-blue)

This project is for the purpose of predicting current sell prices of NFT items using the 
traits of an item. It includes a data feed module, an ANN training module and an ANN testing module.

While the project is centered around the Influence project, most of the infrastructure has been designed to be as collection-agnostic as possible. So don't hestitate to fork!


## Table of contents
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Dependencies](#dependencies)
  - [Run](#run)

## Installation
### Requirements

- Python 3.8+
- [Poetry installation](https://python-poetry.org/docs/) for dependency management

### Dependencies

- Install packages via `poetry install`

### Run 

To run:
- Prepare an OpenSea API key, and set it as the environment variable with name `OS_API_KEY`
- Run `data_feed_script.py` to get a dataset
- Optionally but recommended, run `data_augment_script.py` to augment an existing dataset with extra data
- Run `train_model_script.py` to train a neural network model
- Run `manual_prediction_script.py` to manually test a trained model. This will require some configuration
