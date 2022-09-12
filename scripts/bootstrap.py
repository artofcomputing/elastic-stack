""" Bootstrapping script for data ingestion.

This script creates the necessary indices for the backfilling phase
and is meant to run in a fresh environment.
"""
import logging
import sys
from elasticsearch import Elasticsearch

# Sets up logging mechanism and format.
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

# NOTE: In this case, for ease of development and simplicity, we're using
# authentication with the elastic superuser. For production environments
# that communicate with the Elastic API, please use the proper mechanisms
# for authentication, and secure your elastic account.
USER = "elastic"
PASSWORD = ""
ELASTIC_IP = ""

try:
    logging.info("Creating Elasticsearch connection object.")
    es_client = Elasticsearch(
        f"https://{ELASTIC_IP}:9200",
        # NOTE: Please note that TLS verification is disabled for this script.
        # For production environments, please use the proper mechanisms for TLS
        # authentication.
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=(USER, PASSWORD),
    )
except Exception as error:
    logging.error("Unable to connect to Elasticsearch Cluster. Aborting.")
    raise error

try:
    logging.info("Checking whether index already exists.")
    inmet_index = es_client.indices.exists(index="inmet")
except Exception as error:
    logging.error("Unable to check whether index exists. Aborting.")
    raise error

match inmet_index.body:
    case True:
        logging.error("Index already exists. Exiting.")
        sys.exit(0)
    case False:
        logging.info("Index doesn't exist. Creating.")
    case _:
        logging.error("Unknown type on index match. Aborting")
        raise TypeError

try:
    logging.info("Creating inmet index.")
    create_index = es_client.indices.create(index="inmet")
except Exception as error:
    logging.error("Unable to create index. Aborting.")
    raise error

logging.info("Bootstrapping successful. Exiting.")
sys.exit(0)
