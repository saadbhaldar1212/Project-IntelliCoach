def individual_serializer_for_user(users) -> dict:
    """
    This function takes a dictionary representing a user and returns a serialized version with certain
    fields masked for privacy.
    """
    return {
        "user_id": str(users["_id"]),
        "user_name": users["user_name"],
    }


def list_users(users) -> list:
    """
    The function `list_users` takes a list of users and returns a list of serialized user objects using
    an individual serializer function.
    """
    return [individual_serializer_for_user(user) for user in users]
