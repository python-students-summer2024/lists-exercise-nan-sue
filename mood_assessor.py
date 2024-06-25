import datetime

def ask_current_mood():
    acceptable_mood = ['happy', 'relaxed', 'apathetic', 'sad', 'angry']
    response_in_int = {'happy': 2, 'relaxed': 1, 'apathetic': 0, 'sad': -1, 'angry': -2}
    ask_user = input("Please enter your current mood: ").strip().lower()
    while ask_user not in acceptable_mood:
        ask_user = input("Please enter your current mood: ").strip().lower()
    return response_in_int[ask_user]

def mood_storage(mood):
    get_date = datetime.date.today()
    date_formatted = str(get_date)

    with open('data/mood_diary.txt', 'a', encoding='utf-8') as file:
        file.write(f"{date_formatted},{mood}\n")


def entered_today():
    get_date = datetime.date.today()
    date_formatted = str(get_date)

    try:
        with open('data/mood_diary.txt', 'r', encoding='utf-8') as file:
            entries = file.readlines()
            if entries:
                last_entry = entries[-1].strip()
                last_entry_split = last_entry.split(',')
                if last_entry_split[0] == date_formatted:
                    return True
    except FileNotFoundError:
        return False
    return False

def mood_disorder_determination():
    try:
        with open('data/mood_diary.txt', 'r', encoding='utf-8') as file:
            entries = file.readlines()
    except FileNotFoundError:
        return None
    
    if len(entries) < 7:
        return None
    
    recent_entries = []
    for entry in entries[-7:]:
        recent_entries.append(int(entry.strip().split(',')[1]))
        
    average_mood = sum(recent_entries) / 7
    rounded_average_mood = round(average_mood)

    mood_in_string = {2: 'happy', 1: 'relaxed', 0: 'apathetic', -1: 'sad', -2: 'angry'}

    count_of_mood = {
        'happy': recent_entries.count(2),
        'relaxed': recent_entries.count(1),
        'apathetic': recent_entries.count(0),
        'sad': recent_entries.count(-1),
        'angry': recent_entries.count(-2)
    }
    
    if count_of_mood['happy'] >= 5:
        return "manic"
    elif count_of_mood['sad'] >= 4:
        return "depressive"
    elif count_of_mood['apathetic'] >= 6:
        return "schizoid"
    else:
        return mood_in_string[rounded_average_mood]

def assess_mood():
    if entered_today():
        print("Sorry, you have already entered your mood today.")
        return
    mood = ask_current_mood()
    mood_storage(mood)
    result = mood_disorder_determination()
    if result:
        print(f"Your diagnosis: {result}!")
