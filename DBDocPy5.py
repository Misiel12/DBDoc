# Copyright (c) 2016, Drakecall. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 of the
# License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

# MySQL Workbench Plugin - Written in MySQL Workbench 6.2.3

# An utility to generate data dictionaries (DBDoc)

# Install it through Scripting/Install Plugin/Module menu
# select DBDocPy.py file, restart MWB for the change to take effect.

# It can be accessed through Tools/Utilitere menu, there are 2 options:
# A text version, displayed at MWB console
# An HTML version, exported to a file

# https://github.com

from wb import *
import grt
import ntpath
from mforms import FileChooser
import mforms

ModuleInfo = DefineModule(name="DBdoc HTML", author="Ali Moreno", version="2.0", description="Data Dictionary")


@ModuleInfo.plugin("ali.DBDoc.htmlDataDictionary", caption="DBDoc: Esquema a HTML",
                   description="Diccionario de datos HTML", input=[wbinputs.currentDiagram()], pluginMenu="Utilities")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def htmlDataDictionary(diagram):
    # Put plugin contents here
    htmlOut = ""
    filechooser = FileChooser(mforms.SaveFile)
    if filechooser.run_modal():
        htmlOut = filechooser.get_path()
        print "HTML File: %s" % (htmlOut)
    if len(htmlOut) <= 1:
        return 1

    # iterate through columns from schema
    tables =''
    for figure in diagram.figures:
        if hasattr(figure, "table") and figure.table:
            tables += writeTableDoc(figure.table)


    htmlFile = open("%s.html" % (htmlOut), "w")
    print >> htmlFile, "<html><head><meta charset='UTF-8'>"
    print >> htmlFile, "<title>Diccionario de Datos: %s</title>" % (path_leaf(htmlOut))

    print >> htmlFile, """<link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/style.css">
    <script src="js/jquery.js"></script>
    <script src="js/bootstrap.js"></script>
    <script src="js/npm.js"></script>
    <script src="js/script.js"></script>
    </head>
    <body>
     <nav class="navbar navbar-custom container">
    <div class="container">
        <div class="navbar-header page-scroll">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar"
                    aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <i class="fa fa-bars" aria-hidden="true"></i>
            </button>
            <a class="navbar-brand" href="index.html"><img src="img/sait-clean-menu.png" height="30" width="100"/> <span
                    id="titulo">Base de datos </span> </a>
        </div>
        <div id="navbar" class="collapse navbar-collapse navbar-right navbar-main-collapse">
            <ul class="nav navbar-nav">
                <li class="hidden">
                    <a href="#page-top"></a>
                </li>

                <li class="page-scroll">
                    <a href="SaitDB.html">Sait</a>
                </li>
                <li class="page-scroll">
                    <a href="Cajav1.html">Cajav1</a>
                </li>
                <li class="page-scroll">
                    <a href="Cajav2.html">Cajav2</a>
                </li>
                <li class="page-scroll">
                    <a href="Compras.html">Compras</a>
                </li>
                <li class="page-scroll">
                    <a href="Contabilidad.html">Contabilidad</a>
                </li>
                <li class="page-scroll">
                    <a href="Inventario.html">Inventario</a>
                </li>
                <li class="page-scroll">
                    <a href="Otros.html">Otros</a>
                </li>
                <li class="page-scroll">
                    <a href="Ventas.html">Ventas</a>
                </li>
            </ul>
        </div><!--/.nav-collapse -->
    </div>
</nav>
 

    """
    print >> htmlFile, "<div class='contain'><img class='img-thumbnail center-block imagen' src='img/%s'></div>" % (path_leaf(htmlOut))

    print >> htmlFile, "%s" % (tables)

    print >> htmlFile, "</body><div></div></html>"

    return 0

def writeTableDoc(table):
        htmlFile = ''
        htmlFile += "<div class='container'><div class='panel panel-default'><div class='panel-heading'>%s<span class='pull-right clickable panel-collapsed'><i class='glyphicon glyphicon-chevron-down'></i></span></div><div class='panel-body' style='display: none;'><table class='table table-hover table-striped table-bordered'><caption>Tabla: %s  %s</caption>" % (table.name, table.name, table.comment)
        htmlFile += """<tr><td colspan=\"7\">%s  %s</td></tr>
        <tr>
        <th>Nombre</th>
        <th>Tipo</th>
        <th>PK</th>
        <th>FK</th>
        <th>Comentario</th>
        </tr>"""  % (table.name, table.comment)
        for column in table.columns:
            pk = ('No', 'Si')[bool(table.isPrimaryKeyColumn(column))]
            fk = ('No', 'Si')[bool(table.isForeignKeyColumn(column))]
            nn = ('No', 'Si')[bool(column.isNotNull)]
            htmlFile += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            column.name, column.formattedType,pk, fk, column.comment)

        if (len(table.foreignKeys)):
            htmlFile += "</table></br>"
            htmlFile += "<table class='table table-hover table-striped table-bordered'><caption>Llaves foraneas</caption>"
            htmlFile += """<tr><td colspan=\"4\"></td></tr>
                <tr>
                <th>fk</th>
                <th>columnas</th>
                <th>Tabla referenciada</th>
                <th>columnas referenciadas</th>
                </tr>
                """
            for ForeignKey in table.foreignKeys:
                htmlFile += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                ForeignKey.name,map(lambda x:  x.name , ForeignKey.columns),ForeignKey.referencedTable.name,map(lambda x:  x.name , ForeignKey.referencedColumns))
            htmlFile += "</table></br>"

        if (len(table.indices)):
            name = ''
            htmlFile += "</table></br>"
            htmlFile += "<table class='table table-hover table-striped table-bordered'><caption>Indices</caption>" 
            htmlFile += """<tr><td colspan=\"4\"></td></tr>
                <tr>
                <th>Nombre</th>
                <th>Columnas</th>
                </tr>
                """
            for index in table.indices:
                namen = index.name
                for column in index.columns:
                    if not namen == name:
                        if not namen == 'PRIMARY':
                            name = index.name
                            pk = ('No', 'Si')[bool(table.isPrimaryKeyColumn(column.referencedColumn))]
                            if (pk == 'Si'):
                                htmlFile += "<tr><td>%s</td><td>%s</td></tr>" % (
                                index.name, map(lambda x:  x.referencedColumn.name , index.columns),)
            htmlFile += "</table></br>"

        htmlFile += "</table></div></div></br></div>"
        return htmlFile

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)