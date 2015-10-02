#!/usr/bin/env python

import os
# import sys

kafka_config_file = '/opt/kafka/config/server.properties'
kafka_log_config_file = '/opt/kafka/config/log4j.properties'

zk_nodes = os.environ['ZOOKEEPER_NODE_LIST'].split(',')

kafka_config_template = """# Kafka configuration
broker.id=%(broker_id)d
advertised.host.name=%(host_address)s
port=%(broker_port)d

num.network.threads=%(num_threads)d
num.io.threads=%(num_threads)d

socket.send.buffer.bytes=1048576
socket.receive.buffer.bytes=1048576
socket.request.max.bytes=104857600

log.dirs=%(log_dirs)s
num.partitions=%(num_partitions)d

log.flush.interval.messages=%(flush_interval_msgs)s
log.flush.interval.ms=%(flush_interval_ms)d
log.retention.hours=%(retention_hours)d
log.retention.bytes=%(retention_bytes)d
log.segment.bytes=%(log_segment_bytes)d
log.roll.hours=%(log_roll_hours)d
log.cleanup.interval.mins=1

default.replication.factor=%(replication_factor)d
num.replica.fetchers=%(num_replica_fetchers)d
replica.fetch.max.bytes=1048576
replica.fetch.wait.max.ms=500
replica.high.watermark.checkpoint.interval.ms=5000
replica.socket.timeout.ms=%(replica_socket_timeout_ms)d
replica.socket.receive.buffer.bytes=65536

replica.lag.time.max.ms=%(replica_lag_max_ms)d
replica.lag.max.messages=%(replica_lag_max_msgs)d

auto.leader.rebalance.enable=%(leader_rebalance)s
controlled.shutdown.enable=true

zookeeper.connect=%(zookeeper_nodes)s%(zookeeper_base)s
zookeeper.connection.timeout.ms=6000
zookeeper.session.timeout.ms=6000
zookeeper.sync.time.ms=2000

kafka.metrics.polling.interval.secs=5
kafka.metrics.reporters=kafka.metrics.KafkaCSVMetricsReporter
kafka.csv.metrics.dir=/var/lib/kafka/metrics/
kafka.csv.metrics.reporter.enabled=false
"""

kafka_logging_template = """# Log4j configuration, logs to rotating file
log4j.rootLogger=INFO,R

log4j.appender.R=org.apache.log4j.RollingFileAppender
log4j.appender.R.File=/var/log/kafka/kafka.log
log4j.appender.R.MaxFileSize=100MB
log4j.appender.R.MaxBackupIndex=10
log4j.appender.R.layout=org.apache.log4j.PatternLayout
log4j.appender.R.layout.ConversionPattern=%(log_pattern)s
"""

log_pattern = "%d{yyyy'-'MM'-'dd'T'HH:mm:ss.SSSXXX} %-5p [%-35.35t] [%-36.36c]: %m%n"

replication = min(int(os.environ.get('REPLICATION', 2)), len(zk_nodes))

config_model = {
    'broker_id': int(os.environ.get('BROKER_ID', 0)),
    'host_address': os.environ['HOST_IP'],
    'broker_port': 9092,
    'log_dirs': '/kafka',
    'num_partitions': int(os.environ.get('NUM_PARTITIONS', 8)),
    # Default retention is 7 days (168 hours).
    'retention_hours': int(os.environ.get('RETENTION_HOURS', 168)),
    # Default retention is only based on time.
    'retention_bytes': int(os.environ.get('RETENTION_BYTES', -1)),
    # Segment size (default is 1GB)
    'log_segment_bytes': int(os.environ.get('LOG_SEGMENT_BYTES', 1073741824)),
    # Minimum interval between rolling new log segments (default 1 week)
    'log_roll_hours': int(os.environ.get('LOG_ROLL_HOURS', 24 * 7)),
    'zookeeper_nodes': ",".join(map(lambda x: "{}:2181".format(x), zk_nodes)),
    'zookeeper_base': os.environ.get('ZOOKEEPER_BASE'),
    'flush_interval_ms': int(os.environ.get('FLUSH_INTERVAL_MS', 10000)),
    'flush_interval_msgs': int(os.environ.get('FLUSH_INTERVAL_MSGS', 10000)),
    'num_threads': int(os.environ.get('NUM_THREADS', 8)),
    'replication_factor': replication,
    'num_replica_fetchers': int(os.environ.get('NUM_REPLICA_FETCHERS', 4)),
    'replica_socket_timeout_ms': int(os.environ.get('REPLICA_SOCKET_TIMEOUT_MS', 2500)),
    'replica_lag_max_ms': int(os.environ.get('REPLICA_LAG_MAX_MS', 5000)),
    'replica_lag_max_msgs': int(os.environ.get('REPLICA_LAG_MAX_MSGS', 1000)),
    'leader_rebalance': str(os.environ.get('AUTO_LEADER_REBALANCE', 'false').lower() == 'true').lower()
}

with open(kafka_config_file, "w+") as f:
    f.write(kafka_config_template % config_model)

with open(kafka_log_config_file, 'w+') as f:
    f.write(kafka_logging_template % {'log_pattern': log_pattern})

os.environ['KAFKA_OPTS'] = os.environ.get('JVM_OPTS', '')

# start Kafka
os.execl('/opt/kafka/bin/kafka-server-start.sh', 'kafka', kafka_config_file)
