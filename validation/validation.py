from lxml import etree

# Cargar el esquema XSD
with open("struct.xsd", "rb") as xsd_file:
    schema_root = etree.XML(xsd_file.read())
    schema = etree.XMLSchema(schema_root)

# Cargar el archivo XML
with open("example.xml", "rb") as xml_file:
    xml_doc = etree.XML(xml_file.read())

# Validar el XML
if schema.validate(xml_doc):
    print("El XML es válido.")
else:
    print("El XML no es válido.")
    for error in schema.error_log:
        print(error.message)