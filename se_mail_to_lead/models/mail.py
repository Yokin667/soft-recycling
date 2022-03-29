# -*- coding: utf-8 -*-


from odoo import api, fields, models
import re
from lxml import html
import datetime
import logging

_logger = logging.getLogger(__name__)


class ModuleName(models.Model):
    _inherit = 'crm.lead'

    origen_contacto = fields.Char(string='Origen Contacto')


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def prepare_vals_for_boolean(self, label_rec, value):
        if value.lower() in ['true', 'yes', '1']:
            return {label_rec.bind_with.name: True}
        else:
            return {label_rec.bind_with.name: False}
        return {}

    def prepare_vals_for_char(self, label_rec, value):
        try:
            return {label_rec.bind_with.name: value}
        except:
            _logger.warning(
                'Data is not set for string format for label: {0}'.format(label_rec.name))

    def prepare_vals_for_datetime(self, label_rec, value):
        try:
            datetime_vals = datetime.datetime.strptime(
                value, label_rec.format_datetime)
            return {label_rec.bind_with.name: datetime_vals}
        except:
            _logger.warning(
                'DateTime field format not properly set for label: {0}'.format(label_rec.name))

    def prepare_vals_for_date(self, label_rec, value):
        try:
            date_vals = datetime.datetime.strptime(
                value, label_rec.format_date).date()
            return {label_rec.bind_with.name: date_vals}
        except:
            _logger.warning(
                'Date field format not properly set for label: {0}'.format(label_rec.name))

    def prepare_vals_for_float(self, label_rec, value):
        try:
            return {label_rec.bind_with.name: float(value)}
        except:
            _logger.warning(
                'Data is not in float format for label: {0}'.format(label_rec.name))

    def prepare_vals_for_html(self, label_rec, value):
        try:
            return {label_rec.bind_with.name: value}
        except:
            _logger.warning(
                'Data is not in html format for label: {0}'.format(label_rec.name))

    def prepare_vals_for_integer(self, label_rec, value):
        try:
            return {label_rec.bind_with.name: int(value)}
        except:
            _logger.warning(
                'Data is not in integer format for label: {0}'.format(label_rec.name))

    def prepare_vals_for_selection(self, label_rec, value):
        a = dict(self._fields[
                     label_rec.bind_with.name].selection)
        k = ''
        for key, val in a.items():
            val1 = val.lower()
            val2 = value.lower()
            if val2 == val1:
                k = key
        if k != '':
            try:
                return {label_rec.bind_with.name: k}
            except:
                _logger.warning(
                    'Data is not in string format for label: {0}'.format(label_rec.name))
        else:
            _logger.warning(
                'Data is not in string format for label: {0}'.format(label_rec.name))

    def prepare_vals_for_text(self, label_rec, value):
        try:
            return {label_rec.bind_with.name: value}
        except:
            _logger.warning(
                'Data is not in string format for label: {0}'.format(label_rec.name))

    @api.model
    def message_new(self, msg_dict, custom_values=None):

        if self._name == 'crm.lead':
            additional_info = {}

            result = re.search('<table(.*)</table>', msg_dict['body'])
            # if result:
            #    body = result.group(1)
            #    start_string = "<table "
            #     end_string = " </table>"
            #    final_string = start_string + body + end_string
            # else:
            final_string = msg_dict['body']

            # tree = html.fromstring(final_string)
            # rows = tree.xpath('//tr/td')
            # labels = []
            labels = self.env['lead.labels'].search([])
            data = []
            counter1 = 0
            # for row in rows:
            #    temp = "".join([t.strip() for t in row.itertext()]).strip()
            #     if counter1 % 2 == 1:
            #        data.append(temp)
            #    else:
            #       labels.append(temp)
            #    counter1 += 1
            br=0
            for l in labels:
                index=final_string.find(l.name,br)
                br=final_string.find('<br>',index)
                line = final_string[index:br]
                line=line.strip().split(':')
                data.append(line[1].strip())


            if data and labels:
                data_len = len(data)
                counter = 1
                for label in labels:
                    if counter > data_len:
                        break
                    else:
                        if data[counter - 1]:
                            value = str(data[counter - 1]).strip()
                            has_label=label
                            if has_label:
                                # if has_label.typee == 'one2many':
                                #     subtype = has_label.subtypee

                                if has_label.typee == 'boolean':
                                    result = self.prepare_vals_for_boolean(
                                        has_label, value)
                                    additional_info.update(result)

                                if has_label.typee == 'char':
                                    result = self.prepare_vals_for_char(
                                        has_label, value)
                                    additional_info.update(result)

                                # For date and datetime fields, convert based
                                # on given format.
                                if has_label.typee == 'datetime':
                                    result = self.prepare_vals_for_datetime(
                                        has_label, value)
                                    additional_info.update(result)

                                if has_label.typee == 'date':
                                    result = self.prepare_vals_for_date(
                                        has_label, value)
                                    additional_info.update(result)

                                if has_label.typee == 'float':
                                    result = self.prepare_vals_for_float(
                                        has_label, value)
                                    additional_info.update(result)

                                # Here HTML field, data only print value of
                                # that column not tags<>.
                                if has_label.typee == 'html':
                                    result = self.prepare_vals_for_html(
                                        has_label, value)
                                    additional_info.update(result)

                                if has_label.typee == 'integer':
                                    result = self.prepare_vals_for_integer(
                                        has_label, value)
                                    additional_info.update(result)

                                # For selection field, we compare value with
                                # label of selection field and set accordingly
                                if has_label.typee == 'selection':
                                    result = self.prepare_vals_for_selection(
                                        has_label, value)
                                    additional_info.update(result)

                                if has_label.typee == 'text':
                                    result = self.prepare_vals_for_text(
                                        has_label, value)
                                    additional_info.update(result)
                    counter += 1
                custom_values.update(additional_info)

        result = super(MailThread, self).message_new(
            msg_dict=msg_dict, custom_values=custom_values)
        return result
