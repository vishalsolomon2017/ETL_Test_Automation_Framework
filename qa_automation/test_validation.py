
from pyspark.sql.functions import col,count

from validation import (
    validate_count,
    validate_duplicate,
    validate_source_target
)


# 1. Count Validation

def test_count_validation(source_df, target_df):
    result = validate_count(source_df, target_df)

    print("\nCount Validation Result:", result)

    # Verify returned counts
    assert result["source_count"] == source_df.count()
    assert result["target_count"] == target_df.count()

    # Business rule: counts must match
    assert result["status"] == "PASS", (
        f"Count validation failed. "
        f"Source count: {result['source_count']}, "
        f"Target count: {result['target_count']}"
    )


# 2. Primary Key Validation

def test_primary_key_validation(target_df):
    # Change this to your actual primary key column
    pk_col = "employee_id"

    result = validate_duplicate(target_df, pk_col)

    print("\nPrimary Key Validation Result:", result)

    # Business rule: no null primary keys
    assert result["null_count"] == 0, (
        f"Primary key contains {result['null_count']} null values"
    )

    # Business rule: no duplicate primary keys
    assert result["duplicate_count"] == 0, (
        f"Primary key contains "
        f"{result['duplicate_count']} duplicate key groups"
    )

    assert result["status"] == "PASS", (
        "Primary key validation failed"
    )


# 3. Source-Target Comparison

def test_source_target_validation(source_df, target_df):
    result = validate_source_target(source_df, target_df)

    print("\nSource-Target Validation Result:", result)

    # Business rule: no source rows missing from target
    assert result["source_minus_target_count"] == 0, (
        f"Source has "
        f"{result['source_minus_target_count']} distinct rows "
        f"missing from target"
    )

    # Business rule: no target rows missing from source
    assert result["target_minus_source_count"] == 0, (
        f"Target has "
        f"{result['target_minus_source_count']} distinct rows "
        f"missing from source"
    )

    assert result["status"] == "PASS", (
        "Source-target comparison failed"
    )


# python -m pytest qa_automation/test_validation.py -v -s
