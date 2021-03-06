"""
Author: Ryan Aquino
Description: Scrape Amazon.com Best seller cellphone accessories Device Name, Ratings, Price and Image url then extracts
it in a xlsx format file.
"""
from bs4 import BeautifulSoup
import requests
import xlsxwriter


def get_details(item):
    """
    Helper function to get the scrape the name of the item

    :param item: html item
    :return: json details of item
    """
    sibling = item.find('span').find(class_='zg-item')
    device_name = sibling.find('a').get_text()
    rating = sibling.findAll('a')[2].get_text()
    price = sibling.find(class_='a-row').find('span').get_text()
    image_url = sibling.find('img')['src']

    item_details = {
        'name': device_name.strip(),
        'rating': rating.strip(),
        'price': price.strip(),
        'image': image_url.strip()
    }

    return item_details


def save_to_excel(data):
    """
    Save to excel

    :param data: list of dictionary per item
    :return: None
    """
    out_workbook = xlsxwriter.Workbook('output.xlsx')
    out_sheet = out_workbook.add_worksheet()

    out_sheet.write('A1', 'Device Name')
    out_sheet.write('B1', 'Rating')
    out_sheet.write('C1', 'Price')
    out_sheet.write('D1', 'Image')

    for item in range(len(data)):
        out_sheet.write(item+1, 0, data[item]['name'])
        out_sheet.write(item+1, 1, data[item]['rating'])
        out_sheet.write(item+1, 2, data[item]['price'])
        out_sheet.write(item+1, 3, data[item]['image'])

    out_workbook.close()


def scrape(url):
    """
    Scrape Amazon.com Best seller cellphone accessories

    :param url: url to be scraped
    :return: list of best seller cellphone accessories
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll(class_='zg-item-immersion')

    array_data = []

    for item in items:
        array_data.append(get_details(item))

    return array_data


if __name__ == '__main__':

    try:
        data = scrape('https://www.amazon.com/Best-Sellers-Cell-Phone-Accessories/zgbs/wireless/2407755011/ref=zg_bs_nav_1_wireless')
        save_to_excel(data)
        print('Completed!')

    except BaseException:
        print('Something went wrong!')
