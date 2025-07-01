# Movie Recommendation System with Data Analysis

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

This is a Movie Recommendation System that uses collaborative filtering techniques to provide personalized movie recommendations based on user ratings and preferences. The system also includes data cleaning, preprocessing, and exploratory data analysis (EDA) to gain insights into the dataset.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Data Cleaning](#data-cleaning)
- [Data Preprocessing](#data-preprocessing)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Model Training](#model-training)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To use this Movie Recommendation System, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using [pip](https://pip.pypa.io/en/stable/): 
pip install pandas numpy matplotlib seaborn surprise

3. Run the Jupyter Notebook or Python script to perform data cleaning, preprocessing, analysis, and train the recommendation model.

## Usage

To get movie recommendations, users can input their preferences, and the system will return a list of recommended movies based on their ratings and other users' similar preferences.

## Data Sources

The data for this project comes from three CSV files: `movies.csv`, `ratings.csv`, and `tags.csv`. The dataset contains information about movies, user ratings, and user-generated tags.

## Data Cleaning

The data cleaning process involved handling missing values and duplicates. Missing values in the `rating` column were replaced with the median value.

## Data Preprocessing

Data preprocessing steps included merging the three datasets based on common `movieId` and `userId` columns. Timestamp columns were converted to datetime format for time-based analysis.

## Exploratory Data Analysis

EDA was performed to understand the distribution of movie ratings, the most popular movies, and the distribution of movie genres. Time-based analysis was done for tags and ratings to observe trends over time.

## Model Training

The Movie Recommendation System uses the Singular Value Decomposition (SVD) algorithm, a popular collaborative filtering technique, to build the recommendation model. The Surprise library was used to implement and train the SVD model.

## Results

The system provides movie recommendations for each user in the test set. The top N recommendations with the highest predicted ratings are displayed for each user.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or create a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

For any inquiries or collaborations, please feel free to contact me:

- Name: HAJAR BENJAT
- Email: hajarbenjat@gmail.com
- LinkedIn: https://www.linkedin.com/in/hajar-benjat-a92132106/



