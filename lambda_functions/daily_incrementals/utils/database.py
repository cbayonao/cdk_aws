#!/usr/bin/env python3

import sshtunnel
from os import getenv
from sqlalchemy import URL, create_engine

SSH_TUNNEL_USERNAME = getenv('SSH_TUNNEL_USERNAME')
SSH_TUNNEL_KEY_PATH = getenv('SSH_TUNNEL_KEY_PATH')
SSH_TUNNEL_HOST = getenv('SSH_TUNNEL_HOST')
SSH_TUNNEL_PORT = getenv('SSH_TUNNEL_PORT')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_USER = getenv('DB_USER')
DB_PWD = getenv('DB_PWD')
DB_NAME = getenv('DB_NAME')


STR_CONNECTION = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@localhost:1234/{DB_NAME}'



def connect_DB_through_sshtunnel_orm() -> None:
    """
    Create conection with ssh tunnel.

    :returns: sqlalchemy engine and sshtunnel
    :raises Exception: raises a simple exception
    """
    ssh_tunnel = None
    try:
        print('Connecting to the PostgreSQL Database...')
        ssh_tunnel = sshtunnel.SSHTunnelForwarder(
                (SSH_TUNNEL_HOST, int(SSH_TUNNEL_PORT)),
                ssh_username=SSH_TUNNEL_USERNAME,
                ssh_private_key=SSH_TUNNEL_KEY_PATH,
                remote_bind_address=(DB_HOST, int(DB_PORT)),
                local_bind_address=("localhost", 1234)
            )
        ssh_tunnel.start()
        
    except Exception as err:
        print('Connection Has Failed...', err)
        ssh_tunnel = None
    return ssh_tunnel


tunnel = connect_DB_through_sshtunnel_orm()

engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')

