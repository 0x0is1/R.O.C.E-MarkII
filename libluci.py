import requests
import re
from bs4 import BeautifulSoup as bs
import urllib.parse
import random


error_key = {
    0: "Your browsing activity is empty.",
    1: "Error404"
}

# collector commands


def soup_collector(item_id, item_type):
    url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=" + item_id + "&db=" + item_type + \
        "&report=genbank&extrafeat=null&conwithfeat=on&retmode=html&tool=portal&withmarkup=on&maxdownloadsize=1000000000000"
    data = requests.get(url)
    soup = bs(data.content, 'html.parser')

    # killing javascripts and stylesheets
    for script in soup(["script", "style"]):
        script.decompose()
    return soup


def name_collector(soup):
    span = soup.find_all('span', {'class': 'feature'})[0]
    return span.get('id').split('feature_')[1].split('_source')[0]

# get commands


def intro(soup):
    try:
        raw_intro = soup.findAll('pre', {"class": 'genbank'})[
            0].text.replace('<a href="', '').replace('">', ' - ').replace('</a>', '')

        i = re.findall(r'(?<=LOCUS)[\S\s]*(?=COMMENT)', raw_intro)
        return str(i[0]).replace('  ', '')
    except Exception as e:
        print(e)
        return 'No intro found.'


def feature_cds(soup, count):
    iterator = 0
    value = []

    name = name_collector(soup)
    while iterator <= count-1:
        cds = soup.find('span', {"id": "feature_" +
                                 name + "_CDS_" + str(iterator)})
        if cds == None:
            break
        value.append(str(cds.text).replace('  ', ''))
        iterator += 1
    return value


def feature_source(soup, count):

    name = name_collector(soup)
    value = []
    iterator = 0
    while iterator <= count-1:
        source = soup.find(
            'span', {"id": "feature_" + name + "_source_" + str(iterator)})
        if source == None:
            break
        value.append(str(source.text).replace('  ', ''))
        iterator += 1
    return value


def feature_peptide(soup, count):

    name = name_collector(soup)
    value = []
    iterator = 0
    while iterator <= count-1:
        peptide = soup.find(
            'span', {"id": "feature_" + name + "_mat_peptide_" + str(iterator)})
        if peptide == None:
            break
        value.append(str(peptide.text).replace('  ', ''))
        iterator += 1
    return value


def feature_stem_loop(soup, count):
    value = []
    iterator = 0

    name = name_collector(soup)
    while iterator <= count-1:
        stem_loop = soup.find(
            'span', {"id": "feature_" + name + "_stem_loop_" + str(iterator)})
        if stem_loop == None:
            break
        value.append(str(stem_loop.text).replace('  ', ''))
        iterator += 1
    return value


def chain_sequence(soup, count):
    value = []
    iterator = 1

    name = name_collector(soup)
    while iterator <= count*60:
        source = soup.find(
            'span', {"id": name + "_" + str(iterator)})
        if source == None:
            break
        iterator += 60
        value.append(str(source.text).replace('  ', ''))
    return value


def feature_gene(soup, count):
    value = []
    iterator = 0

    name = name_collector(soup)
    while iterator <= count-1:
        gene = soup.find(
            'span', {"id": "feature_" + name + "_gene_" + str(iterator)})
        if gene == None:
            break
        value.append(str(gene.text).replace('  ', ''))
        iterator += 1
    return value


def comment(soup):
    try:
        raw_intro = soup.findAll('pre', {"class": 'genbank'})[
            0].text.replace('<a href="', '').replace('">', ' - ').replace('</a>', '')

        i = re.findall(r'(?<=COMMENT)[\S\s]*(?=FEATURES)', raw_intro)
        return str(i[0]).replace('   ', '')
    except Exception:
        return 'No comments found.'


def formal():
    print('Welcome to the Bio-samples framework')
    print('National Center for BioTechnology Information')
    print('(https://www.ncbi.nlm.nih.gov)')
    print('')
    print('Enter commands to interact with')
    print('Type Help to see available commands')

# search commands


def search_id_list(name, filter1, filter2, category_type):
    term = urllib.parse.quote(name)

    cookies = {
        'ncbi_sid': 'CE8C4638E6FC4D21_099'+str(random.randint(0000, 100000))+'SID',
    }
    requests.get('https://www.ncbi.nlm.nih.gov/' +
                 category_type + '/?term=' + term, cookies=cookies)
    headers = {
        'Host': 'www.ncbi.nlm.nih.gov',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
    }

    data = 'EntrezSystem2.PEntrez.' + filter1 + '.' + filter2 + '_ResultsPanel.' + filter2 + '_DisplayBar.Presentation=uilist&EntrezSystem2.PEntrez.' + filter1 + \
        '.' + filter2 + '_ResultsPanel.Entrez_Pager.CurrPage=1&EntrezSystem2.PEntrez.DbConnector.LastQueryKey=1&EntrezSystem2.PEntrez.DbConnector.Cmd=displaychanged'

    response = requests.post('https://www.ncbi.nlm.nih.gov/' + category_type,
                             headers=headers, cookies=cookies, data=data, verify=True)
    soup = bs(response.content, 'html.parser')
    if error_key[0] in soup.text:
        return "No result found"
    if error_key[1] in soup.text:
        return "Error404 no such items"
    else:
        return soup.text


def search_detail(name, category_type):
    term = urllib.parse.quote(name)
    url = 'https://www.ncbi.nlm.nih.gov/' + category_type + \
        '/?term=' + term + '&report=docsum&format=text'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    if error_key[0] in soup.text:
        return "No result found"
    if error_key[1] in soup.text:
        return "Error404 no such items"
    else:
        return soup.text


sample_id = 469716625  # SARS_CoV-2 sample-id 1798174254
sample_type = "nuccore"  # nucleotide
print(name_collector(soup_collector(str(sample_id), sample_type)))
#print(search_id_list('sars', 'Gene', 'Gene', 'gene'))
