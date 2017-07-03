#!/bin/bash

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
