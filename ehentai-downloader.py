from bs4 import BeautifulSoup
import urllib.request, sys, os

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')]
urllib.request.install_opener(opener)

def make_req(url):
    return urllib.request.urlopen(url).read().decode('utf-8')

def get_power(remainder):
    power_of_number = 0
    while remainder >= 10:
        remainder /= 10
        power_of_number += 1
    return power_of_number


def download_image(url, directory, number, max_zeros):
    number_string = ""
    remainder = number
    power_of_number = get_power(number)
    for _ in range(max_zeros - power_of_number):
        number_string += "0"
    number_string += str(number)
    urllib.request.urlretrieve(url, directory + '/' + number_string + '.jpg')

def find_image_link(site):
    image = site.find(id="img")
    return(image['src'])

def find_first_img(site):
    images = site.find_all('img')
    for i in images:
        if i.get('alt') == '01':
            return i.parent.get('href')

def get_next_link(site):
    next_link = site.find(id="next")
    return next_link['href']

def main():
    site = BeautifulSoup(make_req(sys.argv[1]), 'html.parser')
    title = site.find(id="gn").string
    images = []
    current_img_site = find_first_img(site)
    previous_img_site = ""
    site = BeautifulSoup(make_req(current_img_site), 'html.parser')
    
    
    while current_img_site not in previous_img_site:
        images.append(find_image_link(site))
        previous_img_site = current_img_site
        current_img_site = get_next_link(site)
        site = BeautifulSoup(make_req(current_img_site), 'html.parser')

    number_of_images = len(images)

    CHECK_FOLDER = os.path.isdir(title)

    if not CHECK_FOLDER:
        os.makedirs(title)
        print("created folder : ", title)

    for i in range(number_of_images):
        download_image(images[i], title, i, get_power(number_of_images))

if __name__ == "__main__":
    main()
