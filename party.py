# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Equal


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    client_number = fields.Function(fields.Char('Client Number',
        states={'readonly': True}),
        'get_client_number', setter='set_client_number')

    def get_client_number(self, name):
        for identifier in self.identifiers:
            if identifier.type == 'client_number':
                return identifier.code

    def get_full_name(self, name):
        full_name = self.name
        if self.client_number:
            full_name = "[%s] %s" % (self.client_number, self.name)
        else:
            full_name = self.name
        return full_name

    @classmethod
    def set_client_number(cls, partys, name, value):
        party_id = partys[0].id
        PartyIdentifier = Pool().get('party.identifier')
        identifiers = PartyIdentifier.search([
            ('party', 'in', partys),
            ('type', '=', 'client_number'),
            ])
        PartyIdentifier.delete(identifiers)
        if not value:
            return

        PartyIdentifier.create([{
            'code': value,
            'type': 'client_number',
            'party': party_id,
            }])

    def get_rec_name(self, name):
        codes = []
        for identifier in self.identifiers:
            if identifier.type == 'client_number':
                codes.append('[' + identifier.code + ']')
        if codes:
            return ''.join(codes) + self.name
        return self.name

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super().search_rec_name(name, clause),
        return ['OR',
                domain,
                ('identifiers.code',) + tuple(clause[1:]),
                ]

    def identifier_get(self, type=None):
        """
        Try to find an identifier for the given type, if no type matches
        the None is returned. If there are more than one identifier, the first
        is returned.
        """
        PartyIdentifier = Pool().get("party.identifier")
        identifiers = PartyIdentifier.search(
            [("party", "=", self.id), ("type", "=", type)],
            order=[('id', 'ASC')])
        if not identifiers:
            return None
        return identifiers[0]


class PartyIdentifier(metaclass=PoolMeta):
    __name__ = 'party.identifier'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.code.states['readonly'] = Equal(Eval('type'), 'client_number')

    @classmethod
    def get_types(cls):
        types = super().get_types()
        return types + [('client_number', 'Client Number')]

    @classmethod
    def create(cls, vlist):
        Configuration = Pool().get('party.configuration')

        vlist = [x.copy() for x in vlist]
        config = Configuration(1)
        for values in vlist:
            type = values.get('type')
            if type == 'client_number':
                code = values.get('code')
                if code is None and config.client_num_sequence:
                    values['code'] = config.client_num_sequence.get()
        return super().create(vlist)
