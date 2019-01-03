import argparse
import json
import os
from google.cloud import pubsub_v1

# TODO Path to google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "key.json"

def publish_messages(project_id, topic_name):
    project_id = project_id
    topic_name = topic_name

    publisher = pubsub_v1.PublisherClient()
    '''The `topic_path` method creates a fully qualified identifier
    in the form `projects/{project_id}/topics/{topic_name}` '''
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(0, 3):
        data = json.dumps({'temperature': n})
        future = publisher.publish(topic_path, data=data)
        print('Published {} of message ID {}.'.format(data, future.result()))

    print('Published messages.')


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Example Google Cloud IoT MQTT device connection code.')
    parser.add_argument(
        '--project_id',
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        required=True,
        help='GCP cloud project name.')
    parser.add_argument(
        '--topic_name', required=True, help='Cloud IoT Topic name')
    return parser.parse_args()


def main():
    args = parse_command_line_args()
    publish_messages(args.project_id, args.topic_name)
    

if __name__ == '__main__':
    main()