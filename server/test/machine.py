#!/usr/bin/env python
import zmq
import json
import time
from time import sleep
from math import sin, radians, fabs

def create_producer(host):
    context = zmq.Context()
    producer = context.socket(zmq.PUSH)
    producer.connect(host)
    return producer


def create_message(message_name, payload):
    return '{} {}'.format(message_name, json.dumps(
        {'machine_id': 4567, 'machine_type': 'M81', 'timestamp': time.time(), 'rfid': '0x1234567',
         'payload': payload}))


def create_login_payload():
    return {'gender': 'Male', 'goal': 'FITNESS', 'height': 182, 'intensity': 'MEDIUM', 'first_name': 'Shawn'}


def create_start_training_payload():
    return {'training_method': 'regular', 'training_weight_concentric': 50, 'training_weight_excentric': 70,
            'number_of_repetitions': 8}


def create_end_training_payload():
    return {'moved_weight': 480}


def create_end_strength_measurement_payload():
    return {'weight': 275}


def create_training_position_data_payload(position):
    return {'position': position}


def create_training_weight_data_payload():
    return {'weight': 65}


def create_training_direction_data_payload():
    return {'direction': 'concentric'}


def create_training_repetition_data_payload():
    return {'repetition': 3}


def create_empty_payload():
    return None


def create_login_message():
    return create_message('login', create_login_payload())


def create_logout_message():
    return create_message('logout', create_empty_payload())


def create_trainer_needed_message():
    return create_message('trainer_needed', create_empty_payload())


def create_start_training_message():
    return create_message('start_training', create_start_training_payload())


def create_end_training_message():
    return create_message('end_training', create_end_training_payload())


def create_start_strength_measurement_message():
    return create_message('start_strength_measurement', create_empty_payload())


def create_end_strength_measurement_message():
    return create_message('end_strength_measurement', create_end_strength_measurement_payload())


def create_training_position_data_message(position):
    return create_message('training_position_data', create_training_position_data_payload(position))


def create_training_weight_data_message():
    return create_message('training_weight_data', create_training_weight_data_payload())


def create_training_direction_data_message():
    return create_message('training_direction_data', create_training_direction_data_payload())


def create_training_repetition_data_message():
    return create_message('training_repetition_data', create_training_repetition_data_payload())


def send_fake_machine_training_flow(producer):
    producer.send(create_login_message())
    producer.send(create_start_training_message())

    for i in range(0, 720, 5):
        producer.send(create_training_position_data_message(fabs(sin(radians(i)))))
        producer.send(create_training_weight_data_message())
        sleep(0.1)
    producer.send(create_training_direction_data_message())
    producer.send(create_training_repetition_data_message())
    producer.send(create_end_training_message())
    producer.send(create_logout_message())


def send_fake_machine_strength_measurment_flow(producer):
    producer.send(create_login_message())
    producer.send(create_start_strength_measurement_message())
    producer.send(create_end_strength_measurement_message())
    producer.send(create_logout_message())


producer = create_producer("tcp://35.195.199.160:5557")
send_fake_machine_training_flow(producer)
send_fake_machine_strength_measurment_flow(producer)
