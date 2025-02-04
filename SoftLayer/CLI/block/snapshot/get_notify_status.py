"""Get the snapshots space usage threshold warning flag setting for specific volume"""
# :license: MIT, see LICENSE for more details.

import click
import SoftLayer
from SoftLayer.CLI import environment


@click.command()
@click.argument('volume_id')
@environment.pass_env
def cli(env, volume_id):
    """Get snapshots space usage threshold warning flag setting for a given volume"""
    block_manager = SoftLayer.BlockStorageManager(env.client)
    enabled = block_manager.get_volume_snapshot_notification_status(volume_id)

    if enabled == 0:
        click.echo("Disabled: Snapshots space usage threshold is disabled for volume {}".format(volume_id))
    else:
        click.echo("Enabled: Snapshots space usage threshold is enabled for volume {}".format(volume_id))
