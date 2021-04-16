#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author : @Pdrooo
# Version : Apr. 2021
# Description : A CTF tools in docker manager
# =============================================================================

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

client = docker.from_env()

@click.group(invoke_without_command = True)
@click.help_option('-h', '--help')
@click.option('-i', '--list-images', 'image', is_flag = True, help = 'List local images')
@click.pass_context
def main(ctx = None, image = False):

    # If no parameter, just run the legacy container
    if ctx.invoked_subcommand is None:
        start()

@main.command()
@click.help_option('-h', '--help')
@click.option('-p', '--pull',   is_flag = True,  help = 'Allow image pull to local registry')
@click.option('-v', '--volume', is_flag = False, multiple = True, help = 'Additional volume in docker format')
def start(pull = False, volume = ()):
    """Start general purpose box (same as no command)"""
    
    run( 'hax', '/bin/zsh', pull, volume )

@main.command()
@click.help_option('-h', '--help')
@click.option('-p', '--pull',   is_flag = True,  help = 'Allow image pull to local registry')
@click.option('-v', '--volume', is_flag = False, multiple = True, help = 'Additional volume in docker format')
def msf(pull = False, volume = ()):
    """Start metasploit msfconsole"""

    run( 'msf', '/usr/bin/msfconsole', pull, volume )

@main.command()
@click.help_option('-h', '--help')
@click.option('-p', '--pull',   is_flag = True,  help = 'Allow image pull to local registry')
@click.option('-v', '--volume', is_flag = False, multiple = True, help = 'Additional volume in docker format')
def hashcat(pull = False, volume = ()):
    """Start hashcat environment"""

    run( 'hashcat', '/usr/bin/hashcat', pull, volume )

@main.command()
@click.help_option('-h', '--help')
@click.option('-l', '--list', 'xlist', is_flag = True, help = 'List available images')
@click.argument('name', required = False, type = click.Choice( list(images) ))
def pull(name, xlist):
    """Pull image and exit"""

    if xlist:
        print( 'Available images :' )
        print( '\n'.join(['> ' + x for x in images]) )
        exit( EXIT_SUCCESS )

    if not name:
        dockerPull('legacy')
        return
    
    dockerPull( name )

# Run app lifecycle
def run(image: str, entrypoint: str, pull: bool = False, volume: tuple = ()):

    # Pull if required
    if pull: dockerPull( image )

    # Generate volumes between host and docker
    volumes = dockerVolumes(volume)

    # Run image
    dockerRun(image, entrypoint, volumes)

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

    info ( f'Pulling image { name } ...' )

    try:
        client.images.pull( images[name], 'latest' )

    except docker.errors.APIError:
        panic( f'Could not pull image { name }' )

    success( f'Image { name } pull done' )

# Start container
def dockerRun(name: str, entrypoint: str, volumes: dict = {}):
    try:
        client.images.get( name )

    except docker.errors.ImageNotFound:
        panic( f'Image { name } not found locally. Use `pull` command or add `--pull` flag.' )

    except docker.errors.APIError:
        panic( 'Could not connect to docker socket' )

    container = client.containers.create(
        image           = '%s:latest' % name,
        auto_remove     = True,
        hostname        = 'hax',
        stdin_open      = True,
        tty             = True,
        volumes         = volumes,
        command         = entrypoint
    )

    dockerpty.start(client.api, container.id)

# Program panic
def panic(err: str):
    print('[-] ' + err)
    exit( EXIT_FAILURE )

# Display cli info
def info(msg: str):
    print('[~] ' + msg)

# Display cli info
def success(msg: str):
    print('[+] ' + msg)

if __name__ == '__main__':
    main()
    