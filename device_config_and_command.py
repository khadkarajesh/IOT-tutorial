import datetime
import jwt
import sys
import argparse
import time
import paho.mqtt.client as mqtt
# project_id = iot-practice-223905


def create_jwt(project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }

    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    print(jwt.encode(token, private_key, algorithm=algorithm))

    return jwt.encode(token, private_key, algorithm=algorithm)


def parse_command_line_args():
    parser = argparse.ArgumentParser(description='Process project parameters')
    parser.add_argument("--project_id",
                        required=True)
    parser.add_argument("--private_key_file",
                        required=True)
    parser.add_argument(
        "--algorithm",
        choices=('RS256', 'ES256'),
        required=True)
    parser.add_argument(
        '--mqtt_bridge_hostname',
        default='mqtt.googleapis.com',
        help='MQTT bridge hostname.')
    parser.add_argument(
        '--mqtt_bridge_port',
        choices=(8883, 443),
        default=8883,
        type=int,
        help='MQTT bridge port.')
    parser.add_argument(
        '--ca_certs',
        default='roots.pem',
        help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument('--cloud_region',
                        choices=('us-central1', 'europe-west1', 'asia-east1'),
                        default='us-central1',
                        type=str,
                        help='Your preferred region')
    parser.add_argument('--registry_id', required=True)
    parser.add_argument('--device_id', required=True)
    return parser.parse_args()


def on_connect(client, userdata, flags, rc):
    print("connected")


def on_disconnect(client, userdata, flags, rc):
    print("on dis-connected")


def on_message(client, userdata, message):
    print(message.payload)


def on_subscribe(client, userdata, flags, rc):
    print("on subscribe")


def on_publish(client, userdata, flags, rc):
    print("on publish")


def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):

    client = mqtt.Client(client_id=('projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id, cloud_region, registry_id, device_id)))
    client.username_pw_set(username='unused', password=create_jwt(
        project_id, private_key_file, algorithm))

    client.tls_set(ca_certs=ca_certs)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    return client

def subscribe_config(client, device_id):
    #subscribe to get device config
    mqtt_config = '/devices/{}/config'.format(device_id)
    client.subscribe(mqtt_config)

def subscribe_command(client, device_id):
    #subscribe to get device commands
    mqtt_command = '/devices/{}/commands/#'.format(device_id)
    client.subscribe(mqtt_command)


if __name__ == "__main__":
    args = parse_command_line_args()
    client = get_client(args.project_id,
                        args.cloud_region,
                        args.registry_id,
                        args.device_id,
                        args.private_key_file,
                        args.algorithm,
                        args.ca_certs,
                        args.mqtt_bridge_hostname,
                        args.mqtt_bridge_port)
    subscribe_command(client, args.device_id)
    subscribe_config(client, args.device_id)
    client.loop_forever()
    
