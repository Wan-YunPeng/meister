#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Run the meister."""

from __future__ import absolute_import, unicode_literals

import sys
import time

# leave this import before everything else!
import meister.settings

from farnsworth.models import Round

# pylint: disable=ungrouped-imports
from meister.brains.elephant import ElephantBrain
from meister.creators.afl import AFLCreator
from meister.creators.backdoor_submitter import BackdoorSubmitterCreator
from meister.creators.cache import CacheCreator
from meister.creators.cb_tester import CBTesterCreator
from meister.creators.colorguard import ColorGuardCreator
from meister.creators.driller import DrillerCreator
from meister.creators.function_identifier import FunctionIdentifierCreator
from meister.creators.patcherex import PatcherexCreator
from meister.creators.poll_creator import PollCreatorCreator
from meister.creators.network_poll_creator import NetworkPollCreatorCreator
from meister.creators.network_poll_sanitizer import NetworkPollSanitizerCreator
from meister.creators.patch_performance import PatchPerformanceCreator
from meister.creators.povfuzzer1 import PovFuzzer1Creator
from meister.creators.povfuzzer2 import PovFuzzer2Creator
from meister.creators.pov_tester import PovTesterCreator
from meister.creators.rex import RexCreator
from meister.creators.rop_cache import RopCacheCreator
from meister.creators.showmap_sync import ShowmapSyncCreator
import meister.log
from meister.schedulers.priority import PriorityScheduler
# pylint: enable=ungrouped-imports

LOG = meister.log.LOG.getChild('main')


def wait_for_ambassador():
    poll_interval = 3
    while not (Round.current_round() and Round.current_round().is_ready()):
        LOG.info("Round data not available, waiting %d seconds", poll_interval)
        time.sleep(poll_interval)


def main(args=None):
    """Run the meister."""
    if args is None:
        args = []

    brain = ElephantBrain()
    creators = [DrillerCreator(),
                RexCreator(),
                PovFuzzer1Creator(),
                PovFuzzer2Creator(),
                ColorGuardCreator(),
                AFLCreator(),
                BackdoorSubmitterCreator(),
                CacheCreator(),
                RopCacheCreator(),
                PatcherexCreator(),
                FunctionIdentifierCreator(),
                NetworkPollCreatorCreator(),
                ShowmapSyncCreator(),
                #PatchPerformanceCreator(),
                # VM jobs
                #PollCreatorCreator(),
                #NetworkPollSanitizerCreator(),
                #CBTesterCreator(),
                PovTesterCreator()]
    scheduler = PriorityScheduler(brain, creators)

    if '--single' in sys.argv:
        scheduler.run()

    else:
        while True:
            wait_for_ambassador()
            LOG.info("Round #%d", Round.current_round().num)
            scheduler.run()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
