# Airport codes

1. Get csv file here: https://datahub.io/core/airport-codes
2. Install cli tool:

        pip install csvkit timezonefinder

3. Check airport types:

        csvcut -c type airport-codes_csv.csv | tail -n +2 | sort | uniq

4. Convert original csv to odoo csv files

        python airport_codes.py airport-codes_csv.csv
