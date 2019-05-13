# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import configuration


def register():
    Pool.register(
        party.Party,
        party.PartyIdentifier,
        configuration.Configuration,
        configuration.ConfigurationSequence,
        module='party_gcoop', type_='model')
