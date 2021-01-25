# Using Prefect to orchestrate data ingestion

Eco2mix data is published every hour, so the workflow is very simple. 
Every hour, request the API to get results that were not fetched yet.
As there are some inconsistencies in the data (e.g a specific region has not published its data for a given hour), each run queries all the data in the past 24 hours.

Once this data is fetched, a little bit of preprocessing is done as to put it in a standardized format, then data is pushed to a Pub/Sub system to be consumed by our applications.

## What is Prefect ?

[Prefect](https://docs.prefect.io/) is a workflow management system, which I will use here to create the same identical workflow every hour.

## Getting started

### Requirements

- Have [Prefect installed](https://docs.prefect.io/core/getting_started/installation.html) and be [logged in Prefect Cloud]() (or in your own deployment of prefect server)
- Have [Docker](https://docs.docker.com/get-docker/) up and running
- Optionnally, have a docker image sharing system in place if you plan to run your agent on a distant computer. I use [DockerHub](https://hub.docker.com/) for that purpose.
- Setup a GCP Service account key as Prefect `GCP_CREDENTIALS` secret ([doc](https://docs.prefect.io/orchestration/concepts/secrets.html#cloud-execution))

### Deploying and running a flow

- To send a flow to Prefect cloud, use `prefect register flow -f flows/scraping.py`
- You can then start your agent via `prefect agent docker start`. It will run the docker containers.
- Flow runs every hour by default. If you want to test a flow run right now, you can request it via `prefect run flow -n regional_data -p test`

## Next steps

- Build a second flow ingesting consolidated data every month.