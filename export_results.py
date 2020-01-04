import argparse
import os
import glob
import logging
import sys



import version09x.benchmarks.corl2017 as corl2017
import version09x.benchmarks.nocrash as nocrash

from version09x.benchmark import benchmark

# TODO pip install atuomatically for the benchmark runner

def export_results(average= True):
    #TODO control averaging process
    # TODO MAYBE REPORT JUST ONE RESULT

    list_csv = sorted(os.listdir('_results'))

    # TODO this is repetition 1 now
    results_dict = {}


    for csv_filename in list_csv:
        print (csv_filename )
        # benchmark characteristics
        # right now we have agent-benchmark-condtions-task
        bench_features = csv_filename[:-4]
        split_names = bench_features.split('_')
        agent_name, benchmark, conditions, task = split_names[0], split_names[1], split_names[2], \
                                                    ''.join(split_names[3:])


        if agent_name not in results_dict:
            results_dict.update({agent_name:[{'benchmark': [benchmark, conditions, task],
                                 'data': []
                                 }]})
        else:
            results_dict[agent_name].append({'benchmark': [benchmark, conditions, task],
                                              'data': [] })

        with open(os.path.join('_results', csv_filename), 'r') as csv_file:

            header = csv_file.readline()
            data = csv_file.readline()
            data_info = data.split(',')
            data_info = [float(x) for x in data_info[1:]]
            results_dict[agent_name][-1]['data'].append(data_info)

    # We write one file for each agent
    # we start by writing the header

    for agent_name in  results_dict.keys():

        # you write the csv with the agent name
        with open(agent_name + '.csv', 'w') as r_file:

            for i in range(len(results_dict[agent_name])):
                count = 0
                benchmark = results_dict[agent_name][i]['benchmark']
                print (benchmark)
                data = results_dict[agent_name][i]['data']
                for data_point in data:
                    print ("d piint", data_point)
                    r_file.write("%s,%s,%s,%s," % ('r' + str(count), benchmark[0],
                                                  benchmark[1], benchmark[2])
                                 )
                    r_file.write("%.03f,%.03f,%.03f,%.03f\n" % (data_point[0], data_point[1],
                                                              data_point[2], data_point[3])
                                 )
                    count += 1

            # write the bench characteristics



if __name__ == '__main__':
    # Run like

    export_results()

