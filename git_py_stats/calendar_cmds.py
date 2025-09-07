"""
Functions related to the 'Calendar' section.
"""

from typing import Optional, Dict, Union
from datetime import datetime, timedelta
from collections import defaultdict

from git_py_stats.git_operations import run_git_command


def commits_calendar_by_author(config: Dict[str, Union[str, int]], author: Optional[str]) -> None:
    """
    Displays a calendar of commits by author

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.
        author: Optional[str]: The author's name to filter commits by.

    Returns:
        None
    """

    # Initialize variables similar to the Bash version
    author_option = f"--author={author}" if author else ""

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    since = config.get("since", "")
    until = config.get("until", "")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "")

    # Original git command:
    # git -c log.showSignature=false log --use-mailmap $_merges \
    #    --date=iso --author="$author" "$_since" "$_until" $_log_options \
    #    --pretty='%ad' $_pathspec
    cmd = [
        "git",
        "-c",
        "log.showSignature=false",
        "log",
        "--use-mailmap",
        "--date=iso",
        f"--author={author}",
        "--pretty=%ad",
    ]

    if author_option:
        cmd.append(author_option)

    cmd.extend([since, until, log_options, merges, pathspec])

    # Remove any empty space from the cmd
    cmd = [arg for arg in cmd if arg]

    print(f"Commit Activity Calendar for '{author}'")

    # Get commit dates
    output = run_git_command(cmd)
    if not output:
        print("No commits found.")
        return

    print("\n      Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec")

    count = defaultdict(lambda: defaultdict(int))
    for line in output.strip().split("\n"):
        try:
            date_str = line.strip().split(" ")[0]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = date_obj.isoweekday()  # 1=Mon, ..., 7=Sun
            month = date_obj.month
            count[weekday][month] += 1
        except ValueError:
            continue

    # Print the calendar
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for d in range(1, 8):
        row = f"{weekdays[d-1]:<5} "
        for m in range(1, 13):
            c = count[d][m]
            if c == 0:
                out = "..."
            elif c <= 9:
                out = "░░░"
            elif c <= 19:
                out = "▒▒▒"
            else:
                out = "▓▓▓"
            row += out + (" " if m < 12 else "")
        print(row)

    print("\nLegend: ... = 0   ░░░ = 1–9   ▒▒▒ = 10–19   ▓▓▓ = 20+ commits")


def commits_heatmap(config: Dict[str, Union[str, int]]) -> None:
    """
    Shows a heatmap of commits per hour of each day for the last N days.

    Uses 256-color ANSI sequences to emulate the original tput color palette:
      226 (bright yellow)
      220 (gold)
      214 (orange)
      208 (dark orange),
      202 (red-orange),
      160 (red),
      88 (deep red),
      52 (darkest red)

    Args:
        config: Dict[str, Union[str, int]]: Config dictionary holding env vars.

    Returns:
        None
    """

    # ANSI color code helpers
    RESET = "\033[0m"

    def ansi256(n: int) -> str:
        return f"\033[38;5;{n}m"

    COLOR_BRIGHT_YELLOW = ansi256(226)
    COLOR_GOLD = ansi256(220)
    COLOR_ORANGE = ansi256(214)
    COLOR_DARK_ORANGE = ansi256(208)
    COLOR_RED_ORANGE = ansi256(202)
    COLOR_RED = ansi256(160)
    COLOR_DARK_RED = ansi256(88)
    COLOR_DEEPEST_RED = ansi256(52)
    COLOR_GRAY = ansi256(240)  # Gives the dark color for no commits

    def color_for_count(n: int) -> str:
        # Map counts to colors
        if n == 1:
            return COLOR_BRIGHT_YELLOW
        elif n == 2:
            return COLOR_GOLD
        elif n == 3:
            return COLOR_ORANGE
        elif n == 4:
            return COLOR_DARK_ORANGE
        elif n == 5:
            return COLOR_RED_ORANGE
        elif n == 6:
            return COLOR_RED
        elif 7 <= n <= 8:
            return COLOR_DARK_RED
        elif 9 <= n <= 10:
            return COLOR_DEEPEST_RED
        else:
            return COLOR_DEEPEST_RED  # 11+

    # Grab the config options from our config.py.
    # config.py should give fallbacks for these, but for sanity,
    # lets also provide some defaults just in case.
    merges = config.get("merges", "--no-merges")
    log_options = config.get("log_options", "")
    pathspec = config.get("pathspec", "--")
    days = int(config.get("days", 30))

    print(f"Commit Heatmap for the last {days} days")

    # Header bar thing
    header = "Day | Date/Hours |"
    for h in range(24):
        header += f" {h:2d}"
    print(header)
    print(
        "------------------------------------------------------------------------------------------"
    )

    # Build each day row from oldest to newest, marking weekends,
    # and printing the row header in "DDD | YYYY-MM-DD |" format
    today = datetime.now().date()
    for delta in range(days - 1, -1, -1):
        day = today - timedelta(days=delta)
        is_weekend = day.isoweekday() > 5
        day_prefix_color = COLOR_GRAY if is_weekend else RESET
        dayname = day.strftime("%a")
        print(f"{day_prefix_color}{dayname} | {day.isoformat()} |", end="")

        # Count commits per hour for this day
        since = f"--since={day.isoformat()} 00:00"
        until = f"--until={day.isoformat()} 23:59"

        cmd = [
            "git",
            "-c",
            "log.showSignature=false",
            "log",
            "--use-mailmap",
            merges,
            since,
            until,
            "--pretty=%ci",
            log_options,
            pathspec,
        ]

        # Remove any empty space from the cmd
        cmd = [arg for arg in cmd if arg]

        output = run_git_command(cmd) or ""

        # Create 24 cell per-hour commit histrogram for the day,
        # grabbing only what is parseable.
        counts = [0] * 24
        if output:
            for line in output.splitlines():
                parts = line.strip().split()
                if len(parts) >= 2:
                    time_part = parts[1]
                    try:
                        hour = int(time_part.split(":")[0])
                        if 0 <= hour <= 23:
                            counts[hour] += 1
                    except ValueError:
                        continue

        # Render the cells
        for hour in range(24):
            n = counts[hour]
            if n == 0:
                # gray dot for zero commits
                print(f" {COLOR_GRAY}.{RESET} ", end="")
            else:
                c = color_for_count(n)
                print(f"{c} █ {RESET}", end="")
        # End the row/reset
        print(RESET)

    # Match original version in the bash impl
    print(
        "------------------------------------------------------------------------------------------"
    )
    # Legend
    print("\nLegend:")
    print(f" {COLOR_BRIGHT_YELLOW}█{RESET} 1 commit")
    print(f" {COLOR_GOLD}█{RESET} 2 commits")
    print(f" {COLOR_ORANGE}█{RESET} 3 commits")
    print(f" {COLOR_DARK_ORANGE}█{RESET} 4 commits")
    print(f" {COLOR_RED_ORANGE}█{RESET} 5 commits")
    print(f" {COLOR_RED}█{RESET} 6 commits")
    print(f" {COLOR_DARK_RED}█{RESET} 7–8 commits")
    print(f" {COLOR_DEEPEST_RED}█{RESET} 9–10 commits")
    print(f" {COLOR_DEEPEST_RED}█{RESET} 11+ commits")
    print(f" {COLOR_GRAY}.{RESET} = no commits\n")
