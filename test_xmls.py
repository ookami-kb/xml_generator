__author__ = 'eugene'
from lxml import etree
if __name__ == '__main__':
    parser = etree.XMLParser(encoding="cp1251")
    httpfile = '/home/eugene/test/diksi.xml'
    obj = etree.parse(httpfile, parser)
    dtd = etree.DTD(open('/home/eugene/test/npl.dtd'))
    dtd.validate(obj)
    httpfile = '/home/eugene/test/index.xml'
    obj = etree.parse(httpfile, parser)
    dtd = etree.DTD(open('/home/eugene/test/nol.dtd'))
    dtd.validate(obj)
    for error in dtd.error_log:
        print error.message