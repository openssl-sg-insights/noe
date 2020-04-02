import os
import datetime as dt

import boto3
from fabric.api import task, lcd, local, run


@task
def build_frontend():
    local('docker run -n temp-project-noe-frontend')
    local('docker exec temp-project-noe-frontend bash -c "yarn build"')
    local('docker cp temp-project-noe-frontend:/project-noe/frontend/build temp/build')
    local('docker rm -f temp-project-noe-frontend')


@task
def deploy_frontend():
    local('aws s3 sync temp/build s3://noe.rollet.app')

    client = boto3.client('cloudfront')
    items_to_invalidate = [
        '/',
        '/static/css/styles.sass',
        '/index.html',
        '/favicon.ico',
        '/manifest.json',
        '/app-icon.png',
    ]
    for distribution_id in os.environ.get('AWS_CLOUDFRONT_DISTRIBUTION_IDS', '').split(','):
        client.create_invalidation(
            DistributionId=distribution_id.strip(),
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(items_to_invalidate),
                    'Items': items_to_invalidate
                },
                'CallerReference': dt.datetime.now().strftime('%Y%m%d%H%M%S')
            }
    )
