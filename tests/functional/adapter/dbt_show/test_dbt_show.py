import pytest
from dbt.tests.adapter.dbt_show.test_dbt_show import (
    BaseShowSqlHeader,
    BaseShowLimit,
    BaseShowDoesNotHandleDoubleLimit,
)

from dbt.tests.util import run_dbt

model_with_json_struct = """
    select *
    from (
        select
  struct<
    k array<
        struct<c1 int64, c2 json>
      >
  >(
    [
      struct(
        1 as c1,
        to_json(struct(1 as a)) as c2
      )
    ]
  )
  as v
    )
    """

model_with_null_json_struct = """
    select (struct<k json>(null)) as null_struct
"""


class TestBigQueryShowLimit(BaseShowLimit):
    pass


class TestBigQueryShowSqlHeader(BaseShowSqlHeader):
    pass


# Added to check if dbt show works with JSON struct
# Addresses: https://github.com/dbt-labs/dbt-bigquery/issues/972
class TestBigQueryShowSqlWorksWithJSONStruct:
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "json_struct_model.sql": model_with_json_struct,
            "null_json_struct_model.sql": model_with_null_json_struct,
        }

    def test_sql_header(self, project):
        run_dbt(["show", "--select", "json_struct_model", "-d"])

    def test_show_with_null_json_struct(self, project):
        run_dbt(["show", "--select", "null_json_struct_model"])


class TestBigQueryShowDoesNotHandleDoubleLimit(BaseShowDoesNotHandleDoubleLimit):
    DATABASE_ERROR_MESSAGE = "Syntax error: Expected end of input but got keyword LIMIT"
