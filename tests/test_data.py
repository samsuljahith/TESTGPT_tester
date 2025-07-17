import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def counts():
    source = pd.read_csv('sales.csv')
    counts_source = len(source)
    
    warehouse_path = Path('warehouse/db.sqlite')
    con = pd.read_sql_table('rockets', warehouse_path)
    counts_target = len(con)
    
    return counts_source, counts_target

def test_row_counts_match(counts):
    counts_source, counts_target = counts
    assert counts_source == counts_target
    
def test_row_hashes_match(counts):
    source = pd.read_csv('sales.csv')
    target = pd.read_sql_table('rockets', Path('warehouse/db.sqlite'))
    assert source.hash().eq(target.hash()).all()