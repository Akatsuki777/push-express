# Service that handles all the aspects of subscription management 
# and notification delivery

import json
from datetime import datetime, timezone
from models.subscriptions import PushSubscription
from pywebpush import webpush, WebPushException
from database import SessionLocal
from helpers.utils import grab_env_var

# Grab all the required variables.

VAPID_PRIVATE_KEY = grab_env_var("PRIVATE_KEY")
VAPID_PUBLIC_KEY = grab_env_var("PUBLIC_KEY")
VAPID_EMAIL = grab_env_var("EMAIL")

# Adds a new subscription into the database

def save_subscription(db,subscription,logger=None):

    if logger:
        logger.info(f"New subscription with endpoint: {subscription["endpoint"]}")

    endpoint= subscription['endpoint']
    keys= subscription['keys']

    existing = (
        db.query(PushSubscription).filter(PushSubscription.endpoint==endpoint).first()
    )

    if existing:
        return existing

    sub = PushSubscription(
        endpoint=endpoint,
        public_browser_key=keys['p256dh'],
        auth=keys['auth'],
        created_at=datetime.now(timezone.utc)
    )

    db.add(sub)
    db.commit()
    db.refresh(sub)

    return sub

# This is the function that sends out a notification to all
# subscribers in the database. isdraw is the variable that contains 
# the details of the draw.

def notify(isdraw,logger):

    db = SessionLocal()

    try:
        subscriptions = db.query(PushSubscription).all()

        payload = {
            "title": f"New Express Entry Draw",
            "body": f"{isdraw['program']} - {isdraw['score']} - {isdraw['date']}",
            "url": "/"
        }

        for sub in subscriptions:
            subscription_info = {
                "endpoint": sub.endpoint,
                "keys": {
                    "p256h": sub.public_browser_key,
                    "auth": sub.auth
                },
            }

            try:
                webpush(
                    subscription_info,
                    json.dumps(payload),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims={
                        "sub": VAPID_EMAIL
                    },
                )

                if logger:
                    logger.info(f"The notification has been successfully sent out.")

            except WebPushException as ex:

                if logger:
                    logger.info(f"Encountered error when trying to push the notification: {ex}")

                #Handle expired subscription
                db.delete(sub)
                db.commit()
    finally:
        db.close()