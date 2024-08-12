import datetime

# Доброе утро: От 6:00 до 12:00.
# Добрый день: От 12:00 до 18:00.
# Добрый вечер: От 18:00 до 22:00
# После 22:00 - Доброй ночи.

def greeting_by_time():
    current_date_time = datetime.datetime.now()
    current_time = current_date_time.strftime("%H:%M")
    if "06:00" <= str(current_time) < "12:00":
        return "Доброе утро"
    elif "12:00" <= str(current_time) < "18:00":
        return "Добрый день"
    elif "18:00" <= str(current_time) < "22:00":
        return "Добрый вечер"
    elif "22:00" <= str(current_time) < "24:00":
        return "Доброй ночи"
    elif "00:00" <= str(current_time) < "06:00":
        return "Доброй ночи"


di={}
tm = greeting_by_time()
di["greeting"] = tm
print(di)




