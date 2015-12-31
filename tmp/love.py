# -*- coding: utf-8 -*-

import requests
from lxml import html
from PIL import Image
from StringIO import StringIO

url = 'http://www.aiqig.com/31.html'

r = requests.get(url)

htm = html.fromstring(r.content)

images = htm.xpath('//div[@id="entry_font"]/ol/li[2]/p/img')

for i, image in enumerate(images):
    img_url = image.get('src')
    img_alt = image.get('alt')
    r = requests.get(img_url)
    im = Image.open(StringIO(r.content))
    im.save('hcr_%s.jpg' % i)

