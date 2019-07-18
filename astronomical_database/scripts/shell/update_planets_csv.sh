#!/bin/bash

DATE_STRING=`date -d "" +%Y-%m-%d`
DATA_DIR=astronomical_database/data/csv/planets
wget "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=pl_hostname,pl_letter,pl_dens,pl_disc,pl_massj,pl_radj,pl_orbsmax,pl_orbper,st_bmvj,st_dist,st_lum,st_rad,st_spstr" -O "${DATA_DIR}/planets.${DATE_STRING}.csv"
cp ${DATA_DIR}/planets.${DATE_STRING}.csv ${DATA_DIR}/planets.csv
