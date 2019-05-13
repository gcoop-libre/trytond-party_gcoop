# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from sql import Table
from trytond.pool import Pool, PoolMeta
from trytond.model import fields, ModelSQL, ModelView
from trytond.pyson import Eval, Equal
from trytond.transaction import Transaction
from trytond import backend

__all__ = ['Party', 'PartyIdentifier']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    client_number = fields.Function(
        fields.Char('Client Number', states={
            'readonly': True,
        }), 'get_client_number', setter='set_client_number')

    def get_client_number(self, name):
        for identifier in self.identifiers:
            if identifier.type == 'client_number':
                return identifier.code

    @classmethod
    def set_client_number(cls, partys, name, value):
        party_id = partys[0].id
        PartyIdentifier = Pool().get('party.identifier')

        identifiers = PartyIdentifier.search([
            ('party', 'in', partys),
            ('type', '=', 'client_number'),
            ])
        if identifiers == []:
            PartyIdentifier.create([{
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
        domain = super(Party, cls).search_rec_name(name, clause),
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
        super(PartyIdentifier, cls).__setup__()
        cls.code.states['readonly'] = Equal(Eval('type'), 'client_number')
        for new_type in [
                ('client_number', 'Client Number'),
                ]:
            if new_type not in cls.type.selection:
                cls.type.selection.append(new_type)

    @classmethod
    def create(cls, vlist):
        Sequence = Pool().get('ir.sequence')
        Configuration = Pool().get('party.configuration')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            type = values.get('type')
            if type == 'client_number':
                code = values.get('code')
                if code is None:
                    config = Configuration(1)
                    if config.client_num_sequence:
                        values['code'] = Sequence.get_id(config.client_num_sequence.id)
        return super(PartyIdentifier, cls).create(vlist)
