import os


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
        },
        "INVITE_A_USER":{
            "subject":f"Shulehub:- Initation to join {kargs.get('SCHOOL_NAME')}",
            "message":f"""Dear sir/madam,<br/><br/> You are invited to join {kargs.get("SCHOOL_NAME")} as a {kargs.get('USER_TYPE')}.
                <br/><br/>To proceed, click the link below and Signup/Login to Shulehub and accept the invitation.<br/><br/>
                {os.environ.get('FRONTEND_DOMAIN')}{os.environ.get('FRONTEND_INVITE_URL')}/{kargs.get("INVITE_ID")} <br/><br/>
                --- ShuleHub Mngt ---"""
        },
        "PASSWORD_RESET":{
            "subject":"Shulehub:- Password Reset",
            "message":f"""Dear {kargs.get('FIRST_NAME')},<br/><br/> Click the link below to reset your password.<br/>
            <a href="{os.environ.get('FRONTEND_DOMAIN')}/{os.environ.get('FRONTEND_PASSWORD_RESET_URL')}/{kargs.get("TOKEN")}">
            {os.environ.get('FRONTEND_DOMAIN')}{os.environ.get('FRONTEND_PASSWORD_RESET_URL')}/{kargs.get("TOKEN")}
            </a><br/><br/> --- ShuleHub Mngt ---"""
        },
    }
    return templates.get(template)
