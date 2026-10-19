19:30:41.809 | INFO    | prefect - Starting temporary server on http://127.0.0.1:8412
See https://docs.prefect.io/v3/concepts/server#how-to-guides for more information on running a dedicated Prefect server.
19:30:45.380 | ERROR   | docket.dependencies - ↩ [     9ms] send_telemetry_heartbeat(){send_telemetry_heartbeat}
Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1953, in _exec_single_context
    self.dialect.do_execute(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 1192, in do_execute
    cursor.execute(statement, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 258, in execute
    self._adapt_connection._handle_exception(error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 412, in _handle_exception
    self._handle_exception_no_connection(self.dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 237, in _handle_exception_no_connection
    super()._handle_exception_no_connection(dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 409, in _handle_exception_no_connection
    raise error.with_traceback(exc_info[2])
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 256, in execute
    return await_(self._execute_async(operation, parameters))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 167, in await_
    return current.parent.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 205, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 279, in _execute_async
    result = await self._cursor.execute(operation, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 40, in execute
    await self._execute(self._cursor.execute, sql, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 32, in _execute
    return await self._conn._execute(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
             ^^^^^^^^^^
sqlite3.OperationalError: database is locked

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/docket/worker.py", line 1134, in _execute
    result = await execution.function(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/services/telemetry.py", line 80, in send_telemetry_heartbeat
    session_start_timestamp, session_id = await _fetch_or_set_telemetry_session(db=db)
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/services/telemetry.py", line 54, in _fetch_or_set_telemetry_session
    await configuration.write_configuration(session, telemetry_session)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/models/configuration.py", line 29, in write_configuration
    await session.flush()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1030, in flush
    await greenlet_spawn(self.sync_session.flush, objects=objects)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 212, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4536, in flush
    self._flush(objects)
  File "<sqlalchemy generated warned() wrapper for sqlalchemy.orm.session.Session._flush>", line 2, in _flush
    return target(fn, self, objects=objects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4679, in _flush
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 166, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4640, in _flush
    flush_context.execute()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 467, in execute
    rec.execute(self)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 643, in execute
    util.preloaded.orm_persistence._save_obj(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 92, in _save_obj
    _emit_insert_statements(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 1237, in _emit_insert_statements
    result = connection.execute(
             ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1458, in execute
    return meth(
           ^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py", line 533, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1678, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1832, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1972, in _exec_single_context
    self._handle_dbapi_exception(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2342, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1953, in _exec_single_context
    self.dialect.do_execute(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 1192, in do_execute
    cursor.execute(statement, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 258, in execute
    self._adapt_connection._handle_exception(error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 412, in _handle_exception
    self._handle_exception_no_connection(self.dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 237, in _handle_exception_no_connection
    super()._handle_exception_no_connection(dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 409, in _handle_exception_no_connection
    raise error.with_traceback(exc_info[2])
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 256, in execute
    return await_(self._execute_async(operation, parameters))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 167, in await_
    return current.parent.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 205, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 279, in _execute_async
    result = await self._cursor.execute(operation, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 40, in execute
    await self._execute(self._cursor.execute, sql, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 32, in _execute
    return await self._conn._execute(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
             ^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) database is locked
[SQL: INSERT INTO configuration ("key", value, id, created, updated) VALUES (:key, :value, :id, :created, :updated)]
[parameters: {'key': 'TELEMETRY_SESSION', 'value': '{"session_id": "64991372-1bd2-4490-b4ca-f64d2c0340ce", "session_start_timestamp": "2026-10-19T09:00:45.377355+00:00"}', 'id': '2e63676a-6039-45f6-82e8-689e6bc23c8e', 'created': '2026-10-19 09:00:45.378820', 'updated': '2026-10-19 09:00:45.378823'}]
(Background on this error at: https://sqlalche.me/e/21/e3q8)
19:30:45.672 | INFO    | Flow run 'optimal-hippogriff' - Beginning flow run 'optimal-hippogriff' for flow 'etl-web-to-lake'
19:30:45.674 | INFO    | Flow run 'optimal-hippogriff' - === ETL Flow: 2021-01 ===
19:30:45.682 | INFO    | Task run 'download_data-a58' - Downloading https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet ...
19:30:46.113 | INFO    | Task run 'download_data-a58' - Task run failed with exception: HTTPError('404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet') - Retry 1/3 will start 10 second(s) from now
19:30:56.120 | INFO    | Task run 'download_data-a58' - Downloading https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet ...
19:30:56.289 | INFO    | Task run 'download_data-a58' - Task run failed with exception: HTTPError('404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet') - Retry 2/3 will start 10 second(s) from now
19:31:06.295 | INFO    | Task run 'download_data-a58' - Downloading https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet ...
19:31:06.449 | INFO    | Task run 'download_data-a58' - Task run failed with exception: HTTPError('404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet') - Retry 3/3 will start 10 second(s) from now
19:31:16.452 | INFO    | Task run 'download_data-a58' - Downloading https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet ...
19:31:16.599 | ERROR   | Task run 'download_data-a58' - Task run failed with exception: HTTPError('404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet') - Retries are exhausted
Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1027, in run_context
    yield self
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1696, in run_task_sync
    engine.call_task_fn(txn)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1044, in call_task_fn
    result = call_with_parameters(self.task.fn, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/utilities/callables/__init__.py", line 356, in call_with_parameters
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/etl_web_to_lake.py", line 41, in download_data
    response.raise_for_status()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/requests/models.py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet
19:31:16.610 | ERROR   | Task run 'download_data-a58' - Finished in state Failed('Task run encountered an exception HTTPError: 404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet')
19:31:16.786 | ERROR   | Flow run 'optimal-hippogriff' - Encountered exception during execution: HTTPError('404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet')
Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 1330, in run_context
    yield self
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 2111, in run_flow_sync
    engine.call_flow_fn()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 1350, in call_flow_fn
    result = call_with_parameters(self.flow.fn, self.parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/utilities/callables/__init__.py", line 356, in call_with_parameters
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/etl_web_to_lake.py", line 113, in etl_web_to_lake
    local_file = download_data(year, month, download_dir)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/tasks.py", line 1230, in __call__
    return run_task(
           ^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1929, in run_task
    return run_task_sync(**kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1699, in run_task_sync
    return engine.state if return_type == "state" else engine.result()
                                                       ^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 619, in result
    raise self._raised
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1027, in run_context
    yield self
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1696, in run_task_sync
    engine.call_task_fn(txn)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1044, in call_task_fn
    result = call_with_parameters(self.task.fn, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/utilities/callables/__init__.py", line 356, in call_with_parameters
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/etl_web_to_lake.py", line 41, in download_data
    response.raise_for_status()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/requests/models.py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet
19:31:16.811 | INFO    | Flow run 'optimal-hippogriff' - Finished in state Failed('Flow run encountered an exception: HTTPError: 404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet')
Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/etl_web_to_lake.py", line 134, in <module>
    etl_web_to_lake(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flows.py", line 1887, in __call__
    return run_flow(
           ^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 2268, in run_flow
    ret_val = run_flow_sync(**kwargs)
              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 2113, in run_flow_sync
    return engine.state if return_type == "state" else engine.result()
                                                       ^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 788, in result
    raise self._raised
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 1330, in run_context
    yield self
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 2111, in run_flow_sync
    engine.call_flow_fn()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/flow_engine.py", line 1350, in call_flow_fn
    result = call_with_parameters(self.flow.fn, self.parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/utilities/callables/__init__.py", line 356, in call_with_parameters
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/etl_web_to_lake.py", line 113, in etl_web_to_lake
    local_file = download_data(year, month, download_dir)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/tasks.py", line 1230, in __call__
    return run_task(
           ^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1929, in run_task
    return run_task_sync(**kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1699, in run_task_sync
    return engine.state if return_type == "state" else engine.result()
                                                       ^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 619, in result
    raise self._raised
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1027, in run_context
    yield self
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1696, in run_task_sync
    engine.call_task_fn(txn)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/task_engine.py", line 1044, in call_task_fn
    result = call_with_parameters(self.task.fn, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/utilities/callables/__init__.py", line 356, in call_with_parameters
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/etl_web_to_lake.py", line 41, in download_data
    response.raise_for_status()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/requests/models.py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.parquet
19:31:16.821 | INFO    | prefect - Stopping temporary server on http://127.0.0.1:8412
19:31:44.459 | INFO    | prefect - Starting temporary server on http://127.0.0.1:8642
See https://docs.prefect.io/v3/concepts/server#how-to-guides for more information on running a dedicated Prefect server.
19:31:45.953 | ERROR   | docket.dependencies - ↩ [   117ms] send_telemetry_heartbeat(){send_telemetry_heartbeat}
Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1953, in _exec_single_context
    self.dialect.do_execute(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 1192, in do_execute
    cursor.execute(statement, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 258, in execute
    self._adapt_connection._handle_exception(error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 412, in _handle_exception
    self._handle_exception_no_connection(self.dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 237, in _handle_exception_no_connection
    super()._handle_exception_no_connection(dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 409, in _handle_exception_no_connection
    raise error.with_traceback(exc_info[2])
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 256, in execute
    return await_(self._execute_async(operation, parameters))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 167, in await_
    return current.parent.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 205, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 279, in _execute_async
    result = await self._cursor.execute(operation, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 40, in execute
    await self._execute(self._cursor.execute, sql, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 32, in _execute
    return await self._conn._execute(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
             ^^^^^^^^^^
sqlite3.OperationalError: database is locked

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/docket/worker.py", line 1134, in _execute
    result = await execution.function(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/services/telemetry.py", line 80, in send_telemetry_heartbeat
    session_start_timestamp, session_id = await _fetch_or_set_telemetry_session(db=db)
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/services/telemetry.py", line 54, in _fetch_or_set_telemetry_session
    await configuration.write_configuration(session, telemetry_session)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/models/configuration.py", line 29, in write_configuration
    await session.flush()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1030, in flush
    await greenlet_spawn(self.sync_session.flush, objects=objects)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 212, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4536, in flush
    self._flush(objects)
  File "<sqlalchemy generated warned() wrapper for sqlalchemy.orm.session.Session._flush>", line 2, in _flush
    return target(fn, self, objects=objects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4679, in _flush
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 166, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4640, in _flush
    flush_context.execute()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 467, in execute
    rec.execute(self)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 643, in execute
    util.preloaded.orm_persistence._save_obj(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 92, in _save_obj
    _emit_insert_statements(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 1237, in _emit_insert_statements
    result = connection.execute(
             ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1458, in execute
    return meth(
           ^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py", line 533, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1678, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1832, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1972, in _exec_single_context
    self._handle_dbapi_exception(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2342, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1953, in _exec_single_context
    self.dialect.do_execute(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 1192, in do_execute
    cursor.execute(statement, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 258, in execute
    self._adapt_connection._handle_exception(error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 412, in _handle_exception
    self._handle_exception_no_connection(self.dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 237, in _handle_exception_no_connection
    super()._handle_exception_no_connection(dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 409, in _handle_exception_no_connection
    raise error.with_traceback(exc_info[2])
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 256, in execute
    return await_(self._execute_async(operation, parameters))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 167, in await_
    return current.parent.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 205, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 279, in _execute_async
    result = await self._cursor.execute(operation, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 40, in execute
    await self._execute(self._cursor.execute, sql, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 32, in _execute
    return await self._conn._execute(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
             ^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) database is locked
[SQL: INSERT INTO configuration ("key", value, id, created, updated) VALUES (:key, :value, :id, :created, :updated)]
[parameters: {'key': 'TELEMETRY_SESSION', 'value': '{"session_id": "127a4e98-bec2-469d-a44c-a8df642dee0e", "session_start_timestamp": "2026-10-19T09:01:45.845737+00:00"}', 'id': 'aed4e822-91a7-44ba-a26b-fe08c3330487', 'created': '2026-10-19 09:01:45.949556', 'updated': '2026-10-19 09:01:45.949561'}]
(Background on this error at: https://sqlalche.me/e/21/e3q8)
19:31:46.063 | INFO    | Flow run 'tall-badger' - Beginning flow run 'tall-badger' for flow 'etl-web-to-lake'
19:31:46.065 | INFO    | Flow run 'tall-badger' - === ETL Flow: 2021-01 ===
19:31:46.075 | INFO    | Task run 'download_data-4fb' - Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet ...
19:31:49.499 | INFO    | Task run 'download_data-4fb' - Downloaded to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/downloads/yellow_tripdata_2021-01.parquet (20.68 MB)
19:31:49.503 | INFO    | Task run 'download_data-4fb' - Finished in state Completed()
19:31:49.684 | INFO    | Task run 'transform_data-e25' - Loaded 1,369,769 rows from yellow_tripdata_2021-01.parquet
19:31:49.699 | INFO    | Task run 'transform_data-e25' - Transformed: 1,369,769 rows ready for load
19:31:49.700 | INFO    | Task run 'transform_data-e25' - Finished in state Completed()
19:31:50.300 | INFO    | Task run 'load_to_lake-b19' - Wrote 1,369,769 rows to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/yellow_tripdata_2021-01.parquet
19:31:50.301 | INFO    | Task run 'load_to_lake-b19' - Finished in state Completed()
19:31:50.301 | INFO    | Flow run 'tall-badger' - === Flow complete: 1,369,769 rows processed ===
19:31:51.092 | INFO    | Flow run 'tall-badger' - Finished in state Completed()
19:31:51.109 | INFO    | prefect - Stopping temporary server on http://127.0.0.1:8642
19:32:00.772 | INFO    | prefect - Starting temporary server on http://127.0.0.1:8092
See https://docs.prefect.io/v3/concepts/server#how-to-guides for more information on running a dedicated Prefect server.
19:32:02.099 | ERROR   | docket.dependencies - ↩ [    11ms] send_telemetry_heartbeat(){send_telemetry_heartbeat}
Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1953, in _exec_single_context
    self.dialect.do_execute(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 1192, in do_execute
    cursor.execute(statement, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 258, in execute
    self._adapt_connection._handle_exception(error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 412, in _handle_exception
    self._handle_exception_no_connection(self.dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 237, in _handle_exception_no_connection
    super()._handle_exception_no_connection(dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 409, in _handle_exception_no_connection
    raise error.with_traceback(exc_info[2])
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 256, in execute
    return await_(self._execute_async(operation, parameters))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 167, in await_
    return current.parent.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 205, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 279, in _execute_async
    result = await self._cursor.execute(operation, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 40, in execute
    await self._execute(self._cursor.execute, sql, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 32, in _execute
    return await self._conn._execute(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
             ^^^^^^^^^^
sqlite3.OperationalError: database is locked

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/docket/worker.py", line 1134, in _execute
    result = await execution.function(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/services/telemetry.py", line 80, in send_telemetry_heartbeat
    session_start_timestamp, session_id = await _fetch_or_set_telemetry_session(db=db)
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/services/telemetry.py", line 54, in _fetch_or_set_telemetry_session
    await configuration.write_configuration(session, telemetry_session)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/prefect/server/models/configuration.py", line 29, in write_configuration
    await session.flush()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1030, in flush
    await greenlet_spawn(self.sync_session.flush, objects=objects)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 212, in greenlet_spawn
    result = context.switch(value)
             ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4536, in flush
    self._flush(objects)
  File "<sqlalchemy generated warned() wrapper for sqlalchemy.orm.session.Session._flush>", line 2, in _flush
    return target(fn, self, objects=objects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4679, in _flush
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 166, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4640, in _flush
    flush_context.execute()
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 467, in execute
    rec.execute(self)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 643, in execute
    util.preloaded.orm_persistence._save_obj(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 92, in _save_obj
    _emit_insert_statements(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 1237, in _emit_insert_statements
    result = connection.execute(
             ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1458, in execute
    return meth(
           ^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/sql/elements.py", line 533, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1678, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1832, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1972, in _exec_single_context
    self._handle_dbapi_exception(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2342, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1953, in _exec_single_context
    self.dialect.do_execute(
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 1192, in do_execute
    cursor.execute(statement, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 258, in execute
    self._adapt_connection._handle_exception(error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 412, in _handle_exception
    self._handle_exception_no_connection(self.dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 237, in _handle_exception_no_connection
    super()._handle_exception_no_connection(dbapi, error)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 409, in _handle_exception_no_connection
    raise error.with_traceback(exc_info[2])
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 256, in execute
    return await_(self._execute_async(operation, parameters))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 167, in await_
    return current.parent.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/util/concurrency.py", line 205, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/sqlalchemy/connectors/asyncio.py", line 279, in _execute_async
    result = await self._cursor.execute(operation, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 40, in execute
    await self._execute(self._cursor.execute, sql, parameters)
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/cursor.py", line 32, in _execute
    return await self._conn._execute(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/venv/lib/python3.12/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
             ^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) database is locked
[SQL: INSERT INTO configuration ("key", value, id, created, updated) VALUES (:key, :value, :id, :created, :updated)]
[parameters: {'key': 'TELEMETRY_SESSION', 'value': '{"session_id": "2331354d-c9b5-4149-b00f-5e022e49a2a1", "session_start_timestamp": "2026-10-19T09:02:02.097147+00:00"}', 'id': 'eb097ea0-74e6-4c2e-a176-c360edbb45e6', 'created': '2026-10-19 09:02:02.098294', 'updated': '2026-10-19 09:02:02.098298'}]
(Background on this error at: https://sqlalche.me/e/21/e3q8)
19:32:02.364 | INFO    | Flow run 'blazing-hornet' - Beginning flow run 'blazing-hornet' for flow 'etl-web-to-lake'
19:32:02.365 | INFO    | Flow run 'blazing-hornet' - === ETL Flow: 2021-01 ===
19:32:02.374 | INFO    | Task run 'download_data-cea' - Finished in state Cached(type=COMPLETED)
19:32:02.472 | INFO    | Task run 'transform_data-339' - Loaded 1,369,769 rows from yellow_tripdata_2021-01.parquet
19:32:02.482 | INFO    | Task run 'transform_data-339' - Transformed: 1,369,769 rows ready for load
19:32:02.483 | INFO    | Task run 'transform_data-339' - Finished in state Completed()
19:32:03.070 | INFO    | Task run 'load_to_lake-bc2' - Wrote 1,369,769 rows to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/data_lake/yellow_taxi/2021/01/yellow_tripdata_2021-01.parquet
19:32:03.071 | INFO    | Task run 'load_to_lake-bc2' - Finished in state Completed()
19:32:03.071 | INFO    | Flow run 'blazing-hornet' - === Flow complete: 1,369,769 rows processed ===
19:32:03.375 | INFO    | Flow run 'blazing-hornet' - Finished in state Completed()
19:32:03.431 | INFO    | Flow run 'accelerated-quail' - Beginning flow run 'accelerated-quail' for flow 'etl-web-to-lake'
19:32:03.433 | INFO    | Flow run 'accelerated-quail' - === ETL Flow: 2021-02 ===
19:32:03.434 | INFO    | Task run 'download_data-0e6' - Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-02.parquet ...
19:32:06.924 | INFO    | Task run 'download_data-0e6' - Downloaded to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/downloads/yellow_tripdata_2021-02.parquet (20.77 MB)
19:32:06.929 | INFO    | Task run 'download_data-0e6' - Finished in state Completed()
19:32:06.990 | INFO    | Task run 'transform_data-529' - Loaded 1,371,709 rows from yellow_tripdata_2021-02.parquet
19:32:07.000 | INFO    | Task run 'transform_data-529' - Transformed: 1,371,709 rows ready for load
19:32:07.002 | INFO    | Task run 'transform_data-529' - Finished in state Completed()
19:32:07.590 | INFO    | Task run 'load_to_lake-ed3' - Wrote 1,371,709 rows to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/data_lake/yellow_taxi/2021/02/yellow_tripdata_2021-02.parquet
19:32:07.592 | INFO    | Task run 'load_to_lake-ed3' - Finished in state Completed()
19:32:07.592 | INFO    | Flow run 'accelerated-quail' - === Flow complete: 1,371,709 rows processed ===
19:32:08.459 | INFO    | Flow run 'accelerated-quail' - Finished in state Completed()
19:32:08.516 | INFO    | Flow run 'venomous-badger' - Beginning flow run 'venomous-badger' for flow 'etl-web-to-lake'
19:32:08.517 | INFO    | Flow run 'venomous-badger' - === ETL Flow: 2021-03 ===
19:32:08.519 | INFO    | Task run 'download_data-837' - Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-03.parquet ...
19:32:12.423 | INFO    | Task run 'download_data-837' - Downloaded to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/downloads/yellow_tripdata_2021-03.parquet (28.62 MB)
19:32:12.427 | INFO    | Task run 'download_data-837' - Finished in state Completed()
19:32:12.497 | INFO    | Task run 'transform_data-201' - Loaded 1,925,152 rows from yellow_tripdata_2021-03.parquet
19:32:12.509 | INFO    | Task run 'transform_data-201' - Transformed: 1,925,152 rows ready for load
19:32:12.510 | INFO    | Task run 'transform_data-201' - Finished in state Completed()
19:32:13.341 | INFO    | Task run 'load_to_lake-f84' - Wrote 1,925,152 rows to /Volumes/Rin T705 M2 Drive/GitHub/Data-Engineer-BootCamp-2024-Study/original/week2_workflow_orchestration/data_lake/yellow_taxi/2021/03/yellow_tripdata_2021-03.parquet
19:32:13.342 | INFO    | Task run 'load_to_lake-f84' - Finished in state Completed()
19:32:13.342 | INFO    | Flow run 'venomous-badger' - === Flow complete: 1,925,152 rows processed ===
19:32:13.538 | INFO    | Flow run 'venomous-badger' - Finished in state Completed()

============================================================
Backfilling: 2021-01
============================================================


============================================================
Backfilling: 2021-02
============================================================


============================================================
Backfilling: 2021-03
============================================================


============================================================
Backfill complete: 4,666,630 total rows processed across 3 months
============================================================

19:32:13.554 | INFO    | prefect - Stopping temporary server on http://127.0.0.1:8092

## Week 2 Homework - Green Taxi Q4 2020

**Date**: October 2026
**Dataset**: Green taxi Oct-Dec 2020
**Source**: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/

### Execution

```bash
python homework_green_taxi.py
```

### Results

**Question 1: Data Loading**
- Shape: 266,855 rows x 20 columns

**Question 2: Data Transformation (filtering)**
- Rows after passenger_count > 0 AND trip_distance > 0: 139,370

**Question 3: Data Transformation (date conversion)**
- Correct method: `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`

**Question 4: VendorID values**
- VendorID: 1 or 2

**Question 5: Snake case conversion**
- Columns needing rename: VendorID, RatecodeID, PULocationID, DOLocationID
- Count: 4

**Question 6: Partitions**
- Unique pickup dates: 96 partitions
