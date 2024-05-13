from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal

def time_ago(date_time_obj):
    # Şimdiki zamanı al ve onu "offset-aware" yap
    now = datetime.now(tzlocal())

    # Aradaki farkı hesapla
    difference = relativedelta(now, date_time_obj)

    # Farkı "x saat önce" veya "x gün önce" gibi bir formatta dön
    if difference.days > 0:
        return f"{difference.days} gün önce"
    elif difference.hours > 0:
        return f"{difference.hours} saat önce"
    elif difference.minutes > 0:
        return f"{difference.minutes} dakika önce"
    else:
        return "birkaç saniye önce"