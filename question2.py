import pandas as pd
import xml.etree.ElementTree as ET

xml_file = "FX_MAS_NEWT_OTHR.xml"
output_csv_file = "CSV_Output.csv"

namespaces = {
    'default': 'urn:iso:std:iso:20022:tech:xsd:auth.030.001.03'
}

tree = ET.parse(xml_file)
root = tree.getroot()
pyld = root.find("{urn:iso:std:iso:20022:tech:xsd:head.003.001.01}Pyld")
document = pyld.find("{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Document")
derivsTradRpt = document.find("{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}DerivsTradRpt")
tradData = derivsTradRpt.find("{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}TradData")

data = []

def findData(row, block, path):
    numChild = 0
    for child in block:
        numChild += 1
        findData(row, child, path + child.tag.replace(namespaces["default"], "").replace("{}", "/"))

    if numChild == 0:
        row[path] = block.text
    return

for rpt in tradData.findall("{urn:iso:std:iso:20022:tech:xsd:auth.030.001.03}Rpt"):
    row = {}
    findData(row, rpt, rpt.tag.replace(namespaces["default"], "").replace("{}", "/"))

    data.append(row)

df = pd.DataFrame(data)

print(df)
open(output_csv_file, "w").close()
with open(output_csv_file, "w") as file:
    df.to_csv(file, index=False, header=True)