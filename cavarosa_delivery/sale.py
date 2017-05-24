# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2017- Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = 'delivery.carrier'

    @api.one
    def import_costs(self):
        if len(self.pricelist_ids) > 0:
            for grid in self.pricelist_ids:
                self.env['delivery.grid.line'].search([('grid_id', '=', grid.id)]).unlink()
                grid.unlink()
        pricelist = self.env['delivery.grid'].create({
            'carrier_id': self.id,
            'name': 'Home Delivery',
            'country_ids': [(4, self.env.ref('base.se').id, 0)],
            'zip_from': str(int(Iterator(ws).zip_from)),
            'zip_to': str(int(Iterator(ws).zip_to)),
        })
        for r in Iterator(ws):
            self.env['delivery.grid.line'].create({
                'name': '%s - 1-3 kli' %int(r.get('postnummer')),
                'type': 'quantity',
                'operator': '<=',
                'max_value': 3.0,
                'price_type': 'fixed',
                'list_price': r.get('pris 1-3 kli'),
                'standard_price': 0.0,
                'grid_id': pricelist.id,
            })
            self.env['delivery.grid.line'].create({
                'name': '%s - 4-6 kli' %int(r.get('postnummer')),
                'type': 'quantity',
                'operator': '>=',
                'max_value': 4.0,
                'price_type': 'fixed',
                'list_price': r.get('pris 4-6 kli'),
                'standard_price': 0.0,
                'grid_id': pricelist.id,
            })
