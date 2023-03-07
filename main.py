import requests
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

def grab_weather_details( total_weather_condition, total_temperature):
    weather_list = []
    bring_umbrella = False
    cold_temperature_count = []
    for x in range(0, 23):
        if total_weather_condition[x]["startTime"][0:10] == tomorrow_date:
            if int(total_weather_condition[x]["startTime"][-8:-6]) % 6 == 0 and int(
                    total_weather_condition[x]["startTime"][-8:-6]) >= 6:
                weather_list.append(str(total_weather_condition[x]["startTime"][5:-3]))
                weather_list.append(total_temperature[x]["elementValue"][0]["value"] + chr(176) + " " + str(
                    total_weather_condition[x]["elementValue"][0]["value"]))
                if bring_umbrella == False and int(total_weather_condition[x]["elementValue"][1]["value"]) >= 8:
                    bring_umbrella = True
                cold_temperature_count.append(int(total_temperature[x]["elementValue"][0]["value"]))
    str_weather = ""
    str_weather += f"最低溫\U00002744: {min(cold_temperature_count)} | 最高溫\U0001F525: {max(cold_temperature_count)}"
    str_weather += "\n"
    return weather_list, str_weather ,bring_umbrella

def  store_weather_detail(weather_list, Bring_umbrella, str_weather):
    if Bring_umbrella == True:
        str_weather += "天氣不佳，記得帶雨傘\U00002614"
        str_weather += "\n\n"
    else:
        str_weather += "天氣不錯，不用帶雨傘\U0001F302"
        str_weather += "\n\n"

    for i in range(len(weather_list)):
        if i % 2 == 0:
            str_weather += str(weather_list[i])
            str_weather += "\n"
        if i % 2 == 1:
            str_weather += str(weather_list[i])
            str_weather += "\n"
    return str_weather

#Sender email and google apps password
my_email = "davidho041860@gmail.com"
password = "hqcyrpugcskwowmo"

#You can enter multiple mail receiver
receiever = ["davidho041860@gmail.com"]

#Generate tomorrow date
today = datetime.now()
tomorrow = today + timedelta(1)
print("Today Date :", today.strftime('%Y-%m-%d'))
print("Tomorrow Date :", tomorrow.strftime('%Y-%m-%d'))
tomorrow_date = tomorrow.strftime('%Y-%m-%d')

#Taiwan weather api address
OWM_Endpoint_NewTaipei_district = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069"
OWM_Endpoint_city = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-089"

weather_params = {
    "Authorization" : "CWB-F9B11217-1E1A-4927-9491-A1D14EA5B3A1",
    "format" : "JSON",
}

#Request NewTaipei district weather
response_NewTaipei_dis = requests.get(OWM_Endpoint_NewTaipei_district, params=weather_params)
response_NewTaipei_j_dis = response_NewTaipei_dis.json()

#Request Taiwan city weather
response_City = requests.get(OWM_Endpoint_city, params=weather_params)
response_City_j = response_City.json()

#Enter district code for specfic district
district_code = 6
weather_HSINTIEN = response_NewTaipei_j_dis["records"]["locations"][0]["location"][district_code]["weatherElement"]
HSINTIEN_total_weather_condition = weather_HSINTIEN[1]["time"]
HSINTIEN_total_temperature = weather_HSINTIEN[2]["time"]

#Enter city code for specfic district
city_code = 9
weather_Taipei = response_City_j["records"]["locations"][0]["location"][district_code]["weatherElement"]
Taipei_total_weather_condition = weather_Taipei[1]["time"]
Taipei_total_temperature = weather_Taipei[2]["time"]

HSINTIEN_weather_list, HSINTIEN_str_weather, HSINTIEN_Bring_umbrella = grab_weather_details( HSINTIEN_total_weather_condition, HSINTIEN_total_temperature)
Taipei_weather_list, Taipei_str_weather, Taipei_Bring_umbrella = grab_weather_details( Taipei_total_weather_condition, Taipei_total_temperature)

HSINTIEN_str_weather = store_weather_detail(HSINTIEN_weather_list, HSINTIEN_Bring_umbrella, HSINTIEN_str_weather)
Taipei_str_weather = store_weather_detail(Taipei_weather_list, Taipei_Bring_umbrella, Taipei_str_weather)

print(f"{response_NewTaipei_j_dis['records']['locations'][0]['location'][district_code]['locationName']}天氣預報\n{HSINTIEN_str_weather}")
print(f"{response_City_j['records']['locations'][0]['location'][city_code]['locationName']}天氣預報\n{Taipei_str_weather}")

m = EmailMessage()

m['X-Priority'] = '1'
m['Subject'] = "明日天氣預報"
m.set_content(f"Hi,\n\n{response_NewTaipei_j_dis['records']['locations'][0]['location'][district_code]['locationName']}天氣預報\n{HSINTIEN_str_weather}\n\n{response_City_j['records']['locations'][0]['location'][city_code]['locationName']}天氣預報\n{Taipei_str_weather}")

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()  ##Make secure
    connection.login(user=my_email, password=password)
    connection.sendmail(my_email,
                        receiever,
                        m.as_string())

