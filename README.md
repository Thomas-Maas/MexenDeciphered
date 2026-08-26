# Mexen Deciphered

A Monte Carlo simulation of the Dutch dice game *Mexen*, built to test whether a common
house-rule variant actually changes the game — and whether the answer depends on how many
people are playing.

*Mexen* is played with several house rules that groups argue about. The argument is
usually settled by opinion. This settles it by simulation.

## What it compares

Two rule variants, across table sizes of 5, 10, 25 and 50 players, at 2,000 rounds per
configuration.

Rather than only reporting total drinks, the simulation tracks where they come from —
losing a round, the knight mechanic, and the rule that lets a player nominate someone
else. That separation is the point: two rule sets can produce a similar total while
redistributing it completely differently across the table.

Results are plotted as a four-panel comparison, one panel per table size.

![Results](mexen%20resultaat%201.png)

<!-- TODO: one sentence here stating what you concluded. The chart is in the repo but
     the finding isn't written down anywhere, and that's the only thing a reader wants. -->

## Modelling notes

The knight mechanic carries state across rounds, so rounds are simulated as a sequence
rather than independently.

Player behaviour is reduced to a single probability parameter for the one real decision
in the game: whether to stop or push on. There is no data on how people actually make
that call, so it is a tunable input rather than a claim. It is currently fixed at one
value and not swept.

## Scope

This compares rules, not strategies — every player behaves identically. It tells you what
a rule change does to the drink economy, not how to play better. The companion project
[31enDeciphered](https://github.com/Thomas-Maas/31enDeciphered) does the strategy side.

## Running it

```bash
pip install numpy matplotlib
python mexen.py
```

Parameters are set at the bottom of the file. The simulation logs every roll, which makes
runs slow and noisy.

## Status

Written a while ago and not actively maintained.
