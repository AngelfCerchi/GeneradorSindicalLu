import csv
from fpdf import FPDF
from pathlib import Path
from datetime import datetime


#Configuracion:
path = Path("../data/profesionales_fatsa.csv").resolve()
sindicato = "fatsa"


#Crea la categoria del empleado.
def crearCategoria(categoria,periodo,codigo,pdf):
        lineaUno = '<record id="general_category_{}" model="hr.labor_union.category">'.format(categoria.lower().replace(" ","_"))
        lineaDos = '<field name="labor_union_id" ref="l10n_ar_payroll_lu_{}.lu_{}" />'.format(sindicato.lower(),sindicato.lower())
        lineaTres = '<field name="name">{}</field>'.format(categoria)
        lineaCuatro = '<field name="category_period_type">{}</field>'.format(periodo.lower())
        lineaCinco = '<field name="code">{}</field>'.format(codigo.upper())
        lineaSeis = '</record>'
        data = [lineaUno,lineaDos,lineaTres,lineaCuatro,lineaCinco,lineaSeis]
        for e in data:
            pdf.cell(200,10,e,ln=2,align="L")

#Crea las versiones de sueldos por la categoria declarada.
def crearVersion2(periodoVersion,monto,categoria,sindicato,pdf):
        lineaUno=  '<record id="category_price_general_category_{}_{}" model="hr.labor_union.category.price">'.format(categoria.lower().replace(" ","_"),periodoVersion.strftime("%m/%Y").replace("/",""))
        lineaDos = '<field name="labor_union_category_id" ref="l10n_ar_payroll_lu_{}.general_category_{}" />'.format(sindicato.lower(),categoria.lower().replace(" ","_"))
        lineaTres =  '<field name="from_date">{}</field>'.format(periodoVersion.strftime("%Y/%m/%d").replace("/","-"))
        lineaCuatro = '<field name="value">{}</field>'.format(monto.replace(",","."))
        lineaCinco = '</record>'
        data = [lineaUno,lineaDos,lineaTres,lineaCuatro,lineaCinco]
        for e in data:
            pdf.cell(200,10,e,ln=2,align="L")
        
with open(path) as csv_file:
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_right_margin(32)
    pdf.set_font("Arial",size=11)
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        if row[0]=="":
            break;
        categoria = row[0]
        periodo = row[1]
        codigo = row[2]
        print("")
        print("** CREANDO CATEGORIA: '{}' CODIGO: '{}' TIPO_DE_PAGO: '{}'".format(categoria,codigo,periodo))
        crearCategoria(categoria,periodo,codigo,pdf)
        for i in range(3,len(row),2):
            if row[i]=="":
                break;
            else:
                periodoVersion = row[i]
                periodoVersionFormatted = datetime.strptime(periodoVersion, '%d/%m/%Y' )
                monto = row[i+1]
                print("* CREANDO VERSION PARA:  Cat '{}' Fecha '{}' Monto '{}' ".format(categoria,periodoVersionFormatted.strftime("%m/%Y"),monto))
                crearVersion2(periodoVersionFormatted,monto,categoria,sindicato,pdf)
    print("")
    print(" SE CREO EL REPORTE EN PDF EN SRC/categorias_{}.pdf".format(sindicato))
    print("")
    pdf.output("categorias_{}.pdf".format(sindicato))
