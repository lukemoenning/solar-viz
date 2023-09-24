import csv


electric_vehicle_charging_array_area = 180/10.7639 # m^2
CAMBUS_array_area = 267.13/10.7639 # m^2

"""Calculate conversion efficiency of solar panel arrays
:param start: start date (year, month, day)
:param end: end date (year, month, day)
:param array: "electric_vehicle" or "CAMBUS"
:param radiance_type: "Clearsky DHI", "Clearsky DNI", "Clearsky GHI", "DHI", "DNI", or "GHI"
:return: conversion efficiency csv file
"""
def conversion_efficiency(start, end, array, radiance_type):
    pass