from confluent_kafka import Producer
import json
import random
import uuid
import time
import os
from datetime import datetime

BOOTSTRAP=os.getenv(
    "BOOTSTRAP_SERVERS",
    "prod-kafka-kafka-internal-bootstrap:9092"
)

producer = Producer({
    'bootstrap.servers': BOOTSTRAP,
    'compression.type': 'snappy',
    'acks': 'all',
    'enable.idempotence': True
})

MSISDN_PREFIX="91"

def msisdn():
    return f"{MSISDN_PREFIX}{random.randint(7000000000,9999999999)}"

def send(topic,payload):
    producer.produce(topic,json.dumps(payload).encode())
    producer.poll(0)

count=0

while True:

    ts=datetime.utcnow().isoformat()

    send("telecom.cdr",{
        "cdrId":str(uuid.uuid4()),
        "msisdn":msisdn(),
        "duration":random.randint(1,500),
        "cellId":f"CELL-{random.randint(1,1000)}",
        "timestamp":ts
    })

    send("telecom.billing",{
        "txnId":str(uuid.uuid4()),
        "amount":round(random.uniform(1,500),2),
        "currency":"INR",
        "timestamp":ts
    })

    send("telecom.network",{
        "alarmId":str(uuid.uuid4()),
        "severity":random.choice(
            ["INFO","WARN","CRITICAL"]
        ),
        "node":f"NODE-{random.randint(1,100)}",
        "timestamp":ts
    })

    send("telecom.recharge",{
        "rechargeId":str(uuid.uuid4()),
        "amount":random.choice(
            [10,20,50,100,500]
        ),
        "timestamp":ts
    })

    send("telecom.customer",{
        "customerId":str(uuid.uuid4()),
        "action":random.choice(
            ["LOGIN","LOGOUT","PROFILE_UPDATE"]
        ),
        "timestamp":ts
    })

    count += 5

    if count % 10000 == 0:
        print(f"Generated {count} events")

    if count >= 1000000:
        producer.flush()
        break

producer.flush()
print("Completed 1 Million Events")
