#!/usr/bin/python3

# This script parses Contiki COOJA output which includes output from PowerTrace module
# PowerTrace output is parsed and used to build a graph showing the energy consumption of
# different motes in the simulation

import plotly
import plotly.graph_objs as go
import datetime
import os
import numpy

__file = input('File to read: ')
__interval_seconds = int(input('Measure interval in seconds: '))

# Configuration
PLOTLY_USERNAME = 'samlinz'
PLOTLY_APIKEY = 'gR8XeP1gPmOgam6jOS5g'
RTIMER_TICKS_SECOND = 32768 # RTIMER_SECONDS VALUE
SKY_V = 3.3  # Mote voltage

SKY_I_TX = 21  # Mote current
SKY_I_RX = 23  # Mote current
SKY_I_CPU = 2.4  # Mote current
SKY_I_IDLE = 0.021  # Mote current

#SKY_I_TX = 18  # Mote current
#SKY_I_RX = 19  # Mote current
#SKY_I_CPU = 2.4  # Mote current
#SKY_I_IDLE = 0.021  # Mote current

# Calculate energy usages
def calc_energy(ticks, current):
    global __interval_seconds, RTIMER_TICKS_SECOND, SKY_V
    return ticks
    # The equation for mW is
    # (value * mote_voltage * mote_current) / (t * RTIMER_SECOND)
    #return (ticks * SKY_V * current) / (__interval_seconds * RTIMER_TICKS_SECOND)


# Crete a trace for a mote
def create_trace(name, x, y):
    return go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=name
    )


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


# Entry point
if __name__ == '__main__':
    lines = []
    meas = dict()

    print("Reading file " + __file)

    # Read lines
    with open(__file) as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]

    print('Parsing lines')

    pt_count = 0

    # Get rid of irrelevant lines
    for line in lines:
        parts = line.split()
        #if parts[1] == 'P' and len(parts) == 28:  # PowerTrace output
        if len(parts) == 10:  # Simplified PowerTrace output
            is_powertrace = True
            for i in range(2, 9):
                if not is_int(parts[i]):
                    is_powertrace = False
            if is_powertrace:
                pt_count += 1
                ref_time = datetime.datetime(2000, 1, 1, 0, 0, 0)
                time_parts = parts[0].split(':')
                time_parts2 = parts[0].split('.')
                clock_time = datetime.datetime(2000, 1, 1, 0, int(time_parts[0]), int(time_parts2[0].split(':')[1]), int(time_parts2[1]) * 1000)
                clock_time = (clock_time - ref_time).total_seconds()
                # Rime address of mote; used to differentiate between motes
                rime_addr = str(parts[1])
                # Measurement sequence number
                #seq_no = int(parts[3])

                # Total accumulated values
                total_cpu = int(parts[2])
                total_lpm = int(parts[3])
                total_tx = int(parts[4])
                total_rx = int(parts[5])

                # Values from the meas cycle
                cycle_cpu_time = int(parts[6])
                cycle_low_power_mode = int(parts[7])
                cycle_tx = int(parts[8])
                cycle_rx = int(parts[9])
                if rime_addr not in meas:
                    meas[rime_addr] = []

                # Calculate actual power in mW
                meas[rime_addr].append((clock_time, calc_energy(cycle_cpu_time, SKY_I_CPU), calc_energy(cycle_low_power_mode, SKY_I_IDLE),
                                        calc_energy(cycle_tx, SKY_I_TX), calc_energy(cycle_rx, SKY_I_RX)))

    print('Found ' + str(pt_count) + ' PowerTrace measurements')

    print('Generating traces')

    title = input('Graph title: ')

    # Remove previous average output
    try:
        os.remove('averages.txt')
    except (OSError, FileNotFoundError):
        pass

    def create_graph(id, name):
        full_title = title + '_' + name

        write_file(full_title + '\n' + '********')

        total = []
        data = []
        for m in meas:
            x_list = []
            y_list = []
            for single_meas in meas[m]:
                x_list.append(single_meas[0])
                y_list.append(single_meas[int(id)])
                total.extend(y_list)
            data.append(create_trace('Mote ' + m, x_list, y_list))
            write_file('Mote ' + m + ' ' + name + ': ' + '{0:.6f}'.format(numpy.mean(y_list)) + 'mW')

        write_file('Total ' + name + ' mean ' + '{0:.6f}'.format(numpy.mean(total)) + 'mW')

        layout = go.Layout(title=full_title, width=800, height=640)

        print('Generating graph ' + str(full_title))

        plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_APIKEY)
        plotly.tools.set_config_file(world_readable=True)

        fig = go.Figure(data=data, layout=layout)
        print(plotly.plotly.plot(fig, filename=full_title.lower()))

    def write_file(value):
        with open('averages.txt', 'a') as f:
            f.write(str(value + '\n'));

    create_graph(1, 'CPU')
    create_graph(2, 'LPM')
    create_graph(3, 'TX')
    create_graph(4, 'RX')

else:
    print('Run the file as the main module')
