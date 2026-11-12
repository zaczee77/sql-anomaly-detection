"""Reference demo: SQL anomaly detection on a small transaction table.

Illustrative reference demo only. This is not a production fraud system
and it makes no claim about any real transaction data. It builds a
small in memory SQLite table of 17 fictional card transactions, then
runs three checks that mirror the shape of real anomaly detection:

1. Amount outlier. The mean and standard deviation of all amounts are
   computed from the table, and a row is flagged when its z score is
   above 2.5 in absolute value. One row is far above the rest.
2. Odd hour. A row is flagged when the transaction hour falls between
   midnight and 5 in the morning. One row lands at 3 in the morning.
3. Duplicate amount burst. A SQL GROUP BY query finds any amount that
   appears 3 or more times. One amount appears exactly 3 times.

The amounts, hours, card endings, and merchants are invented sample
values written only to exercise the checks. Standard library only.
No network, no real data.
"""

import sqlite3

ROWS = [
    (1, "4417", 42.10, 9, "Corner Grocery"),
    (2, "4417", 58.75, 12, "City Pharmacy"),
    (3, "9023", 31.20, 10, "Corner Grocery"),
    (4, "4417", 76.40, 15, "Office Supply Co"),
    (5, "9023", 49.99, 11, "Bookshop"),
    (6, "4417", 63.50, 18, "Corner Grocery"),
    (7, "9023", 28.00, 13, "Coffee Stand"),
    (8, "4417", 84.20, 16, "City Pharmacy"),
    (9, "9023", 55.00, 14, "Bookshop"),
    (10, "4417", 39.95, 10, "Coffee Stand"),
    (11, "9023", 67.30, 19, "Office Supply Co"),
    (12, "4417", 71.15, 17, "Corner Grocery"),
    (13, "4417", 985.00, 14, "Electronics Outlet"),
    (14, "9023", 52.40, 3, "Online Marketplace"),
    (15, "4417", 19.99, 11, "Streaming Service"),
    (16, "4417", 19.99, 11, "Streaming Service"),
    (17, "4417", 19.99, 11, "Streaming Service"),
]

Z_THRESHOLD = 2.5
ODD_HOUR_START = 0
ODD_HOUR_END = 5
BURST_MINIMUM = 3


def build_table(connection):
    connection.execute(
        "CREATE TABLE transactions ("
        " id INTEGER PRIMARY KEY,"
        " card_last4 TEXT,"
        " amount REAL,"
        " hour INTEGER,"
        " merchant TEXT)"
    )
    connection.executemany(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", ROWS
    )


def amount_stats(connection):
    amounts = [row[0] for row in connection.execute(
        "SELECT amount FROM transactions"
    )]
    mean = sum(amounts) / len(amounts)
    variance = sum((value - mean) ** 2 for value in amounts) / len(amounts)
    return mean, variance ** 0.5


def burst_amounts(connection):
    rows = connection.execute(
        "SELECT amount, COUNT(*) AS n FROM transactions"
        " GROUP BY amount HAVING n >= ?",
        (BURST_MINIMUM,),
    )
    return {row[0] for row in rows}


def check_row(row, mean, stddev, bursts):
    row_id, card, amount, hour, merchant = row
    flags = []
    z_score = (amount - mean) / stddev
    if abs(z_score) > Z_THRESHOLD:
        flags.append(
            "amount outlier: z score %.2f" % z_score
        )
    if ODD_HOUR_START <= hour < ODD_HOUR_END:
        flags.append("odd hour: %d in the morning" % hour)
    if amount in bursts:
        flags.append("duplicate amount burst: %.2f repeats" % amount)
    return flags


def main():
    connection = sqlite3.connect(":memory:")
    build_table(connection)
    mean, stddev = amount_stats(connection)
    bursts = burst_amounts(connection)

    print("SQL anomaly detection reference demo")
    print("  Rows in table: 17")
    print("  Mean amount: %.2f" % mean)
    print("  Standard deviation: %.2f" % stddev)
    print("  Z score threshold: %.1f" % Z_THRESHOLD)
    print()

    flagged_count = 0
    for row in connection.execute(
        "SELECT id, card_last4, amount, hour, merchant"
        " FROM transactions ORDER BY id"
    ):
        flags = check_row(row, mean, stddev, bursts)
        row_id, card, amount, hour, merchant = row
        if flags:
            flagged_count += 1
            verdict = "FLAG"
        else:
            verdict = "ok"
        print(
            "Row %d  card %s  %.2f  hour %d  %s  verdict: %s"
            % (row_id, card, amount, hour, merchant, verdict)
        )
        for flag in flags:
            print("  [flag] " + flag)
    print()
    print("Summary")
    print("  Rows checked: 17")
    print("  Rows flagged: %d" % flagged_count)
    print("  Rows clean: %d" % (17 - flagged_count))
    print("  Burst amounts found: %d" % len(bursts))
    print("  Note: every flag is a prompt for human review, not a verdict.")


if __name__ == "__main__":
    main()
