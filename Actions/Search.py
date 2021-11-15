import List
import os
import List
import Create


# There should be an action that clones the module from npm to then download it
def find_bucket(name_searching):
    searching_words = get_words(name_searching)

    # Get the list of all buckets
    list_of_buckets = List.list_buckets()

    # Search for the bucket depending if it's a string or a list
    for bucket in list_of_buckets:
        if type(searching_words) == list:
            for word in searching_words:
                if word in bucket.name:
                    return bucket
        else:
            if searching_words in bucket.name:
                return bucket


def get_words(name_searching):
    # Get the primary words on the string with no nonalpha
    name_searching = name_searching.lower()

    # If the string has non alphabetic characters, get the text only
    if not name_searching.isalpha():
        words_to_look = ""
        for char in name_searching:
            if not char.isalpha() and char != ".":
                words_to_look = name_searching.split(char)
                break
    else:
        words_to_look = name_searching

    return words_to_look


def find_object(bucket_name, name_searching):
    # Get the list of all buckets
    list_of_objects = List.list_objects_in_bucket(bucket_name)

    # Search for the bucket depending if it's a string or a list
    for object_searching in list_of_objects:
        if type(name_searching) == list:
            for word in name_searching:
                if word in object_searching.name:
                    return object_searching.name
        else:
            if name_searching in object_searching.name:
                return object_searching

