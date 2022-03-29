# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    reg = fields.Char('Matricula')
    made = fields.Char('Fabricacion')
    model = fields.Char('Modelo')
    year = fields.Char('Año Fabricación')
    weight = fields.Char('Peso')
    qoute = fields.Char('Cuota')   

