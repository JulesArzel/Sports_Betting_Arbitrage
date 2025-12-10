import json
import glob
import pandas as pd
from pathlib import Path

def load_all_matches(folder="data"):
    rows = []
    files = glob.glob(f"{folder}/*.json")

    for f in files:
        with open(f, "r") as fp:
            match = json.load(fp)

        # Basic match info
        date = match["date"].replace(",", "").strip()
        home = match["homeTeam"]
        away = match["awayTeam"]
        match_id = f"{date}_{home}_{away}".replace(" ", "_")

        # Helper to flatten markets
        def add_market(market_name, market_data, mapping):
            for entry in market_data:
                bookmaker = entry[mapping["bookmaker"]]

                for outcome_key, new_outcome in mapping["outcomes"].items():
                    if outcome_key in entry:
                        rows.append({
                            "match_id": match_id,
                            "date": date,
                            "home": home,
                            "away": away,
                            "market": market_name,
                            "bookmaker": bookmaker,
                            "outcome": new_outcome,
                            "odds": float(entry[outcome_key])
                        })

        # Full-time ML
        add_market(
            "ML_FullTime",
            match["mlFullTime"],
            mapping={
                "bookmaker": "bookMakerName",
                "outcomes": {"hw": "home", "d": "draw", "aw": "away"}
            }
        )

        # First-half ML
        add_market(
            "ML_FirstHalf",
            match["mlFirstHalf"],
            mapping={
                "bookmaker": "bookMakerName",
                "outcomes": {"hw": "home", "d": "draw", "aw": "away"}
            }
        )

        # Second-half ML
        add_market(
            "ML_SecondHalf",
            match["mlSecondHalf"],
            mapping={
                "bookmaker": "bookMakerName",
                "outcomes": {"hw": "home", "d": "draw", "aw": "away"}
            }
        )

        # Over/Under 2.5
        add_market(
            "OU_2.5",
            match["underOver25"],
            mapping={
                "bookmaker": "bookmakerName",
                "outcomes": {"oddsOver": "over", "oddsUnder": "under"}
            }
        )

        # Over/Under 1.5
        add_market(
            "OU_1.5",
            match["underOver15"],
            mapping={
                "bookmaker": "bookmakerName",
                "outcomes": {"oddsOver": "over", "oddsUnder": "under"}
            }
        )

        # Over/Under 3.5
        add_market(
            "OU_3.5",
            match["underOver35"],
            mapping={
                "bookmaker": "bookmakerName",
                "outcomes": {"oddsOver": "over", "oddsUnder": "under"}
            }
        )

    return pd.DataFrame(rows)


