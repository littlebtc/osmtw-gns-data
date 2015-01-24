import os
import unicodecsv
from collections import OrderedDict

result_by_adm = OrderedDict()

with open('original/tw_populatedplaces_p.txt', 'r') as ppl_input:
    rows = unicodecsv.DictReader(ppl_input, dialect=unicodecsv.excel_tab)
    print "Parsing data from GNS..."
    for row in rows:
        # Only NS and N entries will be used.
        if row["NT"] != "NS" and row["NT"] != "N":
            continue
        adm_data = result_by_adm.setdefault(row["ADM1"], OrderedDict())
        entry = adm_data.setdefault(row["UFI"], OrderedDict())
        if len(entry) < 1:
            # Input basic data if not duplicated.
            entry["lat"] = row["LAT"]
            entry["lon"] = row["LONG"]
            entry["place"] = "village"
            entry["name"] = ""
            entry["name:en"] = ""
            entry["GNS:id"] = row["UFI"]
            entry["GNS:dsg_code"] = row["DSG"]
            entry["GNS:dsg_string"] = "populated place" # XXX
            entry["source"] = "GNS"
        # Fill the name
        if row["NT"] == "NS":
            entry["name"] = row["FULL_NAME_ND_RO"]
        else: # It is the N (approved)
            entry["name:en"] = row["FULL_NAME_ND_RO"]

    print "Done, writing data to CSVs..."
    count = 0
    count_nonzh = 0
    fieldnames = ["lat", "lon", "place", "name", "name:en", "GNS:id", "GNS:dsg_code", "GNS:dsg_string", "source"]
    if not os.path.exists("ppl"):
        os.makedirs("ppl")
    for adm, result in result_by_adm.iteritems():
        with open('ppl/adm-%s.csv'%adm, "w") as output:
            writer = unicodecsv.DictWriter(output, fieldnames = fieldnames)
            writer.writeheader()
            for entry in result.itervalues():
                writer.writerow(entry)
                count = count + 1
        with open('ppl/nonzh-adm-%s.csv'%adm, "w") as output:
            writer = unicodecsv.DictWriter(output, fieldnames = fieldnames)
            writer.writeheader()
            for entry in result.itervalues():
                if entry["name"]:
                    continue
                else:
                    writer.writerow(entry)
                    count_nonzh = count_nonzh + 1
    print "OK! %d places, %d has no Chinese name"%(count, count_nonzh)
