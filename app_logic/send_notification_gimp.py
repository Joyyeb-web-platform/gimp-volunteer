from notificationapi_python_server_sdk import (notificationapi)
import os


async def send_admin_notification(notification_client, notification_secret, volunteer_data_link, volunteer_resume_link):
    notificationapi.init(notification_client, notification_secret)

    await notificationapi.send({
        "notificationId": "admin_volunteer_gimp",
        "user": {
            "id": "platform@joyyeb.com",
            "email": "joyyebonline@gmail.com",
            "number": "+4456530395"
        },
        "mergeTags": {
            "user_name": "testUser_name",
            "alerts": [
                {
                    "title": "testTitle"
                }
            ],
            "accountId": "testAccountId",
            "volunteer_data_link": volunteer_data_link,
            "volunteer_resume_link": volunteer_resume_link
        }
    })


async def send_client_notification(notification_client, notification_secret, volunteer_name, volunteer_email):
    notificationapi.init(notification_client, notification_secret)

    await notificationapi.send({
        "notificationId": "voluneteer_invite_gimp",
        "user": {
            "id": "platform@joyyeb.com",
            "email": f"{volunteer_email}",
            "number": "+4456530395"
        },
        "mergeTags": {
            "user_name": "testUser_name",
            "alerts": [
                {
                    "title": "testTitle"
                }
            ],
            "accountId": "testAccountId",
            "volunteer_name": volunteer_name,
        }
    })