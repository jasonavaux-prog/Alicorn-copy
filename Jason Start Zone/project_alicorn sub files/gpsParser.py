#In the real world, this string would come from your phone's hardware.

# Raw GPS data (GPGGA sentence)
# Format:  [0]$GPGGA(message ID), [1]hhmmss.ss (time), [2]raw lat, [3]N/S Indicator, [4]raw long, 
#          [5]E/W Indicator, [6]quality, [7]sats, [8]hdop, [9]alt, [10]unit...
raw_data = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
#[2] in degreesMinutes, most map API need decimal degrees i.e. 48.1173

# 1. Split the string by commas
data_list = raw_data.split(",")

# 2. Extract the specific "indices" we need
# Index 2 is Latitude, Index 4 is Longitude, Index 9 is Altitude
raw_lat = data_list[2]
lat_direction = data_list[3]
raw_lon = data_list[4]
lon_direction = data_list[5]
altitude = data_list[9]

# 3. Print the results to the console
print(f"---GPS DATA EXTRACTED---")
print(f"Raw Latitude: {raw_lat} {lat_direction}")
print(f"Raw Longitude: {raw_lon} {lon_direction}")
print(f"Current Altitude: {altitude} Meters")


def convert_to_decimal(raw_value, direction):
    if not raw_value:
        return None
    
    # Latitude (DDMM.MMMM) has 2 digits for degrees
    # Longitude (DDDMM.MMMM) has 3 digits for degrees
    # We find the decimal point and move back two places to find the split
    dot_index = raw_value.find('.')
    degrees = float(raw_value[:dot_index-2])
    minutes = float(raw_value[dot_index-2:])
    
    decimal = degrees + (minutes / 60)
    
    # If direction is South or West, the coordinate must be negative
    if direction in ['S', 'W']:
        decimal = -decimal
        
    return round(decimal, 6)

# Applying the function to your previous variables
clean_lat = convert_to_decimal(raw_lat, lat_direction)
clean_lon = convert_to_decimal(raw_lon, lon_direction)

print(f"Decimal Coordinates: {clean_lat}, {clean_lon}")