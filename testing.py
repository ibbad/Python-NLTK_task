#!/usr/bin/python
import os
import sys
from stopword_removal import remove_stopwords, perform_imports


def get_filenames_from_directory(directory):
    """
    This function reads name of all test sequences in dataset/json category
    and returns in form of a list.
    :param directory: path to directory from where the files must be read.
    :return:
    """
    from os import walk
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend(filenames)
        break
    return files


def verify_no_stopwords(infile=None, language=None):
    """
    This function checks if there are any stop words from the given language
    available in the file.
    :param infile: file whose text needs to be checked.
    :param language: language whose stop words need to be checked.
    :return:
    """
    # verify that output file does not have any stop_words
    from textract import process
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
    tokens = wordpunct_tokenize(process(infile).decode('UTF-8'))
    stop_words = stopwords.words(language)
    for word in stop_words:
        if word in tokens:
            return False
    return True


def run_test(input_folder=None):
    """
    This function tests the stopword_removal function using some sample files.
    """
    if input_folder is None:
        print("Please specify the folder for input_sample_pdf files.")
        sys.exit(1)
    perform_imports()
    # read all files in the directory.
    samples = get_filenames_from_directory(input_folder)
    count = 0
    for sample in samples:
        remove_stopwords(in_file=input_folder+'/'+sample,
                         out_file=input_folder+'/'+sample[:-3]+'txt')

        count += 1 if verify_no_stopwords(
            infile=input_folder+'/'+sample[:-3]+'txt',
            language=sample.split('.')[0].split('-')[0]) else 0

    if count < len(samples):
        print('Test failed for {failed} languages'.format(failed=count))
    else:
        print('All tests passed')

    # remove all files
    for sample in samples:
        try:
            os.remove(input_folder+'/'+sample[:-3]+'txt')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    run_test(input_folder='input_files')