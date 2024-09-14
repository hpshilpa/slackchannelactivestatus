import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize Slack client with your bot token
slack_token = "xoxb-"
client = WebClient(token=slack_token)

def get_channel_members_info(channel_id):
    try:
        # Step 1: Get the list of members in the channel
        response = client.conversations_members(channel="C01F228D8BH")
        members = response['members']

        # Step 2: Get detailed information about each member
        members_info = []
        for member in members:
            user_info = client.users_info(user=member)
            is_app = user_info['user']['is_bot']
            user_profile = user_info['user']['profile']
            #print(user_profile)
            user_presence = client.users_getPresence(user=member)
            #print('user_presence   ' + str(user_presence))
            
            member_info = {
                "username": user_profile.get("real_name", "N/A"),
                "email": user_profile.get("email", "N/A"),
                "is_app" : is_app,
                "status": user_presence['presence']              
            }
            members_info.append(member_info)

        return members_info

    except SlackApiError as e:
        print(f"Error: {e.response['error']}")
        return []

# Example usage: Replace 'C1234567890' with your channel ID


def list_members_info(channel_id):
    channel_id = "C01F228D8BH"
    members_info = get_channel_members_info(channel_id)
    active_list=[]
    inactive_list=[]
    channel_info={}
    for member in members_info:
        #print(member)
        '''
        if not member['is_app']:
        print(f"Username: {member['username']}, Email: {member['email']}, Status: {member['status']}")
    '''          
        if not member['is_app']:
            if member['status'] =="active":
                active_list.append(member['username'] +'('+ member['email'] +')')
            else:
                inactive_list.append(member['username'] +'('+ member['email'] +')')
            #print(active_list)
            #print(inactive_list)
        channel_info["active-users"] = active_list
        channel_info["inactive-users"] = inactive_list
    return f"Users that are active: {channel_info['active-users']}\nUsers that are inactive: {channel_info['inactive-users']}"
