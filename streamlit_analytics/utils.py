import datetime


def format_seconds(s: int) -> str:
    """Formats seconds to 00:00:00 format."""
    # days, remainder = divmod(s, 86400)
    hours, remainder = divmod(s, 3600)
    mins, secs = divmod(remainder, 60)

    # days = int(days)
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
    output = f"{hours:02}:{mins:02}:{secs:02}"
    return output


def replace_empty(s):
    """Replace an empty string or None with a space."""
    if s == "" or s is None:
        return " "
    else:
        return s
