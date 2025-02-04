"""Displays information about the accounts bandwidth pools"""
# :license: MIT, see LICENSE for more details.
import click

from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.managers.account import AccountManager as AccountManager
from SoftLayer import utils


@click.command()
@environment.pass_env
def cli(env):
    """Displays bandwidth pool information

    Similiar to https://cloud.ibm.com/classic/network/bandwidth/vdr
    """

    manager = AccountManager(env.client)
    items = manager.get_bandwidth_pools()

    table = formatting.Table([
        "Pool Name",
        "Region",
        "Servers",
        "Allocation",
        "Current Usage",
        "Projected Usage"
    ], title="Bandwidth Pools")
    table.align = 'l'

    for item in items:
        name = item.get('name')
        region = utils.lookup(item, 'locationGroup', 'name')
        servers = manager.get_bandwidth_pool_counts(identifier=item.get('id'))
        allocation = "{} GB".format(item.get('totalBandwidthAllocated', 0))
        current = "{} GB".format(utils.lookup(item, 'billingCyclePublicBandwidthUsage', 'amountOut'))
        projected = "{} GB".format(item.get('projectedPublicBandwidthUsage', 0))

        table.add_row([name, region, servers, allocation, current, projected])
    env.fout(table)
