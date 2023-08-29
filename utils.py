from datetime import datetime


def calculate_validity():
    today = datetime.now()

    if today.month >= 9:  # If current month is September or later
        start_year = today.year
    else:
        start_year = today.year - 1

    end_year = start_year + 1
    return f"{start_year}-{end_year}"

def calculate_all_validity_year():
    this_year = calculate_validity()
    year1 = int(this_year.split("-")[0])

    all_validity = []

    for i in range(-5,6):
        all_validity.append(str(year1+i)+"-"+str(year1+i+1))

    return all_validity