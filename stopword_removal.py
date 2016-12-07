"""
This script reads a given pdf file, detects language, removes stopwords and
write the data to a text file.
"""

import sys
import getopt
import logging


def _install_package(package_name):
    """
    This function install the required package using pip.
    :param package_name: python package name.
    :return: True if successfully installed, False otherwise
    """
    import pip
    import os
    if os.getuid() != 0:
        print("Unable to install {pkg} because user is not SUDO. Permission "
              "denied.".format(pkg=package_name))
        return False
    try:
        logging.info('Installing {pkg} using pip.'.format(pkg=package_name))
        pip.main(['install', package_name])
        return True
    except Exception as e:
        logging.error("Error {err} during installing {pkg} using "
                      "pip.".format(err=str(e), pkg=package_name))
        return False


def perform_imports():
    """
    This function performs the necessary imports for the module.
    :return:
    """
    try:
        # For natural language processing
        import nltk
    except ImportError:
        logging.warn('NLTK library not found, installing NLTK library using '
                     'pip...')
        if not _install_package('nltk'):
            logging.error('Unable to install NLTK, please install manually.')
            exit(1)

    try:
        # Google library for detecting language.
        from langdetect import detect
    except ImportError:
        logging.warn('Langdetect library not found.Installing langdetect using '
                     'pip...')
        if not _install_package('langdetect'):
            logging.error('Unable to install langdetect, please install '
                          'manually.')
            exit(1)
    try:
        # For reading PDF files.
        import textract
    except ImportError:
        logging.warn('Textract library not found, installing textract using '
                     'pip...')
        if not _install_package('textract'):
            logging.error('Unable to install textract, please install manually')
            exit(1)


def _is_pdf(file_name=None):
    # TODO: Must be a more detailed check
    if file_name[-3:].lower() != 'pdf':
        return False
    return True


def remove_stopwords(in_file=None, out_file=None):
    """
    This function gets the input text, detects the language, retrieves stop
    words and returns text (string) with stop words removed.
    :param in_file: PDF file from which text needs to be read.
    :param out_file: path where output file should be written. if not
    provided, output file is writte to same path with .txt extension using
    input file name.
    :return:
    """
    if _is_pdf(in_file) is None:
        logging.warning('Input file is not PDF.')
        return None

    from textract import process
    from langdetect import detect
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
    from language_helpers import get_language_name

    # FIXME: issue 6.
    text = process(in_file).decode('UTF-8')
    logging.debug('Text successfully read from {ifile}'.format(ifile=in_file))
    language = get_language_name(key=detect(text))
    logging.debug('Detected language: {lang}'.format(lang=language))

    tokens = wordpunct_tokenize(text)
    try:
        try:
            stop_words = stopwords.words(language)
        except LookupError:
            logging.error('Unable to find data for nltk.corpas. '
                          'Please download.')
            import nltk
            nltk.download()
            stop_words = stopwords.words(language)
    except OSError:
        logging.error('Stopwords corpus not available for '
                      '{lang}'.format(lang=language))
        print('Detected language:{lang}. No stop words available for this '
              'language')
        sys.exit(-2)

    filtered_text = ' '.join([word for word in tokens
                              if word not in stop_words])

    if out_file is None:
        output_file = open(in_file[:-3]+'txt', 'w+')
    else:
        output_file = open(out_file, 'w+')
    output_file.write(filtered_text)
    output_file.close()
    return True


def main(argv):
    """
    Main function handling the input and output arguments and perfoming
    stopword_removal operations
    :param argv: command line arguments
    :return:
    """
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["infile=", "outfile="])
    except getopt.GetoptError:
        print("Use stopword_removal -h  for usage information.")
        sys.exit(-2)
    try:
        infile = None
        outfile = None
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('Usage: \n'
                      'stopword_removal -i <input_pdf_file> -o '
                      '<output_text_file>\n'
                      'stopword_removal --infile <input_pdf_file> --outfile '
                      '<output_text_file>\n')
                sys.exit()
            elif opt in ('-i', '--infile'):
                infile = arg
            elif opt in ('-o', '--outfile'):
                outfile = arg
        if infile is None:
            print("Use stopword_removal -h for usage information.")
            sys.exit(2)
        perform_imports()
        if remove_stopwords(infile, outfile):
            print("Successfully removed stop words.")
            sys.exit(0)
        else:
            print("Operation not completed successfully.")
            sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
