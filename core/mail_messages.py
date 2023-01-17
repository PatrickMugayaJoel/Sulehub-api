
def messages(template, **kargs):
    templates = {
        "USER_UPDATED":{
            "subject":"User information updated",
            "message":"""User information was successfully updated."""
        },
        "USER_CREATED":{
            "subject":"User account created",
            "message":"""Your user account was successfully created."""
        }
    }
    return templates.get(template)
