#!/usr/bin/env python3

from openai import OpenAI
client = OpenAI(api_key="") #Enter API key here

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import sys
import argparse

# Parse Arguments

def parseArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("method", help="Data Retrival Method", type=str, default='soup')
    parser.add_argument("url", help = "URL", type=str)

    default_model = "gpt-4o"
    parser.add_argument("-m", "--model", help="GPT model", type=str, default=default_model)

    default_content = "Summarise the given article in detail using bullet points: "
    parser.add_argument("-p", "--prompt", help="prompt", type=str, default=default_content)

    args = parser.parse_args()
    
    return args

# Quicker retrieval of website data
def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    return ''.join(soup.body.get_text().split())


# Slower retrieval of website data using selenium
def get_selenium_data(url):
    ChromeDriver = webdriver.Chrome()

    driver = ChromeDriver
    driver.get(url)
    
    while input("Enter to extract data"):
        pass

    page_source = driver.page_source
    driver.close()
    soup = BeautifulSoup(page_source, 'html.parser')
    return ''.join(soup.body.get_text().split())

# Function to analyse webpage
def analyse(soup_content, model, prompt):
    completion = client.beta.chat.completions.parse(
        model= model,
        messages=[
            {
                "role": "user",
                "content": prompt + soup_content
            },
        ],
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    args = parseArguments()

    if args.url == 'e' or args.url == 'enter':
        url = str(input("Enter url: "))
    else:
        url = args.url

    if str(args.method) == "soup":
        raw_data = get_data(url)
    elif str(args.method) == "selenium":
        raw_data = get_selenium_data(url)
    else:
        "Incorrect data retrieval method inputted. Try again!"
        sys.exit(0)

    summary = analyse(raw_data, args.model, args.prompt)
    print(summary)




