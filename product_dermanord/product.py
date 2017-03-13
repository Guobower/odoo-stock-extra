# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2016- Vertel AB (<http://vertel.se>).
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

import openerp.exceptions
from openerp.osv import osv
from openerp.osv import fields as osv_fields
from openerp import models, fields, api, _
try:
    import erppeek
except:
    pass

import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit="product.template"

    #~ @api.one
    #~ def _tariff(self):
        #~ if(self.env.ref('base.us').id == self.partner_id.country_id.id):
            #~ self.tariff = self.ustariff
        #~ else:
            #~ self.tariff = self.intrastat_id


    #~ tariff = fields.Char(string='Tariff', compute='_tariff')
    ustariff = fields.Char(string='US Tariff',oldname='x_ustariff')
    iskit = fields.Boolean(string='Is Kit',oldname='x_iskit')

    #combine products
    @api.one
    def combine_products(self, tmp=None):
        for v in self.product_variant_ids:
            v.write({
                'product_tmpl_id': tmp.id,
            })

    #orderpoint_ids
    @api.one
    def _cost_price(self):
        self.cost_price = 0.38 * self.list_price
    cost_price = fields.Float(compute="_cost_price")
    @api.one
    def _variants(self):
        self.variants = ','.join([p.default_code or p.name or '' for p in self.product_variant_ids])
    variants = fields.Char(compute="_variants")
    @api.one
    def _taxes(self):
        self.taxes_view = ','.join([t.description for t in self.taxes_id])
        self.supplier_taxes_view = ','.join([t.description for t in self.supplier_taxes_id])
    taxes_view = fields.Char(compute="_taxes")
    supplier_taxes_view = fields.Char(compute="_taxes")
    #~ orderpoints = fields.One2many(related='product_variant_ids.orderpoint_ids')
    #~ @api.one
    #~ def _stock(self):
        #~ self.orderpoints = ','.join([o.name or '' for o in [v.orderpoint_ids or [] for v in self.product_variant_ids]])
    #~ orderpoints = fields.Char(compute='_stock')

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
    _columns = {
        'property_stock_procurement': osv_fields.property(
            type='many2one',
            relation='stock.location',
            string="Procurement Location",
            domain=[('usage','like','procurement')],
            help="This stock location will be used, instead of the default one, as the source location for stock moves generated by procurements."),
        'property_stock_production': osv_fields.property(
            type='many2one',
            relation='stock.location',
            string="Production Location",
            domain=[('usage','like','production')],
            help="This stock location will be used, instead of the default one, as the source location for stock moves generated by manufacturing orders."),
        'property_stock_inventory': osv_fields.property(
            type='many2one',
            relation='stock.location',
            string="Inventory Location",
            domain=[('usage','like','inventory')],
            help="This stock location will be used, instead of the default one, as the source location for stock moves generated when you do an inventory."),
        }

class Product(models.Model):
    _inherit="product.product"

    ingredients = fields.Text(string='Ingredients', translate=True,)
    ingredients_changed_by = fields.Char(string='Ingredients Changed By', )
    ingredients_last_changed = fields.Date(string='Ingredients Last Changed', )
    public_desc = fields.Text(string='Public Description', translate=True, )
    public_desc_changed_by = fields.Char(string='Public Description Changed By', )
    public_desc_last_changed = fields.Date(string='Public Description Last Changed', )
    reseller_desc = fields.Text(string='Reseller Description', translate=True, )
    reseller_desc_changed_by = fields.Char(string='Reseller Description Changed By', )
    reseller_desc_last_changed = fields.Date(string='Reseller Description Last Changed', )
    shelf_label_desc = fields.Text(string='Shelf Label Description', translate=True, )
    shelf_label_desc_changed_by = fields.Char(string='Shelf Label Description Changed By', )
    shelf_label_desc_last_changed = fields.Date(string='Shelf Label Description Last Changed', )
    use_desc = fields.Text(string='Use Description', translate=True, )
    use_desc_changed_by = fields.Char(string='Use Description Changed By', )
    use_desc_last_changed = fields.Date(string='Use Description Last Changed', )

    #~ ingredients = fields.Text(String='Ingredients', translate=True, oldname='x_ingredients')
    #~ ingredients_changed_by = fields.Char(String='Ingredients Changed By', oldname='x_ingredients_changed_by')
    #~ ingredients_last_changed = fields.Date(String='Ingredients Last Changed', oldname='x_ingredients_last_changed')
    #~ public_desc = fields.Text(String='Public Description', translate=True, oldname='x_public_desc')
    #~ public_desc_changed_by = fields.Char(String='Public Description Changed By', oldname='x_public_desc_changed_by')
    #~ public_desc_last_changed = fields.Date(String='Public Description Last Changed', oldname='x_public_desc_last_changed')
    #~ reseller_desc = fields.Text(String='Reseller Description', translate=True, oldname='x_reseller_desc')
    #~ reseller_desc_changed_by = fields.Char(String='Reseller Description Changed By', oldname='x_reseller_desc_changed_by')
    #~ reseller_desc_last_changed = fields.Date(String='Reseller Description Last Changed', oldname='x_reseller_desc_last_changed')
    #~ shelf_label_desc = fields.Text(String='Shelf Label Description', translate=True, oldname='x_shelf_label_desc')
    #~ shelf_label_desc_changed_by = fields.Char(String='Shelf Label Description Changed By', oldname='x_shelf_label_desc_changed_by')
    #~ shelf_label_desc_last_changed = fields.Date(String='Shelf Label Description Last Changed', oldname='x_shelf_label_desc_last_changed')
    #~ use_desc = fields.Text(String='Use Description', translate=True, oldname='x_use_desc')
    #~ use_desc_changed_by = fields.Char(String='Use Description Changed By', oldname='x_use_desc_changed_by')
    #~ use_desc_last_changed = fields.Date(String='Use Description Last Changed', oldname='x_use_desc_last_changed')
    #new fileds
    ingredients_changed_by_uid = fields.Many2one(comodel_name='res.users', String='Ingredients Changed By')
    public_desc_changed_by_uid = fields.Many2one(comodel_name='res.users', String='Public Description Changed By')
    reseller_desc_changed_by_uid = fields.Many2one(comodel_name='res.users', String='Reseller Description Changed By')
    shelf_label_desc_changed_by_uid = fields.Many2one(comodel_name='res.users', String='Shelf Label Description Changed By')
    use_desc_changed_by_uid = fields.Many2one(comodel_name='res.users', String='Use Description Changed By')
    @api.one
    def _attribute_value_names(self):
        self.attribute_value_names = ','.join(a.name for a in self.attribute_value_ids)
    attribute_value_names = fields.Char(string='Attribute Names', compute='_attribute_value_names', help='This field made for glabel printing')

    # account.analytic.line för produkten på line, knyt till external id produkt-konto
    # om produkten på line är is_kit -> slå upp produkter på bom (säljbara produkter)
    # för varje produkt på bom skapa account.analytic.line
    # antal hänsynt till antal på line samt antal på bom
    # belopp hänsyn till andel av bom-kostnad omräknad till belopp på line säljpris lst_price

    @api.model
    def bom_account_create(self, line):
        product = line.product_id
        if product:
            account = self.env.ref('product_dermanord.account_products')
            move_line = line.invoice_id.move_id.line_id.filtered(lambda l: len(l.analytic_lines) > 0)
            move_id = move_line[0].id if move_line else None
            currency = line.invoice_id.currency_id.with_context(date=line.invoice_id.date_invoice)
            self.env['account.analytic.line'].create({
                'move_id': move_id,
                'name': line.name,
                'date': line.invoice_id.date_invoice,
                'account_id': account.id,
                'unit_amount': line.quantity,
                'amount': currency.compute(line.price_subtotal, line.invoice_id.company_id.currency_id) * 1 if line.invoice_id.type in ('out_invoice', 'in_refund') else -1,
                'product_id': line.product_id.id,
                'product_uom_id': line.uos_id.id,
                'general_account_id': line.account_id.id,
                'journal_id': line.invoice_id.journal_id.analytic_journal_id.id,
                'ref': line.invoice_id.reference if line.invoice_id.type in ('in_invoice', 'in_refund') else line.invoice_id.number,
            })
            if product.iskit and product.bom_ids:
                account = self.env.ref('product_dermanord.account_kit_products')
                total = 0
                for bom_line in product.bom_ids[0].bom_line_ids:
                    if bom_line.product_id.sale_ok:
                        total += bom_line.product_id.lst_price * bom_line.product_qty
                for bom_line in product.bom_ids[0].bom_line_ids:
                    if bom_line.product_id.sale_ok:
                        amount = line.price_subtotal * bom_line.product_id.lst_price * bom_line.product_qty / total
                        self.env['account.analytic.line'].create({
                            'move_id': move_id,
                            'name': line.name,
                            'date': line.invoice_id.date_invoice,
                            'account_id': account.id,
                            'unit_amount': line.quantity * bom_line.product_qty,
                            'amount': currency.compute(amount, line.invoice_id.company_id.currency_id) * 1 if line.invoice_id.type in ('out_invoice', 'in_refund') else -1,
                            'product_id': bom_line.product_id.id,
                            'product_uom_id': bom_line.product_uos.id,
                            'general_account_id': line.account_id.id,
                            'journal_id': line.invoice_id.journal_id.analytic_journal_id.id,
                            'ref': line.invoice_id.reference if line.invoice_id.type in ('in_invoice', 'in_refund') else line.invoice_id.number,
                        })

class product_attribute_value(models.Model):
    _inherit = "product.attribute.value"


    def get_param(self,param,value):
        if not self.env['ir.config_parameter'].get_param(param):
            self.env['ir.config_parameter'].set_param(param,value)
            return value
        else:
            return self.env['ir.config_parameter'].get_param(param)

    @api.one
    def get_remote_price(self):
        tmpl_id = self.env.context.get('active_id')
        if not tmpl_id:
            return None
        tmpl = self.env['product.template'].browse(tmpl_id)
        base_variant = tmpl.product_variant_ids.sorted(lambda v: v.name)[0]
        this_variant = self.env['product.product'].search([('product_tmpl_id','=',tmpl_id),('id','in',[p.id for p in self.product_ids])])[0]

        client = erppeek.Client(self.get_param('host6','')+':'+'8069',self.get_param('host6db',''), 'admin',self.get_param('host6pw',''))
        if not client:
            raise Warning(_('Create parameter for host6/host6db/host6pw'))

        price_remote_ids = client.model('product.product').search([('default_code','=',this_variant.default_code)])
        if len(price_remote_ids) == 0:
            raise Warning(_('Missing remote product %s (%s)') % (this_variant.default_code,this_variant))
        price_remote = client.model('product.product').browse(price_remote_ids[0])
        _logger.info('Get remote price (remote=%s tmpl=%s)' % (price_remote.list_price,tmpl.lst_price))
        price = self.env['product.attribute.price'].search(['&',('product_tmpl_id','=',tmpl_id),('value_id','=',self.id)])
        if not price:
            self.env['product.attribute.price'].create({
                'product_tmpl_id': tmpl_id,
                'value_id': self.id,
                'price_extra': price_remote.list_price - tmpl.lst_price,
                    })
        else:
            price.write({'price_extra':price_remote.list_price - tmpl.lst_price })

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    def _tariff(self):
        if self.product_id:
            if self.invoice_id.partner_shipping_id.country_id.id == self.env.ref('base.us').id:
                self.tariff = self.product_id.ustariff
            else:
                self.tariff = self.product_id.intrastat_id.name

    tariff = fields.Char(string='Tariff', compute='_tariff')

class account_invoice_line(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def action_move_create(self):
        res = super(account_invoice_line, self).action_move_create()
        _logger.warn('invoice',self,'lines',self.invoice_line)
        #raise Warning('kalle')
        for l in self.invoice_line:
            self.env['product.product'].bom_account_create(l)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
