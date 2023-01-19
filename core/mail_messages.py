
def messages(template, kargs):
    templates = {
        "USER_UPDATED":{
            "subject":"User information updated",
            "message":"""User information was successfully updated."""
        },
        "USER_CREATED":{
            "subject":"User account created",
            "message":"""Your user account was successfully created."""
        },
        "SCHOOL_PROFILE_UPDATED":{
            "subject":"School Profile Updated",
            "message":"""Your user account has successfully been updated."""
        },
        "SCHOOL_PROFILE_CREATED":{
            "subject":"School Profile Created",
            "message":"""Your user account has successfully been created."""
        }
    }
    return templates.get(template)
