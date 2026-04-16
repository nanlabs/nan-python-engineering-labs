"""Basic example: CTE and window function style SQL."""
import sqlite3
from pathlib import Path

db = Path('/tmp/m13_postgres_adv.db')
if db.exists():
    db.unlink()

conn = sqlite3.connect(db)
conn.execute('CREATE TABLE sales (region TEXT, seller TEXT, amount INTEGER)')
conn.executemany('INSERT INTO sales VALUES (?, ?, ?)', [
    ('north', 'alice', 120), ('north', 'bob', 80), ('south', 'carl', 90), ('south', 'diana', 150),
])

cte = conn.execute(
    'WITH totals AS (SELECT region, SUM(amount) total FROM sales GROUP BY region) '
    'SELECT region, total FROM totals ORDER BY total DESC'
).fetchall()
print('cte=', cte)

ranking = conn.execute(
    'SELECT seller, region, amount, RANK() OVER (PARTITION BY region ORDER BY amount DESC) '
    'FROM sales'
).fetchall()
print('rank=', ranking)
