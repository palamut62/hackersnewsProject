from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal

def time_ago(date_time_obj):
    # Get the current time and make it offset-aware
    now = datetime.now(tzlocal())

    # Calculate the difference
    difference = relativedelta(now, date_time_obj)

    # Return the difference in a format like "x hours ago" or "x days ago"
    if difference.years > 0:
        return f"{difference.years} years ago"
    elif difference.months > 0:
        return f"{difference.months} months ago"
    elif difference.weeks > 0:
        return f"{difference.weeks} weeks ago"
    elif difference.days > 0:
        return f"{difference.days} days ago"
    elif difference.hours > 0:
        return f"{difference.hours} hours ago"
    elif difference.minutes > 0:
        return f"{difference.minutes} minutes ago"
    else:
        return "a few seconds ago"
