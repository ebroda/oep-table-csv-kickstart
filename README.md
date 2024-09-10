# OEP CSV Importer
Use your csv file as a kickstarter for your [OpenEnergyPlatform](https://openenergyplatform.org)-table. 
Simply select your csv file and the tool will read the first two lines of the csv file and provide based on that
a valid table name and all columns matching your columns in your csv file. Also, the datatype is, at least simply,
guessed. Now you can submit the structure, and it will be created in the OpenEnergyPlatform, so that you can continue 
your upload journey in the OEP Data Upload Wizard, afterwards.

## Setup
- Install requirements, based on [requirements.txt](requirements.txt)
- For correct csv parsing, add [csv.js](https://raw.githubusercontent.com/vanillaes/csv/97d4c81be083f0fc93c460f1f331eeb83edc0e96/index.js) to frontend/app/. Remove two times the keywords "export", e.g.
  ``cd frontend/app/ && wget https://raw.githubusercontent.com/vanillaes/csv/97d4c81be083f0fc93c460f1f331eeb83edc0e96/index.js && awk '{ gsub(/export/, ""); print }' index.js > csv.js && rm index.js``
- Copy [settings.py.xmpl](settings.py.xmpl) to settings.py and set the values, accordingly.
- Run oep_csv_import.py

