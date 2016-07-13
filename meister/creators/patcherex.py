#!/usr/bin/env python

import meister.creators
from farnsworth.models.job import PatcherexJob

LOG = meister.creators.LOG.getChild('patcherex')


class PatcherexCreator(meister.creators.BaseCreator):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    @property
    def jobs(self):
        LOG.debug("Collecting jobs")
        for cbn in self.cbns():
            job, _ = PatcherexJob.get_or_create(cbn=cbn,
                                                limit_cpu=1,
                                                limit_memory=10)
            LOG.debug("Yielding PatcherexJob for %s", cbn.id)
            yield job
