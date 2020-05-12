# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:38:16 2020

@author: iamor
"""
import pdb
import pandas as pd
from xlrd import XLRDError
from .models import Employee
from openpyxl import load_workbook as lw
from django.http import HttpResponse
from io import BytesIO
import xlsxwriter
import requests

from django_tables2 import SingleTableView


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = "filter"

    def get_table_data(self):
        self.filter = self.filter_class(
            self.request.GET, queryset=super().get_table_data()
        )
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data(**kwargs)
        context[self.context_filter_name] = self.filter
        return context

#Auxiliar functions:        
def download_file(obj):
    output = BytesIO()
    # Feed a buffer to workbook
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(str(obj.__name__)+"s")
    objs = obj.objects.all()
    bold = workbook.add_format({'bold': True})
    #modelAttributes = ["employee_number", "name", "surname", "birth_date"]
    modelAttributes = [f.name for f in obj._meta.fields]
    # Fill first row with columns
    row = 0
    for i,elem in enumerate(modelAttributes):
        worksheet.write(row, i, elem, bold)
    row += 1
    # Now fill other rows with columns
    for employee in objs:
        for i,elem in enumerate(modelAttributes):
            e = getattr(employee,elem)
            worksheet.write(row, i, str(e))
        row += 1
    # Close workbook for building file
    workbook.close()
    output.seek(0)
    # see http://xlsxwriter.readthedocs.io/ 
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response
    
def handle_uploaded_file(f, remplacement):
    sheetNameParam = 'Parameters'
    result = "OK"
    fileData = []
    try:
        xl = pd.ExcelFile(f)
        if sheetNameParam not in xl.sheet_names:
            result = "Upload error: The Excel file must have a 'Parameters' worksheet"
        else:
            combCellLength = combinedCellLength(f, sheetNameParam,0)
            params = pd.read_excel(f,  sheet_name=sheetNameParam,skiprows=1)    
            sheetNameData = params[params.columns[combCellLength]][0]
            if sheetNameData not in xl.sheet_names:
                result = "Upload error: The Excel file must have a '"+ sheetNameData +"' worksheet has defined in the parameters worksheet"
            else:
                fileData = pd.read_excel(f,  sheet_name=sheetNameData,skiprows=1)
                paramAttributes = attributesList(params, combCellLength)
                modelAttributes = [f.name for f in Employee._meta.fields]
                result = checkAttributes(paramAttributes, modelAttributes,fileData.columns)
                if result == "OK":
                    df = pd.DataFrame(data=paramAttributes)
                    employeesSaved = 0
                    for i in fileData.index:
                        employeeToSave = Employee()
                        for e in df:
                            setattr(employeeToSave,e, fileData[df[e][0]][i])
                        empExist = Employee.objects.filter(
                                employee_number=employeeToSave.employee_number)
                        if empExist:
                            if remplacement:
                                empExist.delete()
                                employeeToSave.save()
                                employeesSaved += 1
                        else:
                            employeeToSave.save()
                            employeesSaved += 1
    except XLRDError:
        result = "The file selected have not the right Excel format (xls or xlsx)"
    except TypeError as e:
        result = "Some values have not the right type: "+ str(e)
    except Exception as e:
        result = "An error occured when uploading the file: "+ str(e)
    finally:
        return result
    
def combinedCellLength(excel_file, paramSheetname,rangeCell):
    sheet_ranges = lw(excel_file)[paramSheetname]
    combinedCells = sheet_ranges.merged_cell_ranges
    firstCombCell =combinedCells[rangeCell]
    s= str(firstCombCell).split(":")[1][0]
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col = LETTERS.find(s) + 1
    return col

def attributesList (params, combCellLength):
    #{'name':['Prénom'],'surname':['Nom'], 'birth_date':['Date naissance'], 'employee_number':['Matricule']}
    attribList = {}
    for i in range(0,combCellLength):
        attribList[params.columns[i]]= [params[params.columns[i]][0]]
    return attribList

def checkAttributes(paramAttributes, modelAttributes,dataFileCols):
    result = "OK"
    for i in paramAttributes:
        if i not in modelAttributes:
            result = "One or more of the attributes defined in the parameters sheet did not correspond with the model: "+ str(modelAttributes)
    for i in paramAttributes:
        if paramAttributes[i][0] not in dataFileCols:
            result = "One or more ot the attributes defined in the parameters sheet did not correspond with the data sheet columns"
    return result

def webscrap():
    #URL = 'https://www.linkedin.com/pub/dir?firstName=javier&lastName=fernandez+fernandez&trk=homepage-jobseeker_people-search-bar_search-submit'
    URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=madrid'
    page = requests.get(URL)
    return page
 
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)