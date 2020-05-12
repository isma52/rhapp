# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 09:53:59 2020

@author: iamor
"""

from django.forms import DateTimeInput

class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/xdsoft_datetimepicker.html'