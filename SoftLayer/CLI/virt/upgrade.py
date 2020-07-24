"""Upgrade a virtual server."""
# :license: MIT, see LICENSE for more details.

import json

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import exceptions
from SoftLayer.CLI import formatting
from SoftLayer.CLI import helpers
from SoftLayer.CLI import virt


@click.command(epilog="""Note: SoftLayer automatically reboots the VS once
upgrade request is placed. The VS is halted until the Upgrade transaction is
completed. However for Network, no reboot is required.""")
@click.argument('identifier')
@click.option('--cpu', type=click.INT, help="Number of CPU cores")
@click.option('--private', is_flag=True,
              help="CPU core will be on a dedicated host server.")
@click.option('--memory', type=virt.MEM_TYPE, help="Memory in megabytes")
@click.option('--network', type=click.INT, help="Network port speed in Mbps")
@click.option('--add', type=click.INT, required=False, help="add Hard disk in GB")
@click.option('--disk', nargs=1, help="update the number and capacity in GB Hard disk, E.G {'number':2,'capacity':100}")
@click.option('--flavor', type=click.STRING,
              help="Flavor keyName\nDo not use --memory, --cpu or --private, if you are using flavors")
@environment.pass_env
def cli(env, identifier, cpu, private, memory, network, flavor, disk, add):
    """Upgrade a virtual server."""

    vsi = SoftLayer.VSManager(env.client)

    if not any([cpu, memory, network, flavor, disk, add]):
        raise exceptions.ArgumentError("Must provide [--cpu], [--memory], [--network], or [--flavor] to upgrade")

    if private and not cpu:
        raise exceptions.ArgumentError("Must specify [--cpu] when using [--private]")

    vs_id = helpers.resolve_id(vsi.resolve_ids, identifier, 'VS')
    if not (env.skip_confirmations or formatting.confirm("This action will incur charges on your account. Continue?")):
        raise exceptions.CLIAbort('Aborted')

    if memory:
        memory = int(memory / 1024)
    if disk is not None:
        disk = json.loads(disk)

    if not vsi.upgrade(vs_id, cpus=cpu, memory=memory, nic_speed=network, public=not private, preset=flavor,
                       disk=disk, add=add):
        raise exceptions.CLIAbort('VS Upgrade Failed')
