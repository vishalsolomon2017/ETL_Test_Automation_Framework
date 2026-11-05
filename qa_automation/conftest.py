
import pytest
import pandas as pd
from pyspark.sql import SparkSession


# Actual Excel file paths

SOURCE_PATH = "qa_automation/Tables/Source_table.xlsx"
TARGET_PATH = "qa_automation/Tables/Target_table_1.xlsx"


# Create Spark session

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .appName("ETL Pytest Automation")
        .master("local[*]")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    yield spark

    spark.stop()


# Load actual source Excel file

@pytest.fixture(scope="session")
def source_df(spark):
    source_pd = pd.read_excel(SOURCE_PATH)

    source_df = spark.createDataFrame(source_pd)

    return source_df


# Load actual target Excel file

@pytest.fixture(scope="session")
def target_df(spark):
    target_pd = pd.read_excel(TARGET_PATH)

    target_df = spark.createDataFrame(target_pd)

    return target_df
