
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from datetime import datetime
# from textwrap import shorten
# from xml.etree.ElementTree import SubElement
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from uuid import uuid1


# require login to enter function
from django.contrib.auth.decorators import login_required
# import model
from keywordapp.models import *
# ให้สามารถเก็บไฟล์ได้
from django.core.files.storage import FileSystemStorage
# AJAX เขียนแบบ Class-Based
from django.views.generic import View  # ให้ใช้ ListView ได้
from django.http import JsonResponse
from collections import Counter  # เอาไว้นับจำนวนคำใน list


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
    dataForLoop = TempListOfWorkModel.objects.all().order_by('-date')
    context['dataForLoop'] = dataForLoop
    return render(request, 'keywordapp/work.html', context)


def House(request):
    context = {}
    dataForLoop = TempListOfHouseModel.objects.all().order_by('-date')
    context['dataForLoop'] = dataForLoop
    return render(request, 'keywordapp/house.html', context)


# =============================== WORK ===============================
# =============================== WORK ===============================
# =============================== WORK ===============================

def RefreshWork(request):

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



    TempListOfWorkModel.objects.all().delete()
    for x in link:
        linkHref = x.get_attribute('href')
        print("linkHref: "+linkHref)
        
        newTempListOfWork = TempListOfWorkModel()
        newTempListOfWork.link = linkHref
        newTempListOfWork.save()


    driver.quit()

    CollectWorkFromDB(request)

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
    TempListOfWorkModelObject = TempListOfWorkModel.objects.all()

    for x in TempListOfWorkModelObject:
        link = x.link
        id = x.id

        driver.get(link)
        try:
            WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')
        date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')
        content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')

        # driver.close()

        dateText = date.text
        dateOnly = dateText[0:11]

        # Edit data
        updateData = TempListOfWorkModel.objects.get(id=id)
        updateData.header = header.text
        updateData.date = dateOnly
        updateData.content = content.text
        updateData.save()


    driver.quit()
    return redirect('work')



# =============================== WORK ===============================
# =============================== WORK ===============================
# =============================== WORK ===============================

def RefreshHouse(request):

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

    TempListOfHouseModel.objects.all().delete()
    for x in link:
        linkHref = x.get_attribute('href')
        
        newTempListOfHouse = TempListOfHouseModel()
        newTempListOfHouse.link = linkHref
        newTempListOfHouse.save()

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
    TempListOfHouseModelObject = TempListOfHouseModel.objects.all()

    for x in TempListOfHouseModelObject:
        link = x.link
        id = x.id

        driver.get(link)
        try:
            WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '#post-content > h3'))
        except:
            print("cannot find #post-content > h3")

        header = driver.find_element(By.CSS_SELECTOR, '#post-content > h3')
        date = driver.find_element(By.CSS_SELECTOR, '#post-content > h3 + p')
        content = driver.find_element(By.CSS_SELECTOR, '#post-content > p.post-body')

        # driver.close()

        dateText = date.text
        dateOnly = dateText[0:11]

        # Edit data
        updateData = TempListOfHouseModel.objects.get(id=id)
        updateData.header = header.text
        updateData.date = dateOnly
        updateData.content = content.text
        updateData.save()


    driver.quit()

    return redirect('house')

