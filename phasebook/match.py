import time
from flask import Blueprint

from .data.match_data import MATCHES


bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("<int:match_id>")
def match(match_id):
    if match_id < 0 or match_id >= len(MATCHES):
        return "Invalid match id", 404

    start = time.time()
    msg = "Match found" if (is_match(*MATCHES[match_id])) else "No match"
    end = time.time()

    return {"message": msg, "elapsedTime": end - start}, 200


def is_match(fave_numbers_1, fave_numbers_2):

    ### Original Solution:
    #
    #for number in fave_numbers_2:
    #    if number not in fave_numbers_1:
    #        return False
    #
    #return True
    #
    ### Nested loop speed is O(n^2)
    

    # Speed-optimized Solution:
    # A bit of a hack-y solution, but the criterion asked for optimization for speed, not readability

    # Convert both lists to sets as set operations can be used to easily find differences
    first_number_set = set(fave_numbers_1)
    second_number_set = set(fave_numbers_2)
    
    return len(second_number_set.difference(first_number_set)) == 0 # This answers the question "What is in fave_numbers_2 that does not appear in supposedly bigger fave_numbers_1?"
                                                                    # If one or more elements remain, then fave_numbers_2 has at least one number that does not appear in fave_numbers_1
    
    # Unsure of time complexity, but definitely closer to O(n) on average