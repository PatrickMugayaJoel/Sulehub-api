
def messages(template, kargs):
    templates = {
        "STUDY_GROUP_REGISTRATION":{
            "subject":"Shulehub:- Study Groups",
            "message":f"""You have been added to the Study group: {kargs.get("STUDY_GROUP_NAME")}."""
        },
        "FEEDBACK_CREATED":{
            "subject":"Shulehub:- Resource Comments",
            "message":f"""{kargs.get("FEEDBACK_CATEGORY")} comment has been created for the Resource: {kargs.get("RESOURCE_NAME")}."""
        },
        "EVENT_CREATED":{
            "subject":"Shulehub:- Event Created",
            "message":f"""An event ({kargs.get("EVENT_NAME")}) has been created for the school: {kargs.get("SCHOOL_NAME")}."""
        }
    }
    return templates.get(template)
