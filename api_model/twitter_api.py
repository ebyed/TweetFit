# twitter_api.py
import tweepy
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN

# Authenticate Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# # Fetch Direct Messages (DMs)
# def fetch_dms():
#     dms = api.get_direct_messages()
#     messages = []
#     for message in dms:
#         user_id = message.message_create["sender_id"]
#         text = message.message_create["message_data"]["text"]
#         username = api.get_user(user_id=user_id).screen_name
#         messages.append((user_id, username, text))
#     return messages

# # Send DM
# def send_dm(user_id, message):
#     api.send_direct_message(recipient_id=user_id, text=message)

#select the goup id of the DM group 
#uncomment and run this first to fetch the correct group ID
dms = api.get_direct_messages()
for message in dms:
    print(f"Sender: {message.message_create['sender_id']}")
    print(f"Message: {message.message_create['message_data']['text']}")
    print(f"Group ID: {message.id}")
    print("-" * 40)

    #Find the group conversation from the output and note down its ID.

