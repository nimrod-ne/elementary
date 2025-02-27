import json
from typing import List, Optional, Union

from pydantic import BaseModel, validator

from elementary.utils.time import convert_partial_iso_format_to_full_iso_format

TestUniqueIdType = str
ModelUniqueIdType = str


class TestMetadataSchema(BaseModel):
    id: str
    model_unique_id: Optional[ModelUniqueIdType] = None
    test_unique_id: TestUniqueIdType
    detected_at: str
    database_name: str = None
    schema_name: str
    table_name: Optional[str] = None
    column_name: Optional[str]
    test_type: str
    test_sub_type: str
    test_results_description: Optional[str]
    owners: Optional[str]
    tags: Optional[str]
    meta: Optional[dict]
    test_results_query: Optional[str] = None
    other: Optional[str]
    test_name: str
    test_params: Optional[str]
    severity: str
    status: str
    test_created_at: Optional[str] = None
    days_diff: float

    @validator("detected_at", pre=True)
    def format_detected_at(cls, detected_at):
        return convert_partial_iso_format_to_full_iso_format(detected_at)

    @validator("meta", pre=True)
    def load_meta(cls, meta):
        return json.loads(meta) if meta else {}


class TotalsSchema(BaseModel):
    errors: Optional[int] = 0
    warnings: Optional[int] = 0
    passed: Optional[int] = 0
    failures: Optional[int] = 0

    def add_total(self, status):
        total_adders = {
            "error": self._add_error,
            "warn": self._add_warning,
            "fail": self._add_failure,
            "pass": self._add_passed,
        }
        adder = total_adders.get(status)
        if adder:
            adder()

    def _add_error(self):
        self.errors += 1

    def _add_warning(self):
        self.warnings += 1

    def _add_passed(self):
        self.passed += 1

    def _add_failure(self):
        self.failures += 1


class InvocationSchema(BaseModel):
    affected_rows: Optional[int]
    time_utc: str
    id: str
    status: str

    @validator("time_utc", pre=True)
    def format_time_utc(cls, time_utc):
        return convert_partial_iso_format_to_full_iso_format(time_utc)


class InvocationsSchema(BaseModel):
    fail_rate: float
    totals: TotalsSchema
    invocations: List[InvocationSchema]
    description: str


class TestInfoSchema(BaseModel):
    test_unique_id: Optional[str] = None
    database_name: Optional[str] = None
    schema_name: Optional[str] = None
    table_name: Optional[str] = None
    column_name: Optional[str] = None
    test_name: Optional[str] = None
    test_display_name: Optional[str] = None
    latest_run_time: Optional[str] = None
    latest_run_time_utc: Optional[str] = None
    latest_run_status: Optional[str] = None
    model_unique_id: Optional[str] = None
    table_unique_id: Optional[str] = None
    test_type: Optional[str] = None
    test_sub_type: Optional[str] = None
    test_query: Optional[str] = None
    test_params: Optional[dict] = None
    test_created_at: Optional[str] = None
    description: Optional[str] = None
    result: Optional[dict] = None
    configuration: Optional[dict] = None


class ElementaryTestResultSchema(BaseModel):
    display_name: str
    metrics: Optional[Union[list, dict]]
    result_description: str


class DbtTestResultSchema(BaseModel):
    display_name: str
    results_sample: Optional[list] = None
    error_message: str
    failed_rows_count: int


class TestResultSchema(BaseModel):
    metadata: TestInfoSchema
    test_results: Union[dict, list]


class TestRunSchema(BaseModel):
    metadata: TestInfoSchema
    test_runs: InvocationsSchema
