# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import PoolMeta
from trytond.pyson import Eval, If


class AccountTemplate(metaclass=PoolMeta):
    __name__ = 'account.account.template'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.party_required.domain = [
            If(~Eval('type'), ('party_required', '=', False), ()),
            ]
        cls.party_required.states['invisible'] = ~Eval('type')


class Account(metaclass=PoolMeta):
    __name__ = 'account.account'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.party_required.domain = [
            If(~Eval('type'), ('party_required', '=', False), ()),
            ]
        cls.party_required.states['invisible'] = ~Eval('type')
