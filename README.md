# CovidStats
Contains various analyses describing the Covid19 pandemic around the globe.

The Covid-19 pandemic has substantially impacted social and economic situations across the globe and taken a number of lives while doing so. This repository is a meager attempt to understand through simple data analysis and visualization which parts of the world are succeeding or failing to control the pandemic, and what factors may be influencing the outcome, so that we can learn to better handle this and similar situations in the future.

This repository currently:
- [x] Produces animated choropleth maps of the globe illustrating the progression over time of Covid-19 cases and mortality rates.
- [ ] Describes correlation between various factors and Covid-19 cases/mortality (coming soon...)

e.g.
![Covid-19 Cases](/gifs/CovidWorldConfirmedCases.gif)
![Covid-19 Case Rate](/gifs/CovidWorldConfirmedRate.gif)
![Covid-19 Mortality Rate](/gifs/CovidWorldMortalityRate.gif)

## How to use this code:
1. Download or clone the repo (at present you really only need /CovidStats.ipynb, /data/covid_19_data2.csv, and /data/world population.csv)
2. Install requirements (or run online e.g. in Colab)
3. Run CovidStats.ipynb
4. Make gifs to share using your favorite screen capture software (I used ScreenToGif) or share your plots on your website using Plotly's own API (not documented here)

## Thoughts for future revisions...
1. Animate correlations between countries and other (more meaningful) indicators, like:
    * GDP
    * Population density
    * Regional temperature
    * Lockdown regulations
    * other indicators...

## References
1. COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University. Downloaded from the [Novel Corona Virus 2019 Dataset](https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset/data?select=covid_19_data.csv) repository on July 30, 2020.
2. [World Bank](https://data.worldbank.org/indicator/SP.POP.TOTL). Retrieved July 21, 2020.

## Acknowledgements
This project was initially inspired by [Terence Shin](https://towardsdatascience.com/visualizing-the-coronavirus-pandemic-with-choropleth-maps-7f30fccaecf5).
