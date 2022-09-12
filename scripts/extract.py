""" Extract historical data from INMET.

This script extracts historical yearly data from INMET's website, storing zipped
files at the data directory, as well as unzipping the files and storing the
output at the extracted directory. This script is meant to be run after the
bootstrap script.
"""
import sys
import zipfile
import logging
import os
import requests

# Sets up logging mechanism and format.
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

LIST_OF_YEARS = [2000]
ARCHIVE_URL = "https://portal.inmet.gov.br/uploads/dadoshistoricos"
DIRECTORY = ["raw", "intermediate_state"]

for directory in DIRECTORY:
    match os.path.exists(directory):
        case True:
            logging.info("Directory %s already exists. Skipping.", directory)
        case False:
            logging.info("Directory %s doesn't exist. Creating.", directory)
            try:
                os.mkdir(directory)
            except Exception as error:
                logging.error("Unable to create directory %s. Exiting.", directory)
                raise error
        case _:
            logging.error("Unknown type on directory match. Exiting.")
            raise TypeError

logging.info("Initiating download of zipped data.")
for year in LIST_OF_YEARS:

    filename = f"{year}.zip"
    url = f"{ARCHIVE_URL}/{filename}"
    output_file = f"{DIRECTORY[0]}/{filename}"

    try:
        logging.info("Downloading zipped file: %s", filename)
        req = requests.get(url, stream=True, timeout=60, allow_redirects=True)
        with open(output_file, "wb") as output:
            for chunk in req.iter_content(chunk_size=8192, decode_unicode=True):
                output.write(chunk)
        logging.info("Successfully downloaded file %s", filename)
    except Exception as error:
        logging.error("Unable to download zipped file. Exiting.")
        raise error

logging.info("Initiating extraction of data from zipped files.")
try:
    for files in os.listdir(DIRECTORY[0]):
        logging.info("Unzipping file: %s", files)
        try:
            with zipfile.ZipFile(f"{DIRECTORY[0]}/{files}", "r") as zip_ref:
                zip_ref.extractall(DIRECTORY[1])
        except Exception as error:
            logging.error("Unable to unzip file %s. Exiting.", files)
            raise error
        logging.info("Successfully unzipped file %s", files)
except Exception as error:
    logging.error("Unable to list files from the raw directory. Exiting.")
    raise error

logging.info("Extracting successful. Exiting.")
sys.exit(0)
