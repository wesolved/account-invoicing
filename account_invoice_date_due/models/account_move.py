from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    editable_date_due = fields.Date(
        string="Due Date (Editable)",
        help="This field allows manual modification of the due date, even when a payment term is set.",
    )

    @api.onchange("editable_date_due")
    def _onchange_editable_date_due(self):
        """Update invoice_date_due when editable_date_due changes."""
        if self.editable_date_due:
            self.invoice_date_due = self.editable_date_due

    @api.model_create_multi
    def create(self, vals_list):
        """Set editable_date_due from invoice_date_due on creation."""
        moves = super().create(vals_list)
        for move in moves:
            if move.invoice_date_due:
                move.editable_date_due = move.invoice_date_due
        return moves

    def write(self, vals):
        """Synchronize editable_date_due with invoice_date_due."""
        res = super().write(vals)
        if "invoice_date_due" in vals and not vals.get("editable_date_due"):
            for move in self:
                move.editable_date_due = move.invoice_date_due
        return res 