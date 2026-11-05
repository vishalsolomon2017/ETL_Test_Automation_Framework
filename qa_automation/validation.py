
from pyspark.sql.functions import col


# 1. Count Validation

def validate_count(df_s, df_t):
    source_count = df_s.count()
    target_count = df_t.count()

    if source_count == target_count:
        status = "PASS"
    else:
        status = "FAIL"

    result = {
        "check_name": "Count Validation",
        "source_count": source_count,
        "target_count": target_count,
        "status": status
    }

    return result


# 2. Primary Key Validation

def validate_duplicate(df_t, pk_col):
    null_count = (
        df_t.filter(col(pk_col).isNull()).count()
    )

    duplicate_count = (
        df_t.groupBy(pk_col)
        .count()
        .filter(col("count") > 1)
        .count()
    )

    if null_count == 0 and duplicate_count == 0:
        status = "PASS"
    else:
        status = "FAIL"

    result = {
        "check_name": "Primary Key Validation",
        "null_count": null_count,
        "duplicate_count": duplicate_count,
        "status": status
    }

    return result


# 3. Source-Target Comparison

def validate_source_target(df_s, df_t):
    source_minus_target = df_s.subtract(df_t)
    target_minus_source = df_t.subtract(df_s)

    source_minus_target_count = (
        source_minus_target.count()
    )

    target_minus_source_count = (
        target_minus_source.count()
    )

    if (
        source_minus_target_count == 0
        and target_minus_source_count == 0
    ):
        status = "PASS"
    else:
        status = "FAIL"

    result = {
        "check_name": "Source Target Comparison",
        "source_minus_target_count": source_minus_target_count,
        "target_minus_source_count": target_minus_source_count,
        "status": status
    }

    return result
