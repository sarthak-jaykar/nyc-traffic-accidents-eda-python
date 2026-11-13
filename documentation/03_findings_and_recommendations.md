# Findings and Recommendations

## How to read this
Each finding follows: **finding → evidence → business implication → recommendation → measure**. Findings describe the data. None establishes a cause.

## Metric definitions

| Metric | Definition |
|---|---|
| Collisions per day | Collisions in a month ÷ days in that month (August = 29) |
| Injury rate | Collisions with at least one person injured ÷ collisions |
| Share of casualties | A road user group's injured (or killed) count ÷ all injured (or killed) |
| Excess over average | A spike month's count minus the average of other months |

## Findings

**F1. Collisions fell sharply in spring 2020, but the share with injuries rose.**
Collisions per day were 461 in January and 472 in February, fell to 137 in April, and recovered to 254 to 302 from June to August. Over the same months, the injury rate rose from about 22% (January to March) to about 35% (June to August). The April-June average (197 per day) is 58% lower than the January-February average (466 per day) (Mann-Whitney test, p below 0.001).
*Implication:* fewer collisions did not mean fewer injuries per collision.
*Recommendation:* check speed and traffic-volume data for the same months before drawing conclusions. Do not treat 2020 as a baseline until a second year is available. *Owner:* data team with the policy analyst.
*Measure:* injury rate per collision, monthly, against a multi-year baseline.

**F2. Pedestrians account for a large share of deaths.**
Pedestrians are 14.9% of people injured but 38.9% of people killed (56 of 144). Motorists are 73.1% of injuries and 54.9% of deaths. Cyclists are 11.9% of injuries and 6.3% of deaths.
*Implication:* pedestrian injuries are a small share of total harm but a large share of fatal outcomes.
*Recommendation:* prioritise pedestrian safety review on the corridors and time bands in F4 and F5. *Owner:* pedestrian safety lead.
*Measure:* pedestrian deaths and serious injuries, monthly.

**F3. Driver inattention is the largest recorded factor, but a quarter of collisions have no factor.**
Among collisions with a recorded primary factor, "Driver Inattention/Distraction" accounts for 34.7%, with 19,123 collisions. "Unspecified" covers 26% of all collisions.
*Implication:* the largest known factor is behavioural, but factor-based targeting is weaker than it appears.
*Recommendation:* ask the data owner to improve factor recording. Use the inattention finding as a hypothesis for enforcement. *Owner:* road safety programme lead.
*Measure:* share of collisions with a recorded factor, monthly.

**F4. Late evening and evening collisions are more often injurious.**
The injury rate is 34.0% for 20:00 to 23:59 and 29.7% for 16:00 to 19:59, against 27.9% at night, 24.4% at midday and 23.1% in the morning peak. Midday has the most collisions (25,533), while the evening peak has 18,627.
*Implication:* volume and severity peak at different times of day.
*Recommendation:* test targeted enforcement in late-evening and evening periods on the highest-injury corridors. *Owner:* road safety programme lead.
*Measure:* injury rate by time band, monthly.

**F5. Expressways dominate the streets with the most collisions.**
Most of the 15 streets with the most collisions are expressways or parkways. Belt Parkway has 1,241 collisions and 689 injuries. Because street names are missing for 26% of collisions, these counts are a minimum.
*Implication:* engineering effort on arterial and expressway corridors can address many collisions.
*Recommendation:* review speed and merging design on the top three corridors, and fill the missing street names before finalising the ranking. *Owner:* traffic engineering lead.
*Measure:* collisions and injuries per corridor, quarterly.

**F6. Borough injury rates differ, but a third of collisions have no borough.**
Injury rates range from 24.5% (Manhattan) to 30.4% (Staten Island, the smallest group at 1,446 collisions). The "Not recorded" group is 34.4% of collisions, with a 29.6% injury rate.
*Implication:* borough comparisons are weaker than they look until the missing boroughs are resolved.
*Recommendation:* report borough findings with the unrecorded group shown. Ask the data owner to improve recording. *Owner:* road safety programme lead.
*Measure:* share of collisions with a recorded borough.

## Caveats
- One year of data with no baseline. Changes within 2020 are not evidence of their cause.
- The spring change coincides with a major change in travel patterns that this dataset does not describe.
- The Q6 test treats daily counts as comparable. Daily counts are not fully independent, so treat the p-value as indicative.
- Extreme counts are kept and listed; they are not removed.

## Interview talking points
- Why rates per collision and per day are used instead of raw counts.
- Why missing borough is shown as its own group rather than guessed.
- Why a single year cannot show a trend, and what second year of data would change.
