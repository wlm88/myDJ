import http
import math
from datetime import timedelta
import pytest
from django.http import HttpResponse, request
from pandas.tests.io.excel.test_xlrd import xlwt


def action_invoice_download(self):
    return {
        'type': 'ir.actions.act_url',
        'url': '/invoice/excel/download/%s' % self.id,
    }


@http.route('/invoice/excel/download/<int:invoice_id>', type='http', auth='user')
def invoice_excel_download(self, invoice_id, **kwargs):
    invoice = request.env['account.invoice'].browse(invoice_id)

    data = ['序号', '订单日期', '送货日期', '送货单号', '采购订单编号', '商品条码', '产品名称', '规格型号', '订单价格', '订单数量', '累计收货数量', '实际收货单位',
            '实际收货数量', '单价', '金额(含税)', '备注']

    num = 0
    data_line_ids = []
    for item in invoice.invoice_line_ids:
        num += 1
        if item.order_date:
            order_date = item.order_date + timedelta(hours=8)
            order_date = order_date.strftime('%Y-%m-%d')
        else:
            order_date = ' '
        if item.m_delivery_date:
            m_delivery_date = item.m_delivery_date + timedelta(hours=8)
            m_delivery_date = m_delivery_date.strftime('%Y-%m-%d')
        else:
            m_delivery_date = ' '

        data_line = [num, order_date, m_delivery_date, item.m_move_id.picking_id.name,
                     item.purchase_line_id.order_id.name, item.barcode, item.product_id.name,
                     item.product_id.m_specifications, item.purchase_line_id.price_unit,
                     item.purchase_line_id.product_qty, item.purchase_line_id.qty_received,
                     item.uom_id.name, item.quantity, item.price_unit,item.price_total, invoice.comment]
        new_data_line = ['' if items == False else items for items in data_line]
        data_line_ids.append(new_data_line)
    results_num = len(data_line_ids)
    #
    workbook = xlwt.Workbook()
    # style = xlwt.XFStyle()  # 创建style对象
    style = xlwt.easyxf('pattern:pattern solid,fore_colour gray25')
    alignment = xlwt.Alignment()  # 创建alignment对象
    # 指定水平居中 HORZ_CENTER = 0x02 左端对齐
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment  # 指定对齐格式

    sheet_counts = math.ceil(results_num / LIMIT_ROW_PER_SHEET)
    for sheet_num in range(sheet_counts):
        sheet_num = sheet_num + 1
        worksheet = workbook.add_sheet('销售统计{}'.format(sheet_num), cell_overwrite_ok=True)
        if invoice.create_date:
            reconciliation_date = invoice.create_date + timedelta(hours=8)
            reconciliation_date = reconciliation_date.strftime('%Y-%m-%d')
        else:
            reconciliation_date = ' '
        worksheet.write_merge(0, 0, 0, 7, f"甲方名称：{invoice.user_id.company_id.name}")
        worksheet.write_merge(0, 0, 8, 15, f'供应商：{invoice.partner_id.name}')
        worksheet.write_merge(1, 1, 0, 7, f'地址：{invoice.company_id.street}')
        worksheet.write_merge(1, 1, 8, 15, f'交货地点：{invoice.partner_id.street}')
        worksheet.write_merge(2, 2, 0, 7, f'对账日期：{reconciliation_date}')
        worksheet.write_merge(2, 2, 8, 15, f'联系电话：{invoice.partner_id.phone}')

        # 写入数据
        for i in range(len(data)):
            worksheet.write(4, i, data[i], style)
        num1 = 0
        for data_account in data_line_ids:
            num1 += 1
            num2 = 4 + num1
            for k in range(len(data_account)):
                # worksheet.set_row(num2, 100)
                worksheet.write(num2, k, data_account[k])

    file_name = f'{invoice.display_name}.xlsx'
    response = request.make_response(None, headers=[
            ('Content-Type', 'application/vnd.ms-excel'),
            ('Content-Disposition', content_disposition(file_name))
        ],
        )
    workbook.save(response.stream)
    return response