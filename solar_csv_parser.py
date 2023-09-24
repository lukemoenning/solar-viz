import numpy as np
import time
import csv


input_to_column_dict = {"Clearsky DHI":6, "Clearsky DNI":7, "Clearsky GHI":8, "DHI":11, "DNI":12, "GHI":14}
year_to_csv_dict = {2011:'9degrees2011-2021/2011-813957-fixed_tilt.csv', 
                    2012:"9degrees2011-2021/2012-813957-fixed_tilt.csv", 
                    2013:"9degrees2011-2021/2013-813957-fixed_tilt.csv",
                    2014:"9degrees2011-2021/2014-813957-fixed_tilt.csv", 
                    2015:"9degrees2011-2021/2015-813957-fixed_tilt.csv", 
                    2016:"9degrees2011-2021/2016-813957-fixed_tilt.csv", 
                    2017:"9degrees2011-2021/2017-813957-fixed_tilt.csv", 
                    2018:"9degrees2011-2021/2018-813957-fixed_tilt.csv", 
                    2019:"9degrees2011-2021/2019-813957-fixed_tilt.csv",
                    2020:"9degrees2011-2021/2020-813957-fixed_tilt.csv",
                    2021:"9degrees2011-2021/2021-813957-fixed_tilt.csv"}
# radiance_types = ("Clearsky DHI", "Clearsky DNI", "Clearsky GHI", "DHI", "DNI", "GHI")
years = [2011 ,2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
def create_daily_average_csv():
    for year in years:
      daily_sum = {}
      output = []
      i=0
      with open(year_to_csv_dict[year], 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
          if i > 2:  
            for index in [6,7,8,11,12,14]:
              if index not in daily_sum:
                daily_sum[index] = float(row[index])
              else:
                daily_sum[index] += float(row[index])
            if (i-2) % 24 == 0:
              output.append([int(row[1]), int(row[2]), float(daily_sum[6])/24, float(daily_sum[7])/24, float(daily_sum[8])/24, float(daily_sum[11])/24, float(daily_sum[12])/24, float(daily_sum[14])/24])
              for index in [6,7,8,11,12,14]:
                daily_sum[index] = float(row[index])
            i += 1
          else:
            i += 1

      with open(f'averages/{year}-daily_average.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in output:
          csvwriter.writerow(row)
      

def combine_years_to_csv():
  with open("averages/30_degree_fixed_tilt.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Year", "Month", "Day", "CS_DHI", "CS_DNI", "CS_GHI", "DHI", "DNI", "GHI"])
    for year in years:
      with open(f'9degree_averages/{year}-daily_average.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
          csvwriter.writerow([year]+row)
      
if __name__ =="__main__":
  # create_daily_average_csv()
  combine_years_to_csv()