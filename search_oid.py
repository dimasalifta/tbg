import json

# Load JSON data from file
with open('mc2600_oid_list.json', 'r') as f:
    data = json.load(f)

# Define the OID you want to search for
target_oid = "systemVoltage"

# Search for the entry with the matching OID
matching_entry = None
for entry in data:
    if entry['signal_name'] == target_oid:
        matching_entry = entry
        break

# Check if matching entry is found
if matching_entry:
    print("Found matching entry:")
    print("OID:", matching_entry['oid'])
    print("Signal Name:", matching_entry['signal_name'])
    print("English Description:", matching_entry['english_description'])
    print("Chinese Description:", matching_entry['chinese_description'])
    print("Interface Type:", matching_entry['interface_type'])
    print("Value Type:", matching_entry['value_type'])
    print("Value Description:", matching_entry['value_description'])
    print("Permissions:", matching_entry['permissions'])
else:
    print("No matching entry found for OID:", target_oid)
