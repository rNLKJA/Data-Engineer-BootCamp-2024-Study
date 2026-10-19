[0m09:07:23  Running with dbt=1.12.6
[0m09:07:23  Registered adapter: duckdb=1.11.0
[0m09:07:23  Unable to do partial parsing because saved manifest not found. Starting full parse.
[0m09:07:24  [[33mWARNING[0m]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 2 unused configuration paths:
- models.taxi_analytics.marts
- models.taxi_analytics.staging
[0m09:07:24  Found 3 models, 4 data tests, 1 source, 500 macros
[0m09:07:24  
[0m09:07:24  Concurrency: 4 threads (target='dev')
[0m09:07:24  
[0m09:07:24  
[0m09:07:24  Finished running  in 0 hours 0 minutes and 0.03 seconds (0.03s).
[0m09:07:24  [[31mERROR[0m]: Encountered an error:
IO Error: Cannot open file "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/week3_data_warehouse/taxi.duckdb": No such file or directory
[0m09:07:24  Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 110, in exception_handler
    yield
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/sql/connections.py", line 147, in add_query
    cursor = connection.handle.cursor()
             ^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/contracts/connection.py", line 96, in handle
    self._handle.resolve(self)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/contracts/connection.py", line 120, in resolve
    return self.opener(connection)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 68, in open
    connection.handle = cls._ENV.handle()
                        ^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/environments/local.py", line 79, in handle
    self.conn = self.initialize_db(self.creds, self._plugins)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/environments/__init__.py", line 164, in initialize_db
    conn = duckdb.connect(creds.path, read_only=False, config=config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_duckdb.IOException: IO Error: Cannot open file "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/week3_data_warehouse/taxi.duckdb": No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 110, in exception_handler
    yield
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/base/impl.py", line 1372, in execute_macro
    result = macro_function(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/clients/jinja.py", line 427, in __call__
    return self.call_macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/clients/jinja.py", line 395, in call_macro
    return macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 770, in __call__
    return self._invoke(arguments, autoescape)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 784, in _invoke
    rv = self._func(*arguments)
         ^^^^^^^^^^^^^^^^^^^^^^
  File "<template>", line 20, in macro
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/sandbox.py", line 401, in call
    return __context.call(__obj, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 303, in call
    return __obj(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/clients/jinja.py", line 151, in __call__
    return self.call_macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/clients/jinja.py", line 395, in call_macro
    return macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 770, in __call__
    return self._invoke(arguments, autoescape)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 784, in _invoke
    rv = self._func(*arguments)
         ^^^^^^^^^^^^^^^^^^^^^^
  File "<template>", line 50, in macro
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/sandbox.py", line 401, in call
    return __context.call(__obj, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 303, in call
    return __obj(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/clients/jinja.py", line 151, in __call__
    return self.call_macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/clients/jinja.py", line 395, in call_macro
    return macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 770, in __call__
    return self._invoke(arguments, autoescape)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 784, in _invoke
    rv = self._func(*arguments)
         ^^^^^^^^^^^^^^^^^^^^^^
  File "<template>", line 33, in macro
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/sandbox.py", line 401, in call
    return __context.call(__obj, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 303, in call
    return __obj(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/clients/jinja.py", line 151, in __call__
    return self.call_macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/clients/jinja.py", line 395, in call_macro
    return macro(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 770, in __call__
    return self._invoke(arguments, autoescape)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 784, in _invoke
    rv = self._func(*arguments)
         ^^^^^^^^^^^^^^^^^^^^^^
  File "<template>", line 52, in macro
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/sandbox.py", line 401, in call
    return __context.call(__obj, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/jinja2/runtime.py", line 303, in call
    return __obj(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/record.py", line 538, in record_replay_wrapper
    return func_to_record(*call_args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/base/impl.py", line 523, in execute
    return self.connections.execute(sql=sql, auto_begin=auto_begin, fetch=fetch, limit=limit)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 145, in execute
    return super().execute(sql, auto_begin, fetch, limit)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/sql/connections.py", line 219, in execute
    _, cursor = self.add_query(sql, auto_begin)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/sql/connections.py", line 131, in add_query
    with self.exception_handler(sql):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/rinh/.pyenv/versions/3.12.7/lib/python3.12/contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 117, in exception_handler
    self.rollback_if_open()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/base/connections.py", line 125, in rollback_if_open
    if conn is not None and conn.handle and conn.transaction_open:
                            ^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/contracts/connection.py", line 96, in handle
    self._handle.resolve(self)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/contracts/connection.py", line 120, in resolve
    return self.opener(connection)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 68, in open
    connection.handle = cls._ENV.handle()
                        ^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/environments/local.py", line 79, in handle
    self.conn = self.initialize_db(self.creds, self._plugins)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/environments/__init__.py", line 164, in initialize_db
    conn = duckdb.connect(creds.path, read_only=False, config=config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_duckdb.IOException: IO Error: Cannot open file "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/week3_data_warehouse/taxi.duckdb": No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/requires.py", line 198, in wrapper
    result, success = func(*args, **kwargs)
                      ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/requires.py", line 144, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/requires.py", line 295, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/requires.py", line 340, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/requires.py", line 387, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/requires.py", line 404, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/cli/main.py", line 609, in run
    results = task.run()
              ^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/task/runnable.py", line 775, in run
    result = self.execute_with_hooks(selected_uids)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/task/runnable.py", line 701, in execute_with_hooks
    before_run_status = self.before_run(adapter, selected_uids)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/task/run.py", line 1313, in before_run
    self.create_schemas(adapter, required_schemas)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/task/runnable.py", line 883, in create_schemas
    existing_schemas_lowered.update(ls_future.result())
                                    ^^^^^^^^^^^^^^^^^^
  File "/Users/rinh/.pyenv/versions/3.12.7/lib/python3.12/concurrent/futures/_base.py", line 449, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/rinh/.pyenv/versions/3.12.7/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
  File "/Users/rinh/.pyenv/versions/3.12.7/lib/python3.12/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt_common/utils/executor.py", line 20, in connected
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/task/runnable.py", line 858, in list_schemas
    for s in adapter.list_schemas(database_quoted)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/sql/impl.py", line 219, in list_schemas
    results = self.execute_macro(LIST_SCHEMAS_MACRO_NAME, kwargs={"database": database})
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/base/impl.py", line 1371, in execute_macro
    with self.connections.exception_handler(f"macro {macro_name}"):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/rinh/.pyenv/versions/3.12.7/lib/python3.12/contextlib.py", line 158, in __exit__
    self.gen.throw(value)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 117, in exception_handler
    self.rollback_if_open()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/base/connections.py", line 125, in rollback_if_open
    if conn is not None and conn.handle and conn.transaction_open:
                            ^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/contracts/connection.py", line 96, in handle
    self._handle.resolve(self)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/contracts/connection.py", line 120, in resolve
    return self.opener(connection)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/connections.py", line 68, in open
    connection.handle = cls._ENV.handle()
                        ^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/environments/local.py", line 79, in handle
    self.conn = self.initialize_db(self.creds, self._plugins)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/venv/lib/python3.12/site-packages/dbt/adapters/duckdb/environments/__init__.py", line 164, in initialize_db
    conn = duckdb.connect(creds.path, read_only=False, config=config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_duckdb.IOException: IO Error: Cannot open file "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week4_analytics_engineering/week3_data_warehouse/taxi.duckdb": No such file or directory

[0m09:07:40  Running with dbt=1.12.6
[0m09:07:40  Registered adapter: duckdb=1.11.0
[0m09:07:40  Unable to do partial parsing because profile has changed
[0m09:07:41  [[33mWARNING[0m]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 2 unused configuration paths:
- models.taxi_analytics.staging
- models.taxi_analytics.marts
[0m09:07:41  Found 3 models, 4 data tests, 1 source, 500 macros
[0m09:07:41  
[0m09:07:41  Concurrency: 4 threads (target='dev')
[0m09:07:41  
[0m09:07:41  1 of 3 START sql view model analytics.stg_yellow_trips ......................... [RUN]
[0m09:07:41  1 of 3 ERROR creating sql view model analytics.stg_yellow_trips ................ [[31mERROR[0m in 0.03s]
[0m09:07:41  2 of 3 SKIP relation analytics.fact_trips ...................................... [[33mSKIP[0m]
[0m09:07:41  3 of 3 SKIP relation analytics.monthly_revenue ................................. [[33mSKIP[0m]
[0m09:07:41  
[0m09:07:41  Finished running 2 table models, 1 view model in 0 hours 0 minutes and 0.09 seconds (0.09s).
[0m09:07:41  
[0m09:07:41  [31mCompleted with 1 error, 0 partial successes, and 0 warnings:[0m
[0m09:07:41  
[0m09:07:41  [[31mERROR[0m]: in model stg_yellow_trips (models/stg_yellow_trips.sql)
[0m09:07:41    Runtime Error in model stg_yellow_trips (models/stg_yellow_trips.sql)
  IO Error: No files found that match the pattern "../week2_workflow_orchestration/data_lake/yellow_taxi/**/*.parquet"
  
  LINE 8:     SELECT * FROM read_parquet('../week2_workflow_orchestration/data_lake...
                            ^
[0m09:07:41  
[0m09:07:41    compiled code at target/compiled/taxi_analytics/models/stg_yellow_trips.sql
[0m09:07:41  
[0m09:07:41  Done. PASS=0 WARN=0 ERROR=1 SKIP=2 NO-OP=0 REUSED=0 TOTAL=3

## Week 4 Homework - FHV 2019

**Date**: October 2026
**Dataset**: FHV (For-Hire Vehicle) 2019 full year
**Source**: https://d37ci6vzurychx.cloudfront.net/trip-data/

### dbt Models Built

1. `stg_fhv_tripdata` - Staging view (filters to 2019)
2. `fact_fhv_trips` - Fact table with zone joins

### Execution

```bash
cd taxi_analytics
export DBT_PROFILES_DIR=..
dbt run --select stg_fhv_tripdata fact_fhv_trips
python ../homework_fhv_2019.py
```

### Results

**Question 1**: 41,231,038 records in fact_fhv_trips
**Question 3**: 43,261,276 records in stg_fhv_tripdata
**Question 4**: 41,231,038 records in fact_fhv_trips (after zone join filter)
**Question 5**: January 2019 had the most trips

Difference between staging and fact: 2,030,238 records filtered out due to missing/invalid location IDs in the zone lookup.
