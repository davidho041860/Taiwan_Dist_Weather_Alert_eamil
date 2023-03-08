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
    return weather_list, str_weather, bring_umbrella

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
if __name__ == "__main__":

    # Sender email and google apps password
    my_email = "davidho041860@gmail.com"
    password = "hqcyrpugcskwowmo"

    # Enter district code for specific district and city code
    # 0-瑞芳 1-三重 2-平溪 3-淡水 4-石門 5-泰山 6-新店 7-萬里 8-蘆洲 9-永和 10-貢寮
    # 11-深坑 12-鶯歌 13-坪林 14-板橋 15-八里 16-土城 17-三芝 18-汐止 19-新莊 20-金山
    # 21-林口 22-中和 23-雙溪 24-五股 25-三峽 26-樹林 27-烏來 28-石碇
    district_code = 6
    # 0-新竹縣 1-金門縣 2-苗栗縣 3-新北市 4-宜蘭縣 5-雲林縣 6-台南市 7-高雄市 8-彰化縣 9-台北市 10-南投縣
    # 11-澎湖縣 12-基隆市 13-桃園市 14-花蓮縣 15-連江縣 16-台東縣 17-嘉義市 19-嘉義縣 19-屏東縣 20-台中市 21-新竹市
    city_code = 9

    # You can enter multiple mail receiver
    receiever = ["davidho041860@gmail.com"]

    # Generate tomorrow date
    today = datetime.now()
    tomorrow = today + timedelta(1)
    print("Today Date :", today.strftime('%Y-%m-%d'))
    print("Tomorrow Date :", tomorrow.strftime('%Y-%m-%d'))
    tomorrow_date = tomorrow.strftime('%Y-%m-%d')

    # Taiwan weather api address
    OWM_Endpoint_NewTaipei_district = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069"
    OWM_Endpoint_city = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-089"

    weather_params = {
        "Authorization" : "CWB-F9B11217-1E1A-4927-9491-A1D14EA5B3A1",
        "format" : "JSON",
    }

    # Request NewTaipei district weather
    response_NewTaipei_dis = requests.get(OWM_Endpoint_NewTaipei_district, params=weather_params)
    response_NewTaipei_j_dis = response_NewTaipei_dis.json()

    # Request Taiwan city weather
    response_City = requests.get(OWM_Endpoint_city, params=weather_params)
    response_City_j = response_City.json()

    weather_district = response_NewTaipei_j_dis["records"]["locations"][0]["location"][district_code]["weatherElement"]
    District_total_weather_condition = weather_district[1]["time"]
    District_total_temperature = weather_district[2]["time"]

    City_weather = response_City_j["records"]["locations"][0]["location"][district_code]["weatherElement"]
    City_total_weather_condition = City_weather[1]["time"]
    City_total_temperature = City_weather[2]["time"]

    # Grab weather detail
    District_weather_list, District_str_weather, District_Bring_umbrella = grab_weather_details( District_total_weather_condition, District_total_temperature)
    City_weather_list, City_str_weather, City_Bring_umbrella = grab_weather_details( City_total_weather_condition, City_total_temperature)
    # Store weather detail
    District_str_weather = store_weather_detail(District_weather_list, District_Bring_umbrella, District_str_weather)
    City_str_weather = store_weather_detail(City_weather_list, City_Bring_umbrella, City_str_weather)

    # Print the result
    print(f"{response_NewTaipei_j_dis['records']['locations'][0]['location'][district_code]['locationName']}天氣預報\n{District_str_weather}")
    print(f"{response_City_j['records']['locations'][0]['location'][city_code]['locationName']}天氣預報\n{City_str_weather}")

    # Send the weather alert by email
    m = EmailMessage()
    m['X-Priority'] = '1'
    m['Subject'] = "明日天氣預報"
    m.set_content(f"Hi,\n\n{response_NewTaipei_j_dis['records']['locations'][0]['location'][district_code]['locationName']}天氣預報\n{District_str_weather}\n\n{response_City_j['records']['locations'][0]['location'][city_code]['locationName']}天氣預報\n{City_str_weather}")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Make secure
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(my_email,
                            receiever,
                            m.as_string())

