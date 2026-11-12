# SQL anomaly detection

A small reference demo for SQL anomaly detection on a transaction table, built by Nirmeet Rao. It shows the shape of the checks that sit behind fraud and anomaly work: put the data in a table, ask the table plain questions, and let a human review whatever looks unusual.

The demo builds a small in memory SQLite table of 17 fictional card transactions, then runs three checks: an amount outlier check based on the z score, an odd hour check for transactions between midnight and 5 in the morning, and a duplicate amount burst check written as a SQL GROUP BY query. It prints a verdict for every row plus a summary. The transactions, amounts, hours, card endings, and merchants are invented sample values written only to exercise the checks. They are not real transaction data, and no fraud rate, accuracy, or performance number is claimed anywhere here.

## The idea in one paragraph

Anomaly detection starts with a baseline. Most transactions look ordinary, so the job is to describe ordinary first and then notice what departs from it. This demo describes ordinary in three simple ways: the average amount and how far amounts usually spread, the hours when transactions normally happen, and how often any single amount repeats. Each check is one plain question against the table, and each flag is a prompt for human review rather than a verdict. That is the whole pattern, and it is the pattern that scales: the same three questions run unchanged on a table of 17 rows or a table of 17 million, with the thresholds tuned to the data.

## The three checks

1. Amount outlier. The mean and standard deviation of all amounts are computed from the table. A row is flagged when its z score is above 2.5 in absolute value. In this sample, one row of 985.00 carries a z score of 3.98 and is flagged, while every other row stays inside the threshold.
2. Odd hour. A row is flagged when the transaction hour falls between midnight and 5 in the morning. In this sample, one row at 3 in the morning is flagged. The hour alone proves nothing, so the flag asks for a look, not a block.
3. Duplicate amount burst. A SQL GROUP BY query finds any amount that appears 3 or more times. In this sample, the amount 19.99 appears exactly 3 times and all three rows are flagged. A repeated identical charge is a common shape for a subscription retry loop or a test card probe, and either way it deserves a look.

## The demo in this repository

The demo folder contains a small reference demo in plain Python with no external packages, using only the standard library sqlite3 module. It creates the table, loads the 17 sample rows, runs the three checks, and prints a per row verdict plus a summary: 17 rows checked, 5 flagged, 12 clean, 1 burst amount found. The docs folder describes the pattern in general terms and its limits.

## Where this pattern already runs

The same shape appears in the products Nirmeet has built. His credit card fraud detection project, in this same GitHub account, trains a model on transaction features and reports a confusion matrix and classification report, and the checks here are the rule based complement to that model: cheap, explainable questions that run before or beside the model. PharmFlows, the LLM workflows he shipped at Concordia Pharma, reported serving time errors down 86 percent and cycle time down 30 percent on his resume, and those gains came from structure, validation, and review around the model rather than from more model calls. Paxei, his prior authorization preparation product, designs LLM document parsing and clinical drafts around payer criteria guardrails and human review. In each case the system earns trust by checking its own work in the open, with a human deciding what a flag means.

## What this is not

This repository is not a fraud detection system, and it is not a claim about any real transaction data. It contains no real transactions, no measured detection rate, and no claim that these three checks catch fraud. The thresholds are illustrative only: a z score threshold of 2.5, an odd hour window of midnight to 5 in the morning, and a burst minimum of 3 repeats are chosen to make the sample readable, not to fit any real data. On real data the thresholds would be tuned, the baseline would be per card or per merchant, and the checks would be one layer among many. A flag from this demo is a prompt for human review, not a verdict.

## Links

1. Portfolio: https://nirmeetrao.com
2. GitHub: https://github.com/Zaczee77
3. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
