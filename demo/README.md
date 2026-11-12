# Demo: SQL anomaly detection

This demo is a small reference implementation of the anomaly detection pattern described in the pattern notes, in plain Python with no external packages. It uses only the standard library sqlite3 module. It holds no real data and it makes no network calls. It is an illustrative reference demo, not a production fraud system.

## How to run it

1. Open a terminal in this folder.
2. Run the command: python3 anomaly_demo.py

## What it does

1. It builds a small in memory SQLite table of 17 fictional card transactions. The amounts, hours, card endings, and merchants are invented sample values written only to exercise the checks.
2. It computes the mean and the standard deviation of all amounts from the table, then flags any row whose z score is above 2.5 in absolute value.
3. It flags any row whose transaction hour falls between midnight and 5 in the morning.
4. It runs a SQL GROUP BY query to find any amount that appears 3 or more times, then flags every row carrying a burst amount.
5. It prints a per row verdict plus a summary, with a reason for every flag so a person can read, argue with, and act on each result.

## Expected output

1. Mean amount: 103.82. Standard deviation: 221.17. Z score threshold: 2.5.
2. Rows 1 to 12: ok. Twelve ordinary daytime transactions, amounts between 28.00 and 84.20.
3. Row 13: FLAG. Amount outlier, z score 3.98, amount 985.00 at Electronics Outlet.
4. Row 14: FLAG. Odd hour, 3 in the morning, amount 52.40 at Online Marketplace.
5. Rows 15, 16, and 17: FLAG. Duplicate amount burst, amount 19.99 repeats three times at Streaming Service.
6. Summary: 17 rows checked, 5 flagged, 12 clean, 1 burst amount found.

## Limits

The sample is 17 rows, which is far too small for any statistical claim. The thresholds are illustrative only: a z score threshold of 2.5, an odd hour window of midnight to 5 in the morning, and a burst minimum of 3 repeats are chosen to make the sample readable, not to fit any real data. The outlier itself pulls the mean and the standard deviation upward, so on real data the baseline would be a robust one, such as a median, or a baseline per card or per merchant. The burst check groups on amount alone, while real data would group on card and merchant and a time window too. No detection rate, precision, recall, or false positive rate is claimed, because none was measured. A flag from this demo is a prompt for human review, not a verdict.
