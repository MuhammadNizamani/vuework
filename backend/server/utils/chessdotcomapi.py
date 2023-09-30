import urllib3
import json

# List of players
# players = ["BABU_69", "hamidullahnizamani", "Zararnizamani", "muhammadnizamani", "salmannizamani7",
#         "UmAr212212", "Alinizamani101", "inamullahniz6", "GUMNAM_69", "sarwan920"]
# players = ["UmAr212212", "Alinizamani101","BABU_69"]
# for player in players:
#     print(player)
# https://discord.gg/24BCstk4re
def get_data_from_chessdotcom(player:str):
    # Make an HTTP GET request to the Chess.com API
    url =  f"https://api.chess.com/pub/player/{player}"

    try:
        http = urllib3.PoolManager()
        response = http.request("GET", url)

        if response.status == 200:
            data = json.loads(response.data.decode("utf-8"))

            # Extract rating data
            # rapid_rating = data["chess_rapid"]["last"]["rating"]
            # # bullet_rating = data["chess_bullet"]["last"]["rating"]
            # blitz_rating = data["chess_blitz"]["last"]["rating"]

            # print(f"Rapid Rating for {player}: {rapid_rating}")
            # # print(f"Bullet Rating for {player}: {bullet_rating}")
            # print(f"Blitz Rating for {player}: {blitz_rating}")
            print(data)
            
            # else :
            #     print(data["username"])
            
            # if not data:
            #     print("The dictionary is empty.")
            # else:
            #     print("The dictionary is not empty.")
            #     print(data)
            # You can use these rating values to update your HTML elements as needed
            # print(len(data))
            return data
        else:
            print(f"Error fetching data. Status code: {response.status}")
            data = {'404':response.status }
            return data

    except Exception as error:
        print('Error fetching data:', error)
       
def get_rating_data_from_chessdotcom(player:str):
    url =  f"https://api.chess.com/pub/player/{player}/stats"
    

    try:
        http = urllib3.PoolManager()
        response = http.request("GET", url)

        if response.status == 200:
            data = json.loads(response.data.decode("utf-8"))

            # Extract rating data
            # rapid_rating = data["chess_rapid"]["last"]["rating"]
            # # bullet_rating = data["chess_bullet"]["last"]["rating"]
            # blitz_rating = data["chess_blitz"]["last"]["rating"]

            # print(f"Rapid Rating for {player}: {rapid_rating}")
            # # print(f"Bullet Rating for {player}: {bullet_rating}")
            # print(f"Blitz Rating for {player}: {blitz_rating}")
            # print(data)
            # print(data['chess_rapid']['last']['rating'])
            # print(data['chess_blitz']['last']['rating'])
            # print(data['chess_bullet']['last']['rating'])
            
            
            # else :
            #     print(data["username"])
            
            # if not data:
            #     print("The dictionary is empty.")
            # else:
            #     print("The dictionary is not empty.")
            #     print(data)
            # You can use these rating values to update your HTML elements as needed
            # print(len(data))
            return data
        else:
            print(f"Error fetching data. Status code: {response.status}")
            data = {'404':response.status }
            return data

    except Exception as error:
        print('Error fetching data:', error)
    
if __name__ == "__main__":
    # if not get_data_from_chessdotcom("BABU_69"):
    #     print("false")
    # else:
    #     print("True")
    get_rating_data_from_chessdotcom("prinkster")
    # import datetime

    # # Unix timestamp
    # timestamp = int(1694518988)

    # # Convert to a datetime object
    # dt_object = datetime.datetime.fromtimestamp(timestamp)

    # # Format the datetime as a string
    # formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    # print(formatted_date)
