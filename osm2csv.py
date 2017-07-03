#!/usr/bin/env python3
import argparse
import unicodecsv as csv
import xml.etree.ElementTree as ET
import reverse_geocode

def parse_args():
    parser = argparse.ArgumentParser(description='Convert museum osm files to csv')
    parser.add_argument('-i', '--input', type=str, required=True, help='input osm xml filename')
    parser.add_argument('-o', '--output', type=str, required=True, help='output csv filename')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    return parser.parse_args()

def create_entry():
    return {
        "name": None,
        "name:en": None,
        "type": None,
        "int_name": None,
        "old_name": None,
        "old_name:en": None, 
        "country": None,
        "city": None,
        "lat": None,
        "long": None,
        "website": None,
        "date_added": None,
        "description": None
    }

def is_type_tag(tagname):
    types = ['amenity', 'boundary', 'building', 'geological', 'historic', 
             'landuse', 'leisure', 'man_made', 'tourism']
    return tagname in types

def main():

    args = parse_args()

    with open(args.output, 'wb') as csv_file:
        
        fieldnames = ['name', 'name:en', 'type', 'int_name', 'old_name', 'old_name:en', 'country', 
                      'city', 'lat', 'long', 'website', 'date_added', 'description']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        num_rows = 0
        entry = create_entry()
        
        for event, elem in ET.iterparse(args.input, events=("start", "end")):
            if event == 'start':
                if elem.tag == 'node':
                    if 'lat' in elem.attrib: entry['lat'] = elem.attrib['lat']
                    if 'lon' in elem.attrib: entry['long'] = elem.attrib['lon']
                    if 'timestamp' in elem.attrib: entry['date_added'] = elem.attrib['timestamp']
                    coords = [(float(elem.attrib['lat']), float(elem.attrib['lon']))]
                    location = reverse_geocode.search(coords)[0]
                    entry['country'] = location['country']
                    entry['city'] = location['city']
            elif event == 'end':
                if elem.tag == 'tag':
                    if 'k' in elem.attrib and elem.attrib['k'] == 'name': entry['name'] = elem.attrib['v']
                    if 'k' in elem.attrib and elem.attrib['k'] == 'name:en': entry['name:en'] = elem.attrib['v']
                    if 'k' in elem.attrib and is_type_tag(elem.attrib['k']): entry['type'] = elem.attrib['v']
                    if 'k' in elem.attrib and elem.attrib['k'] == 'int_name': entry['int_name'] = elem.attrib['v']
                    if 'k' in elem.attrib and elem.attrib['k'] == 'old_name': entry['old_name'] = elem.attrib['v']
                    if 'k' in elem.attrib and elem.attrib['k'] == 'old_name:en': entry['old_name:en'] = elem.attrib['v']
                    # if 'k' in elem.attrib and elem.attrib['k'] == 'addr:country': entry['country'] = elem.attrib['v']
                    # if 'k' in elem.attrib and elem.attrib['k'] == 'addr:city': entry['city'] = elem.attrib['v']
                    if 'k' in elem.attrib and elem.attrib['k'] == 'website': entry['website'] = elem.attrib['v']
                    if 'k' in elem.attrib and elem.attrib['k'] == 'description': entry['description'] = elem.attrib['v']
                elif elem.tag == 'node':
                    # add to csv
                    csv_writer.writerow(entry)
                    num_rows += 1
                    entry = create_entry()
        print('wrote {} rows to {}'.format(num_rows, args.output))

if __name__ == '__main__':
    main()