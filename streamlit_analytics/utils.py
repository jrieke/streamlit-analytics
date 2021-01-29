import datetime


def format_timedelta(delta: datetime.timedelta) -> str:
    """Formats timedelta to x days, x h, x min, x s."""
    s = delta.total_seconds()
    days, remainder = divmod(s, 86400)
    hours, remainder = divmod(s, 3600)
    mins, secs = divmod(remainder, 60)

    days = int(days)
    hours = int(hours)
    mins = int(mins)
    secs = int(secs)

    # output = f"{secs} s"
    # if mins:
    #     output = f"{mins} min, " + output
    # if hours:
    #     output = f"{hours} h, " + output
    # if days:
    #     output = f"{days} days, " + output
    output = f"{days*24+hours:02}:{mins:02}:{secs:02}"
    return output
