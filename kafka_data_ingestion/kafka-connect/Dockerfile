FROM confluentinc/cp-kafka-connect-base:7.6.0

RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:15.1.4 \
    && confluent-hub install --no-prompt debezium/debezium-connector-postgresql:2.5.4