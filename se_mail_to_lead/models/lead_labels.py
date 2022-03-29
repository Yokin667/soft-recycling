# -*- coding: utf-8 -*-


from odoo import models, fields


class LeadLabels(models.Model):

    _name = 'lead.labels'

    def prepare_domain(self):
        crm_model = self.env['ir.model'].search(
            [('model', '=', 'crm.lead')], limit=1)
        return [
            ('model_id', '=', crm_model.id),
            ('ttype', 'not in', ['binary', 'many2many', 'one2many', 'monetary', 'many2one', 'reference'])]

    name = fields.Char(string='Label')
    bind_with = fields.Many2one('ir.model.fields', domain=prepare_domain)
    typee = fields.Selection(related='bind_with.ttype')
    relation = fields.Char(related='bind_with.relation')
    format_date = fields.Char(string="Date Format")
    format_datetime = fields.Char(string="DateTime Format")
    bind_with_o2m = fields.Many2one(
        'ir.model.fields', domain="[('model_id.model', '=', relation), ('ttype', 'not in', ['binary', 'many2many', 'many2one', 'one2many', 'reference'])]")
    subtypee = fields.Selection(related='bind_with_o2m.ttype')
