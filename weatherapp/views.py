from django.http import HttpResponse
import requests
import json
from datetime import datetime
from django.shortcuts import render


def index(request):

    return render(request, "index.htm")


def own_location(request):
    lat = request.GET['lat']
    lng = request.GET['lng']
    params = {}
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid=c7285183b875cd7afb4f1a4a5ed660ff"
    res = requests.get(url).text
    resp = json.loads(res)
    desc = resp['weather'][0]['description']
    desc = desc.capitalize()
    temp = resp["main"]["temp"]
    temp = f"{temp}°C"
    feelslike = resp["main"]["feels_like"]
    feelslike = f"{feelslike}°C"
    pressure = resp["main"]["pressure"]
    pressure = f"{pressure} Pa"
    humidity = resp["main"]["humidity"]
    humidity = f"{humidity}%"
    windspeed = resp["wind"]["speed"]
    windspeed = f"{windspeed}KM/H"
    sunr = resp["sys"]["sunrise"]
    sunset = resp["sys"]["sunset"]
    sunrise = datetime.fromtimestamp(sunr)
    sunset = datetime.fromtimestamp(sunset)
    sunrise = sunrise.strftime("%X")
    sunset = sunset.strftime("%X")
    city = resp["name"]

    params = {"city": f"Today's Weather of {city}", "description": desc, "temparature": f"Temperature {temp}", "feelslike": f"Feels Like {feelslike}",
              "pressure": f"Pressure {pressure}", "humidity": f"Humidity {humidity}", "windspeed": f"Windspeed {windspeed}",
              "sunrise": f"Sunrise {sunrise}", "sunset": f"Sunset {sunset}"
              }

    return HttpResponse(json.dumps(params))


def today(request):
    City = request.GET['city']
    print(City)
    params = {}
    if City != "select":
        url = f"http://api.openweathermap.org/data/2.5/weather?q={City}&units=metric&appid=c7285183b875cd7afb4f1a4a5ed660ff"
        res = requests.get(url).text
        resp = json.loads(res)
        print(resp)
        desc = resp['weather'][0]['description']
        print(desc)
        desc = desc.capitalize()
        print(desc)

        temp = resp["main"]["temp"]
        temp = f"{temp}°C"
        feelslike = resp["main"]["feels_like"]
        feelslike = f"{feelslike}°C"
        pressure = resp["main"]["pressure"]
        pressure = f"{pressure} Pa"
        humidity = resp["main"]["humidity"]
        humidity = f"{humidity}%"
        windspeed = resp["wind"]["speed"]
        windspeed = f"{windspeed}KM/H"
        sunr = resp["sys"]["sunrise"]
        sunset = resp["sys"]["sunset"]
        sunrise = datetime.fromtimestamp(sunr)
        sunset = datetime.fromtimestamp(sunset)
        sunrise = sunrise.strftime("%X")
        sunset = sunset.strftime("%X")

        print(temp)
        print(feelslike)
        print(pressure)
        print(humidity)
        print(windspeed)
        print(sunrise)
        print(sunset)
        params = {"city": f"Today's Weather of {City}", "description": desc, "temparature": f"Temperature {temp}", "feelslike": f"Feels Like {feelslike}",
                  "pressure": f"Pressure {pressure}", "humidity": f"Humidity {humidity}", "windspeed": f"Windspeed {windspeed}",
                  "sunrise": f"Sunrise {sunrise}", "sunset": f"Sunset {sunset}"
                  }
    else:
        params = {"city": "You didn't select any city", "description": "", "temparature": "", "feelslike": "",
                  "pressure": "", "humidity": "", "windspeed": "",
                  "sunrise": "", "sunset": ""
                  }
    # return render(request,"index.htm",params)
    # print(json.dumps(params))
    return HttpResponse(json.dumps(params))


def forecast(request):
    city2 = request.GET['city']
    date = request.GET['date']
    parameter = {}
    if city2 != "select" or date != "":
        url2 = f"http://api.openweathermap.org/data/2.5/forecast?q={city2}&units=metric&appid=c7285183b875cd7afb4f1a4a5ed660ff"
        fore = requests.get(url2).text
        forec = json.loads(fore)
        forecastslist = forec['list']

        l = len(forecastslist)

        desc = ""
        temp = ""
        feelslike = ""
        pressure = ""
        humidity = ""
        windspeed = ""
        params = {}
        for i in range(1, l, 7):
            date2 = forecastslist[i]['dt_txt'].split(" ")[0]
            desc = forecastslist[i]['weather'][0]['description']
            desc = desc.capitalize()

            temp = f"{forecastslist[i]['main']['temp']}°C"
            feelslike = f"{forecastslist[i]['main']['feels_like']}°C"
            pressure = f"{forecastslist[i]['main']['pressure']} Pa"
            humidity = f"{forecastslist[i]['main']['humidity']}%"
            windspeed = f"{forecastslist[i]['wind']['speed']} KM/H"
            wthr = {"city2": city2,
                    "desc": desc, "temp": f"Temperature {temp}",
                    "feels": f"Feels Like {feelslike}", "press": f"Pressure {pressure}",
                    "humi": f"Humidity {humidity}", "winds": f"Windspeed {windspeed}"

                    }

            params[date2] = wthr
            print(wthr)

        for i in params:
            if date == i:
                parameter = params[i]
                parameter["date"] = i
            '''else:
                parameter ={"city2":"Select valid date",
                           "desc":"","temp":"",
                            "feels":"","press":"",
                             "humi":"","winds":"",
                             "date":""

                     }'''
    else:
        parameter = {"city2": "You didn't select any city",
                     "desc": "", "temp": "",
                     "feels": "", "press": "",
                     "humi": "", "winds": "",
                     "date": ""

                     }

    return HttpResponse(json.dumps(parameter))
