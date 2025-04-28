import logging
from common.aws_resources import SNSClass
from jinja2 import Template
from typing import Any

def get_logger(logger_name) -> logging.Logger:
    '''
        Create logger
    '''
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-3s %(asctime)s %(lineno)s %(name)-12s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

logger = get_logger("HELPER")
#create notification method
def send_alert_notification(finding_data: dict,recipient_config: dict):
    """
        Send message to SNS Topic recepients
    """
    from alert_recipients.alert_recipients import send_email
    for config in recipient_config:
        match config["service"]:
            case "email":
                try:
                    logger.info("Sending email")
                    send_email(
                        msg=finding_data,
                        email_details= config["config"]["email_details"]
                    )
                except Exception as ex:
                    logger.exception(f"Unable to send email: {ex}")
    #TODO
    # return the result of sending notifications                
    #return 'message'

#TODO
class AlertResponse(object):
    def __init__(self,aws_class):
        pass
    def respond_to_alerts(self,message,event, aws_class,**kwargs) -> str:
        
        return message


def create_email_tmplt(record,text) -> Any:
    try:
        template = Template(text)
        return template.render(record=record)
    except Exception as ex:
        print(f'The template could not be rendered: {ex}')
        exit()

