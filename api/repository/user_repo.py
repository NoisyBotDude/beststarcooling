from api.drivers.user import user_drivers

async def update_refresh_token(user_id):
    response = await user_drivers.User().set_refresh_token(user_id)

    if response:
        return response
    
    return False