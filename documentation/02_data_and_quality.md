# Data and Quality

## Source
| Field | Value |
|---|---|
| Dataset | NYC Accidents 2020 (motor vehicle collisions) |
| Publisher | NYC Open Data (City of New York) |
| Dataset context | Secondary dataset obtained from publicly available online educational material; used for educational and portfolio analysis. |
| Period | 1 January to 29 August 2020 |
| Grain | one row per collision (COLLISION_ID is unique) |

## Key fields

| Field | Meaning | Note |
|---|---|---|
| CRASH DATE and CRASH TIME | When the collision happened | Parsed to a date and hour |
| BOROUGH | Borough | Blank for 25,741 (34.4%); kept as "Not recorded" |
| LATITUDE and LONGITUDE | Location | Blank for 5,946; zero for 63 (set to missing) |
| ON STREET NAME | Street | Blank for 19,437 (26%) |
| NUMBER OF PERSONS INJURED and KILLED | Casualties | Totals; consistent with the per-user-type counts |
| CONTRIBUTING FACTOR VEHICLE 1 | Primary recorded factor | "Unspecified" for 19,471 (26%); kept as its own category |

## Quality decisions

| # | Issue | Decision |
|---|---|---|
| 1 | Borough not recorded (34.4%) | Kept as a separate group; not guessed from ZIP code or coordinates |
| 2 | Coordinates missing or zero (6,009 in total) | Set to missing; excluded from any mapping |
| 3 | Factor "Unspecified" (26%) | Reported as a category; shares shown with and without it |
| 4 | Street name missing (26%) | Excluded from the street ranking; the ranking is a minimum |
| 5 | Extreme casualty counts (up to 15 injured in one collision) | Kept and listed in `results/outliers_top_injury_records.csv`; not removed |
| 6 | August is partial (to 29 August) | Monthly comparisons use collisions per day |
| 7 | Casualty totals vs per-user-type counts | Checked: 0 inconsistencies |
| 8 | Duplicate COLLISION_ID or full duplicate rows | Checked: 0 |

Cleaning and profile checks are printed to the console by `script/01_ingest.py` and `script/02_clean.py`.

## Reconciliation

| Total | Expected | Result |
|---|---|---|
| Collisions | 74,881 | 74,881 |
| Monthly counts sum to all collisions | 74,881 | 74,881 |
| Borough counts sum to all collisions | 74,881 | 74,881 |
| Persons killed | 144 | 144 |
| Persons injured | 27,448 | 27,448 |
