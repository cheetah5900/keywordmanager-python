
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from django.shortcuts import render, redirect

from datetime import date,timedelta

# require login to enter function
# import model
from keywordapp.models import *

# =============================== FOR SELENIUM GET DATA ===============================
# =============================== FOR SELENIUM GET DATA ===============================
# =============================== FOR SELENIUM GET DATA ===============================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
# To setting mobile device broswer


# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================



def Work(request):
    context = {}
    headerList = []
    dateList = []
    contentList = []
    linkList = []

    # sort by last 7 days
    currentDate = date.today()
    lastSevenDays = currentDate-timedelta(days=7)
    data = ListOfWorkModel.objects.filter(date__range=[lastSevenDays,currentDate]).order_by('-date')


    for item in data:
        headerList.append(item.header)
        contentList.append(item.content)
        linkList.append(item.link)

        day = item.date.strftime("%d")
        month = item.date.strftime("%b")
        year = item.date.strftime("%Y")
        dateReFormat = "{} {} {}".format(day, month, year)
        dateList.append(dateReFormat)


    dataForLoop = zip(headerList,dateList,contentList,linkList)

    context['dataForLoop'] = dataForLoop
    return render(request, 'keywordapp/work.html', context)


def House(request):
    context = {}
    headerList = []
    dateList = []
    contentList = []
    linkList = []

    # sort by last 7 days
    currentDate = date.today()
    lastSevenDays = currentDate-timedelta(days=7)
    data = ListOfHouseModel.objects.filter(date__range=[lastSevenDays,currentDate]).order_by('-date')

    for item in data:
        headerList.append(item.header)
        contentList.append(item.content)
        linkList.append(item.link)

        day = item.date.strftime("%d")
        month = item.date.strftime("%b")
        year = item.date.strftime("%Y")
        dateReFormat = "{} {} {}".format(day, month, year)
        dateList.append(dateReFormat)


    dataForLoop = zip(headerList,dateList,contentList,linkList)

    context['dataForLoop'] = dataForLoop
    return render(request, 'keywordapp/house.html', context)


# =============================== WORK ===============================
# =============================== WORK ===============================
# =============================== WORK ===============================

def RefreshWork(request):

    # Delete temp link before start anything
    TempLinkOfWorkModel.objects.all().delete()

    # Open in mobile
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1'
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent="+ua)

    # local
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    driver.get('https://sydneythai.info/jobs.php')

    # if cannot find searchBoxHomePage will re-open browser
    checkElement = True
    while checkElement == True:
        try:
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.find_element(By.CLASS_NAME, 'feature-box'))
            checkElement = False
        except:
            print("Cannot find feature-box")
            driver.quit()
            checkElement = False
    link = driver.find_elements(By.CSS_SELECTOR, 'div.feature-box-info > h4.shorter > a')

    # Call all data for checking
    ListOfWork = ListOfWorkModel.objects.all()
    countListOfWork = ListOfWork.count()

    for x in link:
        tempLink = x.get_attribute('href')
        if countListOfWork == 0:
                newListOfWork = TempLinkOfWorkModel()
                newListOfWork.link = tempLink
                newListOfWork.save()
        else:
            for y in ListOfWork:
                if tempLink == y.link:
                    try:
                        TempLinkOfWorkModel.objects.get(link=tempLink).delete()
                    except:
                        pass
                
            newListOfWork = TempLinkOfWorkModel()
            newListOfWork.link = tempLink
            newListOfWork.save()


    driver.quit()

    # CollectWorkFromDB(request)

    return redirect('work')



def CollectWorkFromDB(request):

    # Open in mobile
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1'
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent="+ua)

    # local
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)


    # Call all data for looping
    tempLinkOfWork = TempLinkOfWorkModel.objects.all()
    for x in tempLinkOfWork:
        tempLink = x.link
        driver.get(tempLink)
        try:
            WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')
        date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')
        content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')

        dateText = date.text
        dateOnly = dateText[0:2]

        #Convert text to number to check
        dateToInt = int(dateOnly)

        if dateToInt <= 9:
            monthOnly = dateText[2:5]
            yearOnly = dateText[6:10]
        else:
            monthOnly = dateText[3:6]
            yearOnly = dateText[7:11]

        #Convert text to number
        yearToInt = int(yearOnly)
        monthToInt = ConvertMonthToNumber(monthOnly)


        # Add data
        newListOfWork = ListOfWorkModel()
        newListOfWork.link = tempLink
        newListOfWork.header = header.text
        newListOfWork.date = "{}-{}-{} 00:00:00".format(yearToInt,monthToInt,dateToInt)
        newListOfWork.content = content.text
        newListOfWork.save()


    driver.quit()
    return redirect('work')



# =============================== WORK ===============================
# =============================== WORK ===============================
# =============================== WORK ===============================

def RefreshHouse(request):

    # Delete temp link before start anything
    TempLinkOfHouseModel.objects.all().delete()
    # Open in mobile
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1'
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent="+ua)

    # local
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    driver.get('https://sydneythai.info/house.php')

    # if cannot find searchBoxHomePage will re-open browser
    checkElement = True
    while checkElement == True:
        try:
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.find_element(By.CLASS_NAME, 'feature-box'))
            checkElement = False
        except:
            print("Cannot find feature-box")
            driver.quit()
            checkElement = False
    link = driver.find_elements(By.CSS_SELECTOR, 'div.feature-box-info > h4.shorter > a')

    # Call all data for checking
    ListOfHouse = ListOfHouseModel.objects.all()
    countListOfHouse = ListOfHouse.count()

    for x in link:
        tempLink = x.get_attribute('href')
        tempId = x.id
        if countListOfHouse == 0:
                newListOfHouse = TempLinkOfHouseModel()
                newListOfHouse.link = tempLink
                newListOfHouse.save()
        else:
            for y in ListOfHouse:
                if tempLink == y.link:
                    try:
                        TempLinkOfHouseModel.objects.get(link=tempLink).delete()
                    except:
                        pass
                
            newListOfHouse = TempLinkOfHouseModel()
            newListOfHouse.link = tempLink
            newListOfHouse.save()

    driver.quit()

    CollectHouseFromDB(request)

    return redirect('house')

def CollectHouseFromDB(request):

    # Open in mobile
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1'
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent="+ua)

    # local
    driver = webdriver.Chrome("/Users/chaperone/Documents/GitHub/keywordmanager-python/chromedriver",options=options)

    # Call all data for looping

    tempLinkOfHouse = TempLinkOfHouseModel.objects.all()
    for x in tempLinkOfHouse:
        tempLink = x.link

        driver.get(tempLink)
        try:
            WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')
        date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')
        content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')

        dateText = date.text
        dateOnly = dateText[0:2]

        #Convert text to number to check
        dateToInt = int(dateOnly)

        if dateToInt <= 9:
            monthOnly = dateText[2:5]
            yearOnly = dateText[6:10]
        else:
            monthOnly = dateText[3:6]
            yearOnly = dateText[7:11]

        #Convert text to number
        yearToInt = int(yearOnly)
        monthToInt = ConvertMonthToNumber(monthOnly)

        # Add data
        newListOfHouse = ListOfHouseModel()
        newListOfHouse.link = tempLink
        newListOfHouse.header = header.text
        newListOfHouse.date = "{}-{}-{} 00:00:00".format(yearToInt,monthToInt,dateToInt)
        newListOfHouse.content = content.text
        newListOfHouse.save()

    driver.quit()

    return redirect('house')

def ConvertMonthToNumber(monthOnly):
    if monthOnly == 'Jan':
        result = 1
    elif monthOnly == 'Feb':
        result = 2
    elif monthOnly == 'Mar':
        result = 3
    elif monthOnly == 'Apr':
        result = 4
    elif monthOnly == 'May':
        result = 5
    elif monthOnly == 'Jun':
        result = 6
    elif monthOnly == 'Jul':
        result = 7
    elif monthOnly == 'Aug':
        result = 8
    elif monthOnly == 'Sep' or monthOnly == 'Sept':
        result = 9
    elif monthOnly == 'Oct':
        result = 10
    elif monthOnly == 'Nov':
        result = 11
    elif monthOnly == 'Dec':
        result = 12
    else:
        result = 99
    return result
