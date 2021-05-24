from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher


'''
savant_queries.py

INPUT (from website):
- Pitcher First/Last Name
- Start/End Date for training data 'YYYY-MM-DD'

OUTPUT:
- Selected Data (goes to preprocessing.py)

OR

- Error Message if data does not exist (goes back to website)
'''


def query(first, last, start_date, end_date):
    pitcher_id = -1

    try:
        pitcher = playerid_lookup(last, first)
        pitcher_id = pitcher.iloc[0, 2]
        print("Pitcher ID: ", pitcher.iloc[0, 2])
    except IndexError:
        print("Pitcher Does Not Exist!")  # send this to website

    # grab stats based on ID
    pitcher_stats = statcast_pitcher(start_date, end_date, pitcher_id)

    important_cols = ["game_date", "at_bat_number", "pitch_type", "stand", "p_throws", "balls", "strikes",
                      "on_1b", "on_2b", "on_3b", "outs_when_up"]

    return pitcher_stats[important_cols]  # pass to 'preprocess.py'


