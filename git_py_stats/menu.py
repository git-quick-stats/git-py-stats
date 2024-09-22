"""
Provides the interactive menu for Git Py Stats.
"""

def interactive_menu() -> str:
    """
    Displays the interactive menu and gets the user's choice.

    Returns:
        str: The user's menu choice.
    """
    # ANSI escape codes for colors and formatting
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m' # Not currently used
    YELLOW = '\033[33m'
    WHITE = '\033[37m'
    CYAN = '\033[36m'

    # This mostly follows the original formatting nearly 1:1
    # Note that there is no legacy menu option yet
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
    print(f"\n{HELP_TXT}Please enter a menu option or {EXIT_TXT}press Enter to exit.{NORMAL}")
    
    choice = input(f"{TEXT}> {NORMAL}")
    
    return choice.strip()
