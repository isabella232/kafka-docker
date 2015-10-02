[![Docker Repository on Quay.io](https://quay.io/repository/plivo/kafka/status "Docker Repository on Quay.io")](https://quay.io/repository/plivo/kafka)

# Kafka in a Docker Container #

## Environment Variables ##

The following variables control the configuration of the kafka process
in the container:

**ZOOKEEPER_BASE** - Base path in zookeeper for all kafka data (required parameter).
**ZOOKEEPER_NODE_LIST** - List of Zookeeper node IPs separated by a comma (required parameter).
**BROKER_ID** - Unique integer
**HOST_IP** - Host IP address
**NUM_PARTITIONS** - Default number of partitions (8 by default)
**RETENTION_HOURS** - Default retention is 7 days
**RETENTION_BYTES** - Default retention is based only on time
**LOG_SEGMENT_BYTES** - Size of each log segment
**LOG_ROLL_HOURS** - Interval between rolling new segments (1 week default)

Disk flush settings:
**FLUSH_INTERVAL_MS** - default 10000
**FLUSH_INTERVAL_MSGS** - default 10000

**NUM_THREADS** - IO threads
**NUM_REPLICA_FETCHERS** - Number of recovery threads
**REPLICA_SOCKET_TIMEOUT_MS** - default 2500
**REPLICA_LAG_MAX_MS** - default 5000
**REPLICA_LAG_MAX_MSGS** - default 1000
**AUTO_LEADER_REBALANCE** - default False

## Volumes ##

The following volumes may be mounted on the host if desired (with no
existing data on first startup):

* `/kafka` - Kafka Log storage directory
* `/var/log/kafka` - Kafka application log messages
