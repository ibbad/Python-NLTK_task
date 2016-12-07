#! /usr/bin/python

import sys

try:
    import nltk
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
    # nltk.download()
except ImportError:
    print('Please install nltk library')

try:
    from langdetect import detect
except ImportError:
    print('Please install Langdetect library (pip install langdetect)')

try:
    from textract import process
except ImportError:
    print('Please install textract (pip install textract)')

from language_helpers import get_language_name

# Read pdf file
file_name = sys.argv[1]
text = process('input_files/' + file_name)

text = text.decode('utf-8')
print(text)

# detect the language
lang = detect(text)
print("lang:"+lang)
lang_name = get_language_name(key=lang)
print("language-detected: " + lang_name)

# Remove stop words
tokens = wordpunct_tokenize(text)
stop_words = stopwords.words(lang_name)
print("stopwords:" + str(stop_words))

filtered = [word for word in tokens if word not in stop_words]

# save to file.
output_file = open('output_files/' + file_name + '.txt', 'w+')
output_file.write(' '.join([w for w in filtered]))
output_file.close()

print('Done')
