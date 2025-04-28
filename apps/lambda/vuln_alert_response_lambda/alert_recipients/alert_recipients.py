import pymsteams as teams
from slack_sdk.webhook import WebhookClient
from jira import JIRA
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from time import  sleep
import json
from  common.helpers import create_email_tmplt, get_logger
import os
#####
#TODO
#Each service should be able to send to  multiple groups of contacts from cloud env
#####
logger = get_logger('ALERT_RECIPIENTS')
#ms teams
def send_teams_message(whook_url:str, msg: dict) -> None:
    """
      send message to ms teams
    """
    #create 2 card sections, one for summary of output, and 1 for details output
    message = teams.connectorcard(whook_url)
    summary_section = teams.cardsection()
    detail_section = teams.cardsection()
    summary_section.title(msg['summary-title'])
    summary_section.text(msg['summary-body'])
    detail_section.title(msg['detail-title'])
    detail_section.text(msg['detail-body'])
    message.title(msg['title'])
    #message.text(message['body'])
    message.addSection(summary_section)
    message.addSection(detail_section)
    message.send()

#create jira ticket
# Authentication
jira = JIRA(
    basic_auth=("your_email@domain.com", "your_api_token"),
    server="https://your-domain.atlassian.net"
)
def create_jira_ticket(msg,project_key, issue_type="Problem"):
    issue_dict = {
        'project': {'key': project_key},
        'summary': f'{msg["summary-title"]}\n{msg["summary-body"]}\n\n{msg["detail-title"]}\n{msg["detail-body"]}',
        'description': msg["summary-title"],
        'issuetype': {'name': issue_type},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    return new_issue
#TODO
#slack oauth flow
#generates incoming webhook url 
def get_slack_authz():
    pass
#slack message
def send_slack_message(webhook_url: str,msg: dict):
      
  url = webhook_url
  webhook = WebhookClient(url)
  #TODO
  #what is returned in the response?
  response = webhook.send(
      text=f"{msg['summary-title']}\n {msg['summary-body']}\n\n {msg['detail-title']}\n {msg['detail-body']}",
      blocks=[
              {
              "type": "header",
              "text": {
                "type": "plain_text",
                "text": msg['summary-title']
              }
            },
          {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": msg['summary-body']                           
                  }
          },
                        {
              "type": "header",
              "text": {
                "type": "plain_text",
                "text": msg['summary-title']
              }
            },
                    {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": msg['detail-body']                           
                  }
            }
        ]
    )

#email
#html and attachment capability
def send_email(msg: dict,email_details: dict):
  '''Send email to receivers'''

  try:
    with open(file=email_details['html_part'], mode='r') as html_part,open(file=email_details['txt_part'], mode='r') as txt_part:
      html_part = html_part.read()
      txt_part = txt_part.read()
  except Exception as ex:
    logger.info(f'The email template files: {email_details["html_part"]} and {email_details["txt_part"]} could not be loaded: {ex}')
    exit()
  message = MIMEMultipart("alternative")
  message["Subject"] = email_details['email_subject']
  message["From"] = email_details['sender_email']
  #message["To"] = email_details['receiver_email']
  if email_details['attachment_file']:
    #TODO
    #attach any valid file
    try:
      with open(email_details['attachment_file'], "rb") as attachment:
          # Add file as application/octet-stream
          # Email client can usually download this automatically as attachment
          part = MIMEBase("application", "octet-stream")
          part.set_payload(attachment.read())
      # Encode file in ASCII characters to send by email    
          encoders.encode_base64(part)
          # Add header as key/value pair to attachment part
          part.add_header(
              "Content-Disposition",
              f"attachment; filename= {email_details['attachment_file']}",
          )
          # Add attachment to message and convert message to string
          message.attach(part)
    except Exception as ex:
      logger.exception(f"Unable to load email attachment: {email_details['attachment_file']}, {ex}")
    
  context = ssl.create_default_context()
  email_paswd = os.getenv("EMAIL_PASWORD",None)
  if email_paswd == None:
    logger.error(f'email_paswd is not set')
    exit()
  try:
      with smtplib.SMTP_SSL("localhost", 1025, context=context) as server:
          server.login(email_details['sender_email'], email_paswd)  
          for item in email_details["receiver_email"]:
            msg['recipient_name'] = item['name']
            msg['email_subject'] = item['email_subject']
            html_part = create_email_tmplt(record=msg,text=html_part)
            txt_part = create_email_tmplt(record=msg, text=txt_part)
            message["To"] = item['email']
            txt_part = MIMEText(txt_part, "plain")
            html_part = MIMEText(html_part, "html")
            message.attach(txt_part)
            message.attach(html_part)
            text = message.as_string()
            server.sendmail(
                email_details['sender_email'], 
                item['email'], 
                text
              )
            sleep(2)
  except Exception as ex:
     logger.exception(f"Unable to send email to {email_details['receiver_email']}, {ex}")

#TODO
#snow ticket