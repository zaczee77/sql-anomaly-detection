# Pattern notes: SQL anomaly detection

## The problem

A transaction table is mostly ordinary. The anomaly detection problem is to describe ordinary in a way a query can test, then surface the rows that depart from it. The three checks in this demo are three different descriptions of ordinary: how big amounts usually are, when transactions usually happen, and how often any one amount repeats.

## Check 1: amount outlier with a z score

The demo computes the mean and the standard deviation of every amount in the table, then scores each row as a z score, which is the distance from the mean measured in units of standard deviation. A row is flagged when the absolute z score is above 2.5.

This check has a known weakness that the demo shows on purpose. The outlier itself pulls the mean and the standard deviation upward, so a table with one huge row reports a mean of 103.82 and a standard deviation of 221.17 even though 12 of the 17 rows sit between 28.00 and 84.20. On real data the fix is a robust baseline: a median and a median absolute deviation, or a baseline computed per card or per merchant, or a baseline from a trailing window rather than from all time. The z score is kept here because it is the simplest version of the idea and it is easy to explain to a reviewer.

## Check 2: odd hour

The demo flags any row whose hour falls between midnight and 5 in the morning. The window is illustrative only. On real data the window would come from the cardholder's own history, since a night shift worker transacts at 3 in the morning every day and a daytime shopper never does. The check is useful as a signal to combine with others, not as a rule on its own. An odd hour plus an unusual amount is a much stronger story than either flag alone, which is why the demo prints every flag on a row instead of stopping at the first one.

## Check 3: duplicate amount burst in SQL

The demo finds repeated amounts with a single SQL query: GROUP BY amount, HAVING COUNT(*) >= 3. This is the most SQL native of the three checks, and it is the one that scales best, because the database does the grouping and the application only reads the short list of burst amounts. On real data the grouping would usually add a card or a merchant and a time window, so that the same amount charged to different cards at different merchants does not count as a burst. The demo groups on amount alone to keep the sample readable.

## Why three checks instead of one score

A single anomaly score hides the reason. Three named checks give a reviewer a sentence for each flag: the amount is far from the mean, the hour is unusual, the amount repeats. That sentence is what lets a human decide quickly, and it is what lets a team argue about a threshold and change it. The same lesson runs through the evaluation work in this series: a check that is written down, versioned, and run the same way every time is a contract with the user about what good means.

## Limits

The sample is 17 rows, which is far too small for any statistical claim, and the thresholds are chosen to make the sample readable. No detection rate, precision, recall, or false positive rate is claimed, because none was measured. The demo runs entirely in memory and holds no state between runs. Nothing here should be used to block a real transaction. Every flag is a prompt for human review, not a verdict.
