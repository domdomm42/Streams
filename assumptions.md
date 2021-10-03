1. Messages function will not require implementation of timestamps and u_id (who sent it) as there is no message create/send/delete function in this implementation. therefore simpled message and message_id would suffice for testing. 
2. Newly registered and logged in users will no be in any channels irrespective of auth/login_id as they have not been invited or joined to any public/private channel (i.e. found in data store but not in channel members). 
3. Channels_list_v1 returns the list of channels that the autherised user is apart of irrespective of private or public status. Likewise channel_details_v1 will return info on the channel irrespective of private and public status if the channel is valid and the user if a member (not specified entirely in interface spec). 
4. Channel_join_v1 does not require the user to be invited to public channels and can join freely. 
5. Channel_id and user_id always positive and can not bigger than 2^32
