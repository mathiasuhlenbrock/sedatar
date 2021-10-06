#!/bin/zsh

DATE_STRING=$(date +%Y-%m-%d)
DATA_DIR=astronomical_database/data/csv/planets
wget "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+disc_year,hostname,pl_dens,pl_letter,pl_massj,pl_orbper,pl_orbsmax,pl_radj,st_lum,st_rad,st_spectype,sy_bmag,sy_dist,sy_vmag+from+ps+where+default_flag=1&format=csv" -O "${DATA_DIR}/planets.${DATE_STRING}.csv"
cp ${DATA_DIR}/planets."${DATE_STRING}".csv ${DATA_DIR}/planets.csv
