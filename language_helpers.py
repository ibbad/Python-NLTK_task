import json

# Read the file
with open('lang_dir.json') as lang_data:
    lang_directory = json.load(lang_data)


def get_language_name(key=None):
    """
    This function returns language full name for the given key.
    :param key: two character key ISO 639-1 standard for the language.
    :return: language name in string format
    """
    if key is not None and key in lang_directory.keys():
        return lang_directory.get(key)["lang_name"]
    else:
        return None
