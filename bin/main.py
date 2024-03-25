#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import argparse
import inspect
import logging
import os
import re
import sys

import pandas
import spacy

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from bin import field_extraction
from bin import lib


def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.getLogger().setLevel(logging.INFO)

    # Add command line arguments
    args = parse_arguments()

    # Extract data from upstream.
    observations = extract(args.config)

    # Spacy: Spacy NLP
    nlp = spacy.load(args.lang + '_core_web_sm')

    # Transform data to have appropriate fields
    observations, nlp = transform(args.config, args.lang, observations, nlp)

    # Load data for downstream consumption
    load(args.config, observations, nlp)

    pass


def extract(config):
    logging.info('Begin extract')

    # Reference variables
    candidate_file_agg = list()

    # Create list of candidate files
    for root, subdirs, files in os.walk(lib.get_conf(config, 'resume_directory')):
        folder_files = map(lambda x: os.path.join(root, x), files)
        candidate_file_agg.extend(folder_files)

    # Convert list to a pandas DataFrame
    observations = pandas.DataFrame(data=candidate_file_agg, columns=['file_path'])
    logging.info('Found {} candidate files'.format(len(observations.index)))

    # Convert the relative path to an absolute path
    observations['file_path'] = observations['file_path'].apply(lambda x: os.path.abspath(x))

    # Subset candidate files to supported extensions
    observations['extension'] = observations['file_path'].apply(lambda x: os.path.splitext(x)[1])
    observations = observations[observations['extension'].isin(lib.AVAILABLE_EXTENSIONS)]
    logging.info('Subset candidate files to extensions w/ available parsers. {} files remain'.
                 format(len(observations.index)))

    # Attempt to extract text from files
    observations['text'] = observations['file_path'].apply(lib.convert_pdf)

    # Add timestamp for each file
    observations['timestamp'] = observations['file_path'].apply(lib.extract_timestamps)

    # Archive schema and return
    lib.archive_dataset_schemas(config, 'extract', locals(), globals())
    logging.info('End extract')
    return observations


def transform(config, lang, observations, nlp):
    # TODO Docstring
    logging.info('Begin transform')

    # Extract candidate name
    observations['candidate_name'] = observations['text'].apply(lambda x:
                                                                field_extraction.candidate_name_extractor(x, nlp, lang))

    if lang == 'en':
        for index, candidate_name in observations['candidate_name'].items():
            if candidate_name == "NOT FOUND":
                match = re.search(field_extraction.NAME_REGEX, observations['text'][index], re.IGNORECASE)
                observations['candidate_name'][index] = match[0]

    # Extract contact fields
    observations['email'] = observations['text'].apply(lambda x: lib.term_match(x, field_extraction.EMAIL_REGEX))
    PHONE_REGEX = field_extraction.PHONE_REGEX if lang == 'en' else field_extraction.PHONE_REGEX_CN

    observations['phone'] = observations['text'].apply(lambda x: lib.term_match(x, PHONE_REGEX))

    # Extract skills
    observations = field_extraction.extract_fields(config, observations)

    # Archive schema and return
    lib.archive_dataset_schemas(config, 'transform', locals(), globals())
    logging.info('End transform')
    return observations, nlp


def load(config, observations, nlp):
    logging.info('Begin load')
    output_path = os.path.join(
        lib.get_conf(config, 'summary_output_directory'), 'resume_summary.csv')

    logging.info('Results being output to {}'.format(output_path))
    print('Results output to {}'.format(output_path))

    observations.to_csv(path_or_buf=output_path, index_label='index')
    logging.info('End transform')
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument(
        '--config',
        default='../confs/config.yaml',
        help='Path to the configuration file')
    parser.add_argument('--lang', default='zh', help='Language')
    args = parser.parse_args()
    return args


# Main section
if __name__ == '__main__':
    main()
