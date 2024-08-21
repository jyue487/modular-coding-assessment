import pandas as pd
import xml.etree.ElementTree as ET

excel_file = "XML_test_flat.xlsx"
output1_xml_file = "Output1.xml"
output2_xml_file = "Output2.xml"
output_values_sheet = "Output_Values"
output_xml_path_sheet = "Output_XML_Path"

df_output_values = pd.read_excel(excel_file, sheet_name=output_values_sheet, engine='openpyxl')
df_output_xml_path = pd.read_excel(excel_file, sheet_name=output_xml_path_sheet, engine='openpyxl')

# print(list(df_output_values.columns) == list(df_output_xml_path))
order = df_output_values.columns
df_output_xml_path = df_output_xml_path[order]
# print(list(df_output_values.columns) == list(df_output_xml_path))

m = len(df_output_values.axes[0])
n = len(df_output_values.axes[1])

### Task 1a: convert the first row in “Output_Values” into XML format. Name the file Output1.xml
first_row_of_output_values = df_output_values.iloc[0]
first_row_of_output_xml_path = df_output_xml_path.iloc[0].values


root = ET.Element(first_row_of_output_xml_path[0].split("/")[0])

for path, value in zip(first_row_of_output_xml_path, first_row_of_output_values):
    cellpath = path.split("/")[1:]
    parent = root
    
    for part in cellpath:
        if '@' in part:
            attr_name = part[1:].strip()
            parent.attrib[attr_name] = value
            continue

        found = False
        for child in parent:
            if child.tag == part:
                parent = child
                found = True
                break
        if not found:
            parent = ET.SubElement(parent, part)
    
    if "@" not in cellpath[-1]:
        parent.text = str(value)

tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)
open(output1_xml_file, "w").close()
tree.write(output1_xml_file, encoding="utf-8", xml_declaration=True)





### Task 1b: convert all rows in “Output_Values” into XML format. Name it Output2.xml
document_root = ET.Element("TradData")

# row_of_output_values = df_output_values.iloc[0]
# row_of_output_xml_path = df_output_xml_path.iloc[0].values

for i in range(m):

    row_of_output_values = df_output_values.iloc[i]
    row_of_output_xml_path = df_output_xml_path.iloc[i].values

    root = ET.SubElement(document_root, row_of_output_xml_path[0].split("/")[0])

    for path, value in zip(row_of_output_xml_path, row_of_output_values):
        cellpath = path.split("/")[1:]
        parent = root
        
        for part in cellpath:
            if '@' in part:
                attr_name = part[1:].strip()
                parent.attrib[attr_name] = value
                continue

            found = False
            for child in parent:
                if child.tag == part:
                    parent = child
                    found = True
                    break
            if not found:
                parent = ET.SubElement(parent, part)
        
        if "@" not in cellpath[-1]:
            parent.text = str(value)


tree = ET.ElementTree(document_root)
ET.indent(tree, space="\t", level=0)
open(output2_xml_file, "w").close()
tree.write(output2_xml_file, encoding="utf-8", xml_declaration=True)
