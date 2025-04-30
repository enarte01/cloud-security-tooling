from alert_sources.ECR.ecr_alert_handler.ecr_alerts_handler import ecr_alerts_handler
import json



def lambder_handler(event,context=None):
    """Lambda entry point"""

    ecr_alerts_handler(event=event)
