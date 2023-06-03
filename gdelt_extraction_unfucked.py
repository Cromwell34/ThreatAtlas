import csv
import pandas as pd
import os
from datetime import datetime, timedelta, date

start_date = datetime(2023, 2, 5)
end_date = datetime(2023, 2, 6)
header = "GLOBALEVENTID SQLDATE MonthYear Year FractionDate Actor1Code Actor1Name Actor1CountryCode Actor1KnownGroupCode Actor1EthnicCode Actor1Religion1Cod Actor1Religion2Code Actor1Type1Code Actor1Type2Code Actor1Type3Code Actor2Code Actor2Name Actor2CountryCode Actor2KnownGroupCode Actor2EthnicCode Actor2Religion1Code Actor2Religion2Code Actor2Type1Code Actor2Type2Code Actor2Type3Code IsRootEvent EventCode EventBaseCode EventRootCode QuadClass GoldsteinScale NumMentions NumSources NumArticles AvgTone Actor1Geo_Type Actor1Geo_FullName Actor1Geo_CountryCode Actor1Geo_ADM1Code Actor1Geo_Lat Actor1Geo_Long Actor1Geo_FeatureID Actor2Geo_Type Actor2Geo_FullName Actor2Geo_CountryCode Actor2Geo_ADM1Code Actor2Geo_Lat Actor2Geo_Long Actor2Geo_FeatureID ActionGeo_Type ActionGeo_FullName ActionGeo_CountryCode ActionGeo_ADM1Code ActionGeo_Lat ActionGeo_Long ActionGeo_FeatureID DATEADDED SOURCEURL".split(
    " "
)
import os
from zipfile import ZipFile
import pandas as pd


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


days = [str(day.strftime("%Y%m%d")) for day in date_range(start_date, end_date)]

with open("gdelt_extraction/cameo_dict.csv", mode="r", encoding="utf-8") as inp:
    reader = csv.reader(inp)
    cameo_dict = {rows[0]: rows[2] for rows in reader}

test_dir = os.listdir("gdelt_extraction/results")
for f in test_dir:
    convert_dict = {"EventCode": str}

    df2 = pd.read_csv("gdelt_extraction/results/" + f)
    df2 = df2.astype(convert_dict)
    df2.replace({"EventCode": cameo_dict}, inplace=True)

    print(df2["EventCode"])
    df2.to_csv("gdelt_extraction/results_cleaned/" + f + "_coded" + ".csv")


print("Unzipping files")
test_dir = os.listdir("gdelt_extraction/dump")
for n in test_dir:
    with ZipFile("gdelt_extraction/dump/" + n, "r") as zipObj:
        zipObj.extractall("gdelt_extraction/dump")

print("Adding headers")
# process and save files
test_dir = os.listdir("gdelt_extraction/dump")
for p in test_dir:
    if ".CSV" in p:
        data_test = pd.read_csv(
            "gdelt_extraction/dump/" + p, delimiter="\t", names=header
        )
        data_test.to_csv("gdelt_extraction/results/" + p + "_processed" + ".csv")
