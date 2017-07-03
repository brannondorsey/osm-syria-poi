# Open Street Maps Syria Points of Interest

[`data/syria-poi.csv`](data/syria-poi.csv) contains data from cultural/historical points of interest in Syria (1,982 in total). It was extracted from [planet.osm](https://wiki.openstreetmap.org/wiki/Planet.osm) as of June 5th, 2017. For a complete list of Open Street Maps tags used to extract these points, see the [OSM Tags](#OSM-Tags) section below.

The code in this repository uses [Osmosis](https://wiki.openstreetmap.org/wiki/Osmosis) to search for OSM nodes that match the specific [OSM tags below](#OSM-Tags) using a [polygon shape file of Syria](data/syria.poly) as the "bounding box" (poly source [here](https://download.geofabrik.de/)). It would be trivial to adapt `query.sh` to use different search criteria to meet your needs. See [here](https://wiki.openstreetmap.org/wiki/Osmosis/Detailed_Usage_0.45) for more info. I've written code that parses the resulting [`data/syria-poi.osm`](data/syria-poi.osm) query into a CSV that includes only a subset of desirable fields. I've found the country/city data provided by OSM to be quite sparse, so I've ignored OSM's city and country fields and chosen to instead include results from a reverse geolookup by lat/long using the [reverse-geocode](https://bitbucket.org/richardpenman/reverse_geocode) python package.

If you wish to repeat this process, or run similar queries or convert OSM XML to CSV, see below.

## Download

Open Street Maps planet data is ~54GB compressed, and ~751GB once uncompressed. [Full planet files](https://wiki.openstreetmap.org/wiki/Planet.osm) are made available weekly.

```bash
# clone this repo
git clone https://github.com/brannondorsey/osm-syria-poi

# navigate to the data folder
cd osm-syria-poi/data

# download the planet osm file
wget https://ftp5.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/planet/2017/planet-170102.osm.bz2

# you will likely need to install pbzip2 before running this command
# uncompress using 2GB of RAM (the max)
pbzip2 -d -m2000 planet-170102.osm.bz2
```

Osmosis can operate on `.bz2` compressed OSM files, however this is not encouraged and unless disk space is a limited resource should be avoided. 

## Query

The official OSM query tool is a Java application called [Osmosis](https://wiki.openstreetmap.org/wiki/Osmosis). You must [download and install](https://wiki.openstreetmap.org/wiki/Osmosis#How_to_install) it for your platform. Next we search for all museums in the world and output the results to an XML file called `syria-poi.osm` inside `data/`.

```bash
osmosis \
 --read-xml data/planet-170102.osm \
 --bounding-polygon file="data/syria.poly" \
 --tf accept-nodes amenity=library,arts_centre,fountain,planetarium,theatre,crypt,grave_yard,place_of_worship,ranger_station \
                   boundary=national_park,protected_area \
                   building=cathedral,chapel,church,mosque,temple,synagogue,shrine,conservatory,greenhouse,pavilion,ruins \
                   geological=palaeontological_site \
                   historic=aircraft,aqueduct,archaeological_site,battlefield,boundary_stone,building,cannon,castle,city_gate,citywalls,farm,fort,gallows,locomotive,manor,memorial,milestone,monastery,monument,pillory,railway_car,ruins,rune_stone,ship,tomb,wayside_cross,wayside_shrine \
                   landuse=cemetery \
                   leisure=garden,nature_reserve,park,wildlife_hide \
                   man_made=bridge,campanile,cross,lighthouse,obelisk,observatory,tower \
                   tourism=aquarium,artwork,attraction,gallery,zoo \
 --tf reject-ways \
 --tf reject-relations \
 --write-xml data/syrian_poi.osm
```

The above command is also the contents of `query.sh`. So you can instead run `./query.sh` for convenience. See here for [full Osmosis usage documentation](https://wiki.openstreetmap.org/wiki/Osmosis/Detailed_Usage_0.45).

## Convert to CSV (and augment location using geolookup)

`osm2csv.py` is a python program to convert osm file (that are the result of `query.sh`) to csv. Before running this program you must install the necessary dependencies.

```bash
pip install numpy scipy reverse_geocode unicodecsv
``` 

To convert and augment geo location data, run:

```bash
python osm2csv.py --input data/syria-poi.osm --output data/syria-poi.csv
```

## OSM Tags

Below is a list of Open Street Maps tags used in `query.sh`. 

### Amenity

- Library
- Arts_centre
- Fountain
- Planetarium
- Theatre
- Crypt
- Grave_yard
- Place_of_worship
- Ranger_station

### Boundary

- National_park
- Protected_area

### Building

- Cathedral
- Chapel
- Church
- Mosque
- Temple
- Synagogue
- Shrine
- Conservatory
- Greenhouse
- Pavilion
- Ruins

### Geological

- Palaeontological_site

### Historic

- Aircraft
- Aqueduct
- Archaeological_site
- Battlefield
- Boundary_stone
- Building
- Cannon
- Castle
- City_gate
- Citywalls
- Farm
- Fort
- Gallows
- Locomotive
- Manor
- Memorial
- Milestone
- Monastery
- Monument
- Pillory
- Railway_car
- Ruins
- Rune_stone
- Ship
- Tomb
- Wayside_cross
- Wayside_shrine

### Landuse

- Cemetery

### Leisure

- Garden
- Nature_reserve
- Park
- Wildlife_hide

### Man_made

- Bridge
- Campanile
- Cross
- Lighthouse
- Obelisk
- Observatory
- Tower

### Tourism

- Aquarium
- Artwork
- Attraction
- Gallery
- Museum
- Zoo



