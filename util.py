import pandas as pd

def get_all_teams(df: pd.DataFrame) -> set[str]:
    """
    Return all unique team names from the given data of a single season
    """

    return set(df['Home team'][:8]) | set(df['Away team'][:8]) # Only need to look at the first round (8 games) because every team will occur exactly once


def figure_out_team(short_name: str, all_names: set[str]) -> str:
    """
    team_name = the best match from all_teams that contains "team";
    or, throw an "invalid team" error if no good match
    or, throw "can't figure out which team u mean" if too many matches
    """
    matches = []
    snlower = short_name.lower()
    for n in all_names:
        if snlower in n.lower():
            matches.append(n)

    if len(matches) == 0:
        raise ValueError(f'Invalid team: Valid teams are {all_names}')

    if len(matches) > 1:
        raise ValueError(f"Can't figure out which team you are referring to: Valid teams are {all_names}; You matched with {matches}")

    return matches[0]