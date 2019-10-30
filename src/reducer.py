import sys

# We will use -9999 as an error value, so if the output contains -9999 something has gone wrong
last_temp = -9999

last_key = None

# Read in each line that has been sent to this particular reducer
for line in sys.stdin:
    line = line.strip()
    current_key, value = line.split("\t", 1)
    observation_type, current_temp = value.split(".")

    current_temp = int(current_temp)

    if current_key == last_key:
        if last_temp < current_temp:
            temp_difference = current_temp - last_temp
        else:
            temp_difference = last_temp - current_temp

        print("%s,%s" % (current_key, temp_difference))
        # Reset the last_temp to the error value
        last_temp = -9999
    else:
        last_temp = current_temp
        last_key = current_key
