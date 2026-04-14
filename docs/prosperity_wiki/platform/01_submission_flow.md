# Submission Flow

Source basis:

- `docs/prosperity_wiki_raw/05_game_mechanics_overview.md`
- `docs/prosperity_wiki_raw/07_faq.md`

## Rounds

- Prosperity has 16 days of simulation divided into 5 rounds.
- Rounds 1 and 2 last 72 hours.
- Rounds 3, 4, and 5 each last 48 hours.
- At the end of every round, before the timer runs out, teams submit algorithmic and manual trades to be processed.
- When a new round starts, results of the previous round are disclosed and the leaderboard is updated.
- Previous rounds remain viewable in the dashboard for reviewing information and results.
- Once a round is closed, the submitted trader for that round can no longer be changed.
- Round 5 final results are processed and the winner is announced within 2 weeks.

See [../reference/round_schedule.md](../reference/round_schedule.md) for dated schedule entries.

## Algorithmic submissions

- Every round contains an algorithmic trading challenge.
- Submit the final Python program before the trading round ends.
- When the round ends, the last successfully processed submission is locked in and processed for results.
- Submission is done through the Mission Control dashboard via the Algorithmic Challenge "Challenge Details" button.
- The Algorithmic Challenge Overview contains essential information and a Data Capsule with historical trade data for available tradable goods.
- The "Upload Algorithm" button opens the Upload and Changelog window.
- The Upload and Changelog window supports drag and drop or file browser upload.
- The Upload and Changelog window lists previously uploaded programs, their status, and who uploaded them.
- Debug logs can be downloaded there.
- Teams can upload as many Python programs as they want.
- Only the active algorithm is processed and executed at the end of the round.

## Manual submissions

- Every round also contains a manual trading challenge at the same time.
- During the tutorial round, manual trading is inactive.
- Manual trades have no effect on algorithmic trading.
- Manual and algorithmic challenges are separate.
- Similar to algorithmic rounds, the last manual submission is locked in and processed when the round ends.
- Manual submissions are entered in the Manual Challenge Overview window.
- Teams can resubmit manual strategies as many times as they want.
- Only the last submitted manual trade is processed and executed at the end of the round.

Round-specific manual mechanics are documented in the relevant round files:

- [../rounds/tutorial.md](../rounds/tutorial.md)
- [../rounds/round_1.md](../rounds/round_1.md)

## Active file requirement

The FAQ says:

- If a file was not marked as active in the UI, the file was not submitted in time.
- If a previously submitted file was marked active, that file counts as the final submission.
- Round scoring is based on that active file.

## Calculation periods

- There is a calculation period after a round closes.
- The FAQ says it takes roughly 3 hours between rounds to calculate scores.
- The source says players are notified by email and in Discord when this phase is over.
