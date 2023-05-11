-- Table datanode stores the different data nodes. Each data node represents a sensor or data source
CREATE TABLE datanode(
    -- unique identifier of the data node
    id varchar(255) not null
        constraint PK_DataNode
            primary key,
    description varchar(255)
);

-- measurement values with the values of the measurement readings
CREATE TABLE measurement_value (
    id BIGSERIAL,
    start TIMESTAMPTZ NOT NULL,
    end TIMESTAMPTZ NOT NULL,
    node_id varchar(255) NOT NULL REFERENCES datanode(ID),
    value DOUBLE PRECISION NOT NULL
);

-- create hypertable to optimize queries
SELECT create_hypertable('measurement_value', 'end', chunk_time_interval => INTERVAL '1 day');

-- create index tu support efficient queries on time and nodeId
CREATE INDEX IX_NodeId_time ON measurement_value (node_id, end DESC);

-- Create materialized view to summarize data by minute
CREATE MATERIALIZED VIEW measurements_summary_minute
WITH (timescaledb.continuous) AS
SELECT node_id,
       time_bucket(INTERVAL '1 minute', end_time) AS measurement_bucket,
       AVG(value) as average,
       MAX(value) as max,
       MIN(value) as min
FROM measurement_value
GROUP BY node_id, measurement_bucket;


SELECT add_continuous_aggregate_policy('measurements_summary_minute',
  start_offset => INTERVAL '1 month',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 hour');

CREATE MATERIALIZED VIEW measurements_summary_quarter_hour
WITH (timescaledb.continuous) AS
SELECT node_id,
       time_bucket(INTERVAL '15 minutes', end_time) AS measurement_bucket,
       AVG(value) as average,
       MAX(value) as max,
       MIN(value) as min
FROM measurement_value
GROUP BY node_id, measurement_bucket;


SELECT add_continuous_aggregate_policy('measurements_summary_quarter_hour',
  start_offset => INTERVAL '1 month',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 hour');
