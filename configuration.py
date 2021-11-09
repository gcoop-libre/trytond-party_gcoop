# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Id

client_num_sequence = fields.Many2One('ir.sequence', 'ClientNum Sequence',
    domain=[
        ('sequence_type', '=',
            Id('party_gcoop', 'sequence_type_party_client_num')),
        ],
    help="Used to generate the client number sequence.")


class Configuration(metaclass=PoolMeta):
    'Party Configuration'
    __name__ = 'party.configuration'

    client_num_sequence = fields.MultiValue(client_num_sequence)

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'client_num_sequence':
            return pool.get('party.configuration.party_sequence')
        return super().multivalue_model(field)

    @classmethod
    def default_client_num_sequence(cls, **pattern):
        return cls.multivalue_model(
            'client_num_sequence').default_client_num_sequence()


class ConfigurationSequence(metaclass=PoolMeta):
    __name__ = 'party.configuration.party_sequence'
    client_num_sequence = client_num_sequence

    @classmethod
    def default_client_num_sequence(cls):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        try:
            return ModelData.get_id('party', 'sequence_client_num')
        except KeyError:
            return None
