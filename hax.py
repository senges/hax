#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author : @Pdrooo
# Version : Apr. 2021
# Description : A CTF tools in docker manager
# =============================================================================

from rich.console import Console
from rich.table import Table
from rich import box

import os
import click
import docker
import dockerpty

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

images = {
    'legacy'    : 'hax',
    'msf'       : 'hax-msf',
    'minimal'   : 'hax-minimal',
    'hashcat'   : 'hax-hashcat',
}

verbose = True

client = docker.from_env()
console = Console()

@click.group(invoke_without_command = True)
@click.help_option('-h', '--help')
# @click.option('-v', '--verbose', 'vflag', is_flag = True, help = 'Verbose mode')
@click.pass_context
def main(ctx = None, image = False, vflag = False):
    # verbose = vflag

    # If no parameter, just run the legacy container
    if ctx.invoked_subcommand is None:
        spawn( 'legacy', False, () )

@main.command()
@click.help_option('-h', '--help')
@click.argument('name', required = False, default = 'legacy', type = click.STRING)
@click.option('-p', '--pull',   is_flag = True,  help = 'Pull image if not present')
@click.option('-v', '--volume', is_flag = False, multiple = True, help = 'Additional volume in docker format')
def run(name, pull, volume):
    """Run ctf environment"""
    
    spawn( name, pull, volume )

@main.command()
@click.help_option('-h', '--help')
@click.argument('name', required = False, default = 'legacy', type = click.Choice( list(images) ))
def pull(name):
    """Pull image and exit"""
    
    dockerPull( name )

@main.command()
@click.help_option('-h', '--help')
def list():
    """List local images"""

    table = Table( show_header = True, header_style = "bold", box = box.SQUARE )
    table.add_column("Images")
    table.add_column("Size",  justify='right')
    table.add_column("State", justify='center')

    for i in images:
        if img := dockerStat( images[i] ):
            table.add_row(i, '[i]' + dockerSize(img), '✓')
        else:
            table.add_row(i, '-', '✗ ')

    console.print(table)

@main.command()
@click.help_option('-h', '--help')
def refresh():
    """Pull latest version of local images"""

    for i in images:
        if dockerStat( images[i] ):
            try: dockerPull( images[i] )
            except: pass

@main.command()
@click.help_option('-h', '--help')
def wordlist():
    """Manage wordlists"""

    panic( 'Not yet implemented' )

@main.command()
@click.help_option('-h', '--help')
def build():
    """Build images from source"""

    panic( 'Not yet implemented' )

# Spawn new docker environment
def spawn(name: str, pull: bool = False, volume: tuple = ()):

    # Pull if required
    if pull: dockerPull( images[name] )

    # Generate volumes between host and docker
    volumes = dockerVolumes(volume)

    # Run image
    dockerRun(images[name], volumes)

# Check if local image is present
def dockerStat(name: str):
    try:
        img = client.images.get( name )

    except docker.errors.ImageNotFound:
        return False

    except docker.errors.APIError:
        panic( 'Could not connect to docker socket' )

    return img

# Docker volume list generation
def dockerVolumes(userVolumes: tuple = ()) -> dict:
    volumes = {
        '/tmp' : { 'bind' : '/tmp', 'mode' : 'rw' },
    }

    # If current user has ssh, share read only
    ssh = '%s/.ssh' % os.environ.get('HOME')

    if os.path.isdir(ssh):
        volumes[ ssh ] = { 'bind' : '/root/.ssh', 'mode' : 'ro' }

    # Add user custom volume if any
    for v in userVolumes:
        try:
            chunk = v.split(':')

            if len(chunk) < 2:
                raise ValueError('Missing parts in volume declaration')
            
            # Default mount strategie is read/write
            if len(chunk) == 2:
                chunk.append('rw')

            # Not sure if necessary as docker does not enforce
            # local path stat.
            if not os.path.isdir( chunk[0] ):
                raise ValueError( f'Path { chunk[0] } does not exist' )

            # Make sure rwx rights are properly set
            if chunk[2] not in ['ro', 'rw']:
                raise ValueError( 'Volume rights must be one of : [ro, rw]')

            volumes[ chunk[0] ] = { 'bind' : chunk[1], 'mode' : chunk[2] }
            
        except ValueError as err:
            panic( err.args[0] )

        except:
            panic( f'Invalid volume format `{ v }`' )

    return volumes

# Pull docker image
def dockerPull(name: str):

    info ( f'Pulling image { name } from registry' )

    try:
        with console.status("[bold grey]Pulling ..."):
            client.images.pull( name, 'latest' )

    except docker.errors.APIError:
        panic( f'Could not pull image { name }' )

    success( f'Image { name } pull done' )

# Start container
def dockerRun(name: str, volumes: dict = {}):

    if not dockerStat( name ):
        panic( f'Image { name } not found locally. Use `pull` command or add `--pull` flag.' )

    container = client.containers.create(
        image           = '%s:latest' % name,
        auto_remove     = True,
        hostname        = 'hax',
        stdin_open      = True,
        tty             = True,
        volumes         = volumes
    )

    dockerpty.start(client.api, container.id)

# Return docker image size
def dockerSize(image: str) -> str:
    return prettySize( image.attrs['Size'] )

# Program panic
def panic(err: str):
    console.print('[red]✗ ' + err)
    exit( EXIT_FAILURE )

# Display cli info
def info(msg: str):
    if verbose: console.print('[yellow]~ ' + msg)

# Display cli info
def success(msg: str):
    if verbose: console.print('[green]✓ ' + msg)

# Pretty print bytes
def prettySize(bytes, units=[ '','KO','Mo','Go','To' ]):
    return str(bytes) + ' ' + units[0] if bytes < 1024 else prettySize( bytes>>10, units[1:] )

if __name__ == '__main__':
    main()