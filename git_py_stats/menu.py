"""
Provides the interactive menu for Git Py Stats.
"""

from typing import Dict, Union


# TODO: We can refactor this with a few loops to make it more
#       efficient and less burdened by user-error during coding
def interactive_menu(config: Dict[str, Union[str, int]]) -> str:
    """
    Displays the interactive menu and gets the user's choice.

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
    Returns:
        str: The user's menu choice.
    """
    # ANSI escape codes for colors and formatting
    # FIXME: We now have colors in two places - one in the calendar area
    # and one here. Refactor this to have a global color scheme for the
    # whole program that it can leverage instead of having multiple colors
    # in different places.
    NORMAL = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    WHITE = "\033[37m"
    CYAN = "\033[36m"

    # Handle default, legacy, and colorless menu
    theme = config.get("menu_theme", "")

    # Grab the days set by the user for _GIT_DAYS
    # NOTE: We should already have a guard here to default this to 30
    # in the config.py file. Possible redundancy here.
    days = config.get("days", 30)

    if theme == "legacy":
        TITLES = f"{BOLD}{RED}"
        TEXT = f"{NORMAL}{CYAN}"
        NUMS = f"{BOLD}{YELLOW}"
        HELP_TXT = f"{NORMAL}{YELLOW}"
        EXIT_TXT = f"{BOLD}{RED}"
    elif theme == "none":
        TITLES = BOLD
        TEXT = ""
        NUMS = BOLD
        HELP_TXT = ""
        EXIT_TXT = BOLD
        NORMAL = ""
    else:
        TITLES = f"{BOLD}{CYAN}"
        TEXT = f"{NORMAL}{WHITE}"
        NUMS = f"{NORMAL}{BOLD}{WHITE}"
        HELP_TXT = f"{NORMAL}{CYAN}"
        EXIT_TXT = f"{BOLD}{CYAN}"

    print(f"\n{TITLES} Generate:{NORMAL}")
    print(f"{NUMS}    1){TEXT} Contribution stats (by author)")
    print(f"{NUMS}    2){TEXT} Contribution stats (by author) on a specific branch")
    print(f"{NUMS}    3){TEXT} Git changelogs (last 10 days)")
    print(f"{NUMS}    4){TEXT} Git changelogs by author")
    print(f"{NUMS}    5){TEXT} My daily status")
    print(f"{NUMS}    6){TEXT} Output daily stats by branch in CSV format")
    print(f"{NUMS}    7){TEXT} Save git log output in JSON format")
    print(f"\n{TITLES} List:{NORMAL}")
    print(f"{NUMS}    8){TEXT} Branch tree view (last 10)")
    print(f"{NUMS}    9){TEXT} All branches (sorted by most recent commit)")
    print(f"{NUMS}   10){TEXT} All contributors (sorted by name)")
    print(f"{NUMS}   11){TEXT} New contributors (sorted by email)")
    print(f"{NUMS}   12){TEXT} Git commits per author")
    print(f"{NUMS}   13){TEXT} Git commits per date")
    print(f"{NUMS}   14){TEXT} Git commits per month")
    print(f"{NUMS}   15){TEXT} Git commits per year")
    print(f"{NUMS}   16){TEXT} Git commits per weekday")
    print(f"{NUMS}   17){TEXT} Git commits per weekday by author")
    print(f"{NUMS}   18){TEXT} Git commits per hour")
    print(f"{NUMS}   19){TEXT} Git commits per hour by author")
    print(f"{NUMS}   20){TEXT} Git commits per timezone")
    print(f"{NUMS}   21){TEXT} Git commits per timezone by author")
    print(f"\n{TITLES} Suggest:{NORMAL}")
    print(f"{NUMS}   22){TEXT} Code reviewers (based on git history)")
    print(f"\n{TITLES} Calendar:{NORMAL}")
    print(f"{NUMS}   23){TEXT} Activity calendar by author")
    print(f"{NUMS}   24){TEXT} Activity heatmap for the last {days} days")
    print(f"\n{HELP_TXT}Please enter a menu option or {EXIT_TXT}press Enter to exit.{NORMAL}")

    choice = input(f"{TEXT}> {NORMAL}")

    return choice.strip()
