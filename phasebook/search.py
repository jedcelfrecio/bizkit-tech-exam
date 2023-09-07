from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    if len(args) == 0:
        return USERS # No arguments means return all users

    results = []
    value = ""

    for field in args: # Will get results for each key as they are ordered in the query string (Part of bonus challenge)

        value = args[field]

        if field == "id":
            merge_results_with_unique_users(results, get_user_with_id(value))
        elif field == "name":
            merge_results_with_unique_users(results, get_users_based_on_name(value))
        elif field == "age":
            merge_results_with_unique_users(results, get_users_based_on_age(value))
        else:
            merge_results_with_unique_users(results, get_users_based_on_occupation(value))

    return results

def merge_results_with_unique_users(results, matched_users):
    # Filter function that appends only non-existing users to results
    for user in matched_users:
        if not user_already_exists_in_results(user, results):
            results.append(user)

def get_user_with_id(id):
    
    for user in USERS:
        if user["id"] == id:
            return [user] # Returns as a single-element array to maintain consistency with other functions' parameters

    return None

def get_users_based_on_name(name):
    # Returns users matched that contain the letters of name within their own name
    users_with_similar_names = []

    for user in USERS:
        if user_has_letters_in_name(user, name):
            users_with_similar_names.append(user)

    return users_with_similar_names

def get_users_based_on_age(age):
    # Returns users matched with ages near to age argument
    users_around_age = []

    for user in USERS:
        if user_is_around_age(user, age):
            users_around_age.append(user)

    return users_around_age

def get_users_based_on_occupation(occupation):
    # Returns users matched that contain the letters of occupation within their own occupation
    users_with_similar_occupations = []

    for user in USERS:
        if user_has_letters_in_occupation(user, occupation):
            users_with_similar_occupations.append(user)

    return users_with_similar_occupations

def user_already_exists_in_results(user, results):

    if len(results) == 0: # If there are no users in results yet, then passed user is surely not in results yet
        return False

    for existing_user in results:
        if user["id"] == existing_user["id"]: # If the passed user has an identical ID to an existing user, then it is them, as IDs are unique
            return True

    return False

def user_has_letters_in_name(user, letters):
    return letters.lower() in user["name"].lower() # The comparison is a partial match (are these letters in the name?) and operands are set to lowercase for case-insensitivity

def user_is_around_age(user, age):
    age = int(age) # Converts to integer as an increment and decrement are present in the function
    return int(user["age"]) in [age - 1, age, age + 1]

def user_has_letters_in_occupation(user, letters):
    return letters.lower() in user["occupation"].lower() # Identical to function user_has_letters_in_name, but created regardless as an abstracted interface instead of hardcoding