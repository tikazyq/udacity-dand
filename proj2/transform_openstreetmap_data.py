"""
The data is downloaded from https://mapzen.com/data/metro-extracts.
Search by "london, england" and select OSM XML. The unzipped raw data
is called london_england.osm
"""
from datetime import datetime
import xml.etree.cElementTree as ET
from pprint import pprint
import re
import codecs
import json
from postcode import uk


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
INFO = ['website']
TAG_KEY_PREFIXES = ['addr', 'naptan']

SOURCE_MAPPING = {
    'Bing': 'bing',
    'Yahoo': 'yahoo',
    'Wikipedia': 'wikipedia',
    'GPS': 'gps',
    'Landsat': 'landsat',
    'Local': 'local',
    'NaPTAN': 'naptan',
    'NLS': 'nls',
    'NPE': 'npe',
    'Observation': 'observation',
    'OS Open Data': ['os', '1:25k'],
    'Survey': 'survey',
    'Campus': 'campus map',
    'PGS': 'pgs',
    'Website': 'http|www\.',
}


def trans_pos(k, v, node):
    if node.get('pos') is None:
        node['pos'] = []
    if k == 'lat':
        node['pos'].insert(0, float(v))
    elif k == 'lon':
        node['pos'].append(float(v))
    return node


def trans_attr(element, node):
    for k, v in element.attrib.iteritems():
        if k in CREATED:
            if node.get('created') is None:
                node['created'] = {}
            node['created'][k] = v
        elif k in ['lat', 'lon']:
            node = trans_pos(k, v, node)
        else:
            node[k] = v
    return node


def trans_tags(element, node):
    tags = element.findall('tag')
    for tag in tags:
        k = tag.attrib.get('k')
        v = tag.attrib.get('v')
        ks = k.split(':')
        _k = ks[0]
        if len(ks) >= 2:
            if _k == 'addr':
                _k = 'address'

            if node.get(_k) is None:
                node[_k] = {}

            if isinstance(node.get(_k), str):
                pass

            elif isinstance(node.get(_k), dict):

                # unify the postcode if the second level of k is postcode
                if ks[1] == 'postcode':
                    node[_k][ks[1]] = unify_postcode(v)

                else:
                    node[_k][ks[1]] = v

            else:
                pass

        elif k in ['lat', 'lon']:
            node = trans_pos(k, v, node)

        else:
            node[k] = v

        # clean source
        if k == 'source':
            node['source_category'] = unify_source(v)

        # clean amenity
        if k == 'amenity':
            node['amenity_category'] = unify_amenity(v)

    return node


def unify_source(source):
    """
    Unify sources data and transform into consistent fashion.
    :param source:
    """
    _source_cat = set()
    if isinstance(source, str):
        _source = source.replace('_', ' ').lower()
        _source = problemchars.sub(' ', _source).strip()

        for cat, pat in SOURCE_MAPPING.iteritems():
            # If one of the source pattern matches with the source category,
            # add it to the array of source category.
            if isinstance(pat, str):
                _pat = [pat]
            elif isinstance(pat, list):
                _pat = pat
            else:
                continue

            for p in _pat:
                if re.search(p, _source) is not None:
                    _source_cat.add(cat)

    elif isinstance(source, dict):
        for k, v in source.iteritems():
            _source_cat.add(unify_source(v))

    return list(_source_cat)


def unify_postcode(postcode):
    """
    Transform inconsistent postcode into consistent postcode.
    :param postcode:
    :return:
    """
    _postcode = postcode.upper().strip()
    _postcode = problemchars.sub('', _postcode)
    try:
        p = uk.validate(_postcode)
        if p is not None:
            return p.normalised
        else:
            return postcode
    except Exception, err:
        return postcode


def unify_amenity(amenity):
    _amenity = amenity.lower().strip()
    _amenity = problemchars.sub(' ', _amenity).strip()
    _amenity = _amenity.replace('_', ' ').strip()
    return _amenity


def is_basic_node(node):
    """
    Check if a node is a node that contains only the basic info ('pos', 'created', 'id', 'type')
    nothing more info is stored in the node.
    """
    return sorted(node.keys()) == ['created', 'id', 'pos', 'type']


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        if element.tag == 'node':
            # transform attributes
            node = trans_attr(element, node)

            # transform tags
            node = trans_tags(element, node)

        elif element.tag == 'way':
            nds = element.findall('nd')
            for nd in nds:
                if node.get('node_refs') is None:
                    node['node_refs'] = []
                node['node_refs'].append(nd.get('ref'))

            # transform attributes
            node = trans_attr(element, node)

            # transform tags
            node = trans_tags(element, node)

        node['type'] = element.tag

        # tag the node if it is a basic node
        if node['type'] == 'node':
            node['basic_node'] = is_basic_node(node)

        pprint(node)

        return node
    else:
        return None


def run_mongoimport(file_in):
    import subprocess

    col_name = file_in.split('.')[0]
    cmd = 'mongo --eval "db.getMongo().getDB(\'osm\').manchester_england.remove({});"'
    subprocess.call(cmd, shell=True)

    cmd = '''
    mongoimport -h localhost \
    -d osm \
    -c {0} \
    --file {1}
    '''.format(col_name, file_in)
    subprocess.call(cmd, shell=True)


def process_map(file_in, pretty=False, sample_size=None, mongoimport=True):
    file_out = "{0}.json".format(file_in)

    with codecs.open(file_out, "wb") as fo:
        c = 0
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")

            if sample_size is not None and c == sample_size:
                break

            c += 1

    if mongoimport:
        run_mongoimport('{0}.json'.format(file_in))

    print 'total processed elements: {0}'.format(c)


if __name__ == '__main__':
    tic = datetime.now()

    # process_map('manchester_england.osm', sample_size=100000)
    process_map('manchester_england.osm', sample_size=None)

    toc = datetime.now()

    print 'Total processed time: {0} seconds'.format((toc - tic).total_seconds())

