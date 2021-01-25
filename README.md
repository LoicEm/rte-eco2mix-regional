# rte-eco2mix-regional: data ingestion

France's electricity production is avalaible in near-realtime through [RTE eco2mix](https://www.rte-france.com/en/eco2mix).

## Goal: produce a clean, up-to-date dataset to produce up-to-date predictions

The data available through the eco2mix is updated every hour, and only runs on a period between now and the past month.
I want to persist this data in my own architecture, and use it as a base to build predictions over the next 24 hours.

This repo is part of my rte-project, it handles data ingestion and cleaning, before pushing it to a MongoDB database.

## Tools:

This is the occasion for me to use some of the most exciting tools that are available to data engineering.
Each component will have it's own README:
- [Data ingestion orchestration with Prefect](flows/README.md)

## Total budget: 0€

One of the challenges I set is to spend exactly 0€ on this project: this is made possible by using resources availables in the [GCP Free Tier](https://cloud.google.com/free)