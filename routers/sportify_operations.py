from ..async_database import SessionLocal

db = SessionLocal()


def get_token_from_db(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    #database query
    c.execute("SELECT access_token, expires_at, refresh_token FROM tokens WHERE user_id=?", (user_id,))
    token_data = c.fetchone()
    conn.close()
    #check and return 
    if token_data:
        return {
            'access_token': token_data[0],
            'expires_at': token_data[1],
            'refresh_token': token_data[2]
        }
    else:
        return None




def save_token_to_db(user_id, access_token, expires_at, refresh_token):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    #database query 
    c.execute("INSERT OR REPLACE INTO tokens (user_id, access_token, expires_at, refresh_token) VALUES (?, ?, ?, ?)", (user_id, access_token, expires_at, refresh_token))
    conn.commit()
    conn.close()





def cache_handler(user_id, token_info = None):
    if token_info is None:
        pass

        token_data = get_token_from_db(user_id)
        if token_data and token_data['expires_at'] > time.time():
            return token_data['access_token']
        else:
        new_token_data = get_new_token(token_data["refresh_token"])
        save_token_to_db(user_id, new_token_data['access_token'], new_token_data['expires_at'], new_token_data['refresh_token'])
        return new_token_data['access_token']

    save_token_to_db(user_id, token_info["access_token"], token_info["refresh_token"], token_info["expires_at"])








def get_new_token(refresh_token):
    sp_oauth = SpotifyOAuth(client_id='your_client_id,
    client_secret='your_client_secret', redirect_uri='your_redirect_uri', scope='your_scope')
    token_info = sp_oauth.refresh_access_token(refresh_token)
    return {
        'access_token': token_info['access_token'],
        'expires_at': token_info['expires_at'],
        'refresh_token': token_info['refresh_token']
    }
