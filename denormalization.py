import json

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(data, filename):
    """Save JSON data to a file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def merge_data(members, payments, regions):
    """Embed payments and region details into member documents."""
    region_map = {region['region_no']: region for region in regions}
    payment_map = {}
    for payment in payments:
        if payment['member_no'] not in payment_map:
            payment_map[payment['member_no']] = []
        payment_map[payment['member_no']].append(payment)

    for member in members:
        member['payments'] = payment_map.get(member['member_no'], [])
        if 'region_no' in member:
            member['region'] = region_map.get(member['region_no'], {})
            del member['region_no']  # Remove region_no if you do not want it duplicated

    return members

def process_corporations(corporations, payments, members):
    """Calculate aggregates and embed them in corporations."""
    member_to_corp = {m['member_no']: m['corp_no'] for m in members}
    for corp in corporations:
        corp_payments = [p for p in payments if member_to_corp.get(p['member_no']) == corp['corp_no']]
        total_payments = sum(p['payment_amt'] for p in corp_payments)
        corp['total_payments'] = total_payments
    return corporations

# Example file paths
members_file = '_member__202410070837.json'
payments_file = 'payment_202410070837.json'
regions_file = 'region_202410070838.json'
corporations_file = 'corporation_202410070836.json'

# Load data
members = load_json(members_file)
payments = load_json(payments_file)
regions = load_json(regions_file)
corporations = load_json(corporations_file)

# Process and merge data
members = merge_data(members, payments, regions)
corporations = process_corporations(corporations, payments, members)

# Save processed data
save_json(members, 'denormalized_members.json')
save_json(corporations, 'denormalized_corporations.json')
