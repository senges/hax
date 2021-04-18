#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author : @Pdrooo
# Version : Apr. 2021
# Description : A CTF tools in docker manager
# =============================================================================

from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

import os
import json
import click
import docker
import dockerpty

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Tagging strategy will be improved very soon

images = {
    'legacy'    : 'pdrooo/hax:legacy',
    'hax'       : 'pdrooo/hax:latest',
    'minimal'   : 'pdrooo/hax:minimal',
    'expose'    : 'pdrooo/hax:expose',
    'msf'       : 'pdrooo/hax:msf',
    'cracking'  : 'pdrooo/hax:crack',
    'osint'     : 'pdrooo/hax:osint'
}

verbose = True

client = docker.from_env()
console = Console()

@click.group(invoke_without_command=True)
@click.help_option('-h', '--help')
# @click.option('-v', '--verbose', 'vflag', is_flag = True, help = 'Verbose mode')
@click.pass_context
def main(ctx=None, image=False, vflag=False):
    # verbose = vflag

    # If no parameter, just run the default container
    if ctx.invoked_subcommand is None:
        spawn('hax', False, ())

@main.command()
@click.help_option('-h', '--help')
@click.argument('name', required=False, default='hax', type=click.STRING)
@click.option('-p', '--pull',   is_flag=True,  help='Pull image if not present')
@click.option('-v', '--volume', is_flag=False, multiple=True, help='Additional volume in docker format')
def run(name, pull, volume):
    """Run ctf environment"""

    spawn(name, pull, volume)

@main.command()
@click.help_option('-h', '--help')
@click.argument('name', required=False, default='hax', type=click.Choice(list(images)))
def pull(name):
    """Pull image and exit"""

    dockerPull( images[name] )

@main.command('list')
@click.help_option('-h', '--help')
def xlist():
    """List local images"""

    table = Table(show_header=True, header_style="bold", box=box.SQUARE)
    table.add_column("Images")
    table.add_column("Size",  justify='right')
    table.add_column("State", justify='center')

    for i in images:
        if img := dockerStat(images[i]):
            table.add_row(i, '[i]' + dockerSize(img), '✓')
        else:
            table.add_row(i, '-', '✗ ')

    console.print(table)

@main.command()
@click.help_option('-h', '--help')
def refresh():
    """Pull latest version of local images"""

    for i in images:
        if dockerStat(images[i]):

            # Do not exit on program panic
            try: dockerPull(images[i])
            except: pass

@main.command(short_help = 'Expose TCP endpoint using ngrok')
@click.help_option('-h', '--help')
@click.argument('port', required = True, type = click.STRING)
@click.option('-p', '--pull', is_flag = True, help='Pull image if not present')
def expose(port, pull):
    """
    Expose TCP endpoint using ngrok

    PORT is the local port you want to expose
    """

    spawn ( 
        name    = 'expose', 
        pull    = pull, 
        volumes = (), 
        env     = [ 'NGROK_PORT=' + port ]
    )

@main.command()
@click.help_option('-h', '--help')
@click.confirmation_option(prompt = 'Any configuration will be stored plaintext on disk. Continue ?')
@click.option('--ngrok_token', prompt=True, default=lambda: getConfig('ngrok_token'))
def config(ngrok_token):
    """Configure hax"""
    
    env = []
    volumes = []

    config_folder = os.environ.get('HOME') + '/.hax'

    # Ask for custom additional volumes
    console.print('[yellow]Additional volumes (one per line, docker format)')
    while v := click.prompt('Volume ' + str(len(volumes) + 1), default=False, show_default=False, type=str):
        volumes.append(v)

    # Ask for custom additional en vars
    console.print('[yellow]Additional environment variables (one per line, `NAME=val` format)')
    while e := click.prompt('Var ' + str(len(env) + 1), default=False, show_default=False, type=str):
        env.append(e)

    try:
        Path(config_folder).mkdir(exist_ok = True)

    except FileNotFoundError:
        panic( 'Parent directory must exist' )
    
    with open(os.path.join(config_folder, 'config.json'), 'w+') as f:
        config = {
            'ngrok_token' : ngrok_token,
            'volumes'     : volumes,
            'env'         : env
        }

        json.dump(config, f, indent = 4)

    success('Config file updated !')

@main.command()
@click.help_option('-h', '--help')
def wordlist():
    """Manage wordlists"""

    panic('Not yet implemented')

@main.command()
@click.help_option('-h', '--help')
def build():
    """Build images from source"""

    panic('Not yet implemented')

# Spawn new docker environment
def spawn(name: str, pull: bool = False, volumes: tuple = (), env: list = []):

    if images.get(name):
        image = images[name]    # If builtin image
    else:
        image = name            # Else it's custom image

    # Pull if required
    if pull:
        dockerPull(image)

    # Generate volumes between host and docker
    volumes = dockerVolumes(volumes)

    # Generate environment variables to expose in docker
    env = dockerEnv(env)
    
    # Run image
    dockerRun(image, volumes, env)

# Check if local image is present
def dockerStat(name: str):
    try:
        img = client.images.get(name)

    except docker.errors.ImageNotFound:
        return False

    except docker.errors.APIError:
        panic('Could not connect to docker socket')

    return img

# Docker env list generation
def dockerEnv(env: list = []):
    env.append( 'NGROK_TOK=' + getConfig('ngrok_token') )

    # Add env from config file if any
    if custom := getConfig('env'):
        env += custom

    return env

# Docker volume list generation
def dockerVolumes(userVolumes: tuple = ()) -> dict:
    volumes = {
        '/tmp': {'bind': '/tmp', 'mode': 'rw'},
    }

    # If current user has ssh, share read only
    ssh = '%s/.ssh' % os.environ.get('HOME')

    if os.path.isdir(ssh):
        volumes[ssh] = {'bind': '/root/.ssh', 'mode': 'ro'}

    # Add volumes from config file if any
    userVolumes += tuple(getConfig('volumes'))

    # Add user custom volume if any
    for v in userVolumes:
        try:
            chunk = v.split(':')

            if len(chunk) < 2:
                raise ValueError( f'Missing parts in volume declaration `{ v }`' )

            # Default mount strategie is read/write
            if len(chunk) == 2:
                chunk.append('rw')

            # Not sure if necessary as docker does not enforce
            # local path stat.
            if not os.path.isdir(chunk[0]):
                raise ValueError(f'Local path `{ chunk[0] }` does not exist')

            # Make sure rwx rights are properly set
            if chunk[2] not in ['ro', 'rw']:
                raise ValueError('Volume rights must be one of : [ro, rw]')

            volumes[chunk[0]] = {'bind': chunk[1], 'mode': chunk[2]}

        except ValueError as err:
            panic(err.args[0])

        except:
            panic(f'Invalid volume format `{ v }`')

    return volumes

# Pull docker image
def dockerPull(name: str):

    info(f'Pulling image { name } from registry')

    try:
        with console.status("[bold grey]Pulling ..."):
            client.images.pull( name )

    except docker.errors.APIError:
        panic(f'Could not pull image { name }')

    success(f'Image { name } pull done')

# Start container
def dockerRun(name: str, volumes: dict = {}, env: list = []):

    if not dockerStat(name):
        panic(f'Image { name } not found locally. Use `pull` command or add `--pull` flag.')

    container = client.containers.create(
        image        = name,
        auto_remove  = True,
        hostname     = 'hax',
        stdin_open   = True,
        tty          = True,
        network_mode = 'host',
        volumes      = volumes,
        environment  = env,
    )

    dockerpty.start(client.api, container.id)

# Return docker image size
def dockerSize(image: docker.models.images.Image) -> str:
    size = int(image.attrs['Size'])

    # Remove top layer size if not legacy image
    if images['legacy'] not in image.tags:
        if legacy := dockerStat( images['legacy'] ):
            size -= int(legacy.attrs['Size'])

    return prettySize(size)

# Get key from config file
def getConfig(key: str):
    try:
        with open(os.environ.get('HOME') + '/.hax/config.json') as f:
            value = json.load(f).get(key)
    except:
        value = None

    return value

# Program panic
def panic(err: str):
    console.print('[red]✗ ' + err)
    exit(EXIT_FAILURE)

# Display cli info
def info(msg: str):
    if verbose:
        console.print('[yellow]~ ' + msg)

# Display cli info
def success(msg: str):
    if verbose:
        console.print('[green]✓ ' + msg)

# Pretty print bytes
def prettySize(bytes, units=['', 'KO', 'Mo', 'Go', 'To']):
    return str(bytes) + ' ' + units[0] if bytes < 1024 else prettySize(bytes >> 10, units[1:])

if __name__ == '__main__':
    main()
