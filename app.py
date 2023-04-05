from texttable import Texttable
import numpy as np
import pandas as pd
import streamlit as st
from algorithm import *

def main():
    input_type = ['blocks', 'words']

    st.title("Group 5 CSARCH2 Final Project")
    st.text("Cache simulator (Block-set-associative / LRU)")

    set_size = st.sidebar.text_input("Set Size (blocks)", key="set_size")
    block_size = st.sidebar.text_input("Block Size (words)", key="block_size")
    mm = st.sidebar.text_input("Main Memory Size", key="mm")
    cache_memory_size = st.sidebar.text_input("Cache Memory Size (blocks/words)", key="cache_size")
    cache_type = st.sidebar.radio("Cache Memory Type", input_type)
    program_flow = st.sidebar.text_input("Program Flow (blocks/words)", key="program_flow")
    instruction_type = st.sidebar.radio("Program Flow Type", input_type)
    existError = False
    
    # set_size = 2 #blocks
    # block_size = 2 #words
    # mm = None
    # cache_memory_size = "4"
    # program_flow = "1 7 5 0 2 1 5 6 5 2 2 0"

    simulate = st.button("Simulate", key="simulate")

    if(simulate):
        set_size = set_size.strip()
        block_size = block_size.strip()
        cache_memory_size = cache_memory_size.strip()
        program_flow = program_flow.strip()

        try:    #checks if set size and block size input are integers
            set_size = int(set_size)
            block_size = int(block_size)
        except ValueError:
            existError = True
            st.warning("Set Size and Block Size must be an integer.")

        if(existError == False):
            if(set_size < 0):   #checks if set size is positive
                st.warning("Set Size must be a positive integer.")
                existError = True
            elif(block_size < 0):   #checks if block size is positive
                st.warning("Block Size must be a positive integer.")
                existError = True

            if(existError == False):
                try:
                    cache_memory_size = int(cache_memory_size) #checks if cache memory size is an integer
                except ValueError:
                    st.warning("Cache memory size must be an integer")
                    existError = True

                if(existError == False):
                    if(cache_memory_size < 0):  #checks if cache memory size is positive
                        st.warning("Cache memory size must be a positive integer")
                        existError = True

                    if(existError == False):
                        if(program_flow == ""): #checks if program flow has at least one instruction
                            st.warning("Program flow must have at least one instruction.")
                            existError = True 

        if(existError == False):
            cache_check = 1
            cache_access_time = 1
            memory_access_time = 10
            snapshot, hit, miss = main_algo(set_size, block_size, mm, cache_memory_size, cache_type, program_flow, instruction_type)

            if(snapshot == -1):
                st.warning("Cache Memory Size is not a valid input given the Set Size and/or Block Size")
            elif(snapshot == -2):
                st.warning("Instructions in Program Flow must be integers")
            elif(snapshot == -3):
                st.warning("Instructions in Program Flow must be positive")

            else:
                miss_penalty = cache_check + (block_size*memory_access_time) + cache_access_time
                hit_rate = hit/(hit+miss)
                miss_rate = miss/(hit+miss)
                avg_access_time = hit_rate*cache_access_time + miss_penalty*miss_rate
                total_access_time = (hit*block_size*cache_access_time) + (miss*block_size*(cache_access_time+memory_access_time)) + cache_check*miss

                st.write("Cache Hits: {cache_hit}".format(cache_hit=hit))
                st.write("Cache Miss: {cache_miss}".format(cache_miss=miss))
                st.write("Miss Penalty: {penalty}ns".format(penalty=miss_penalty))
                st.write("Average Memory Access Time: {access_time}ns".format(access_time=avg_access_time))
                st.write("Total Memory Access Time: {access_time}ns".format(access_time=total_access_time))

                table_header = ["Sets"]

                for row in range(0, len(snapshot), 1):
                    blocks_in_set = len(snapshot[row])

                    while(blocks_in_set < set_size):
                        snapshot[row].append([])
                        blocks_in_set+=1

                    for col in range(0, set_size, 1):
                        if not snapshot[row][col]:
                            snapshot[row][col] = "-"
                        else:
                            snapshot[row][col] = snapshot[row][col][0]

                for i in range(0, set_size, 1):
                    table_header.append("Block {i}".format(i=i))

                for i in range(0, len(snapshot),1):
                    snapshot[i].insert(0, "Set {i}".format(i=i))

                np_snapshot = np.array(snapshot)

                df = pd.DataFrame(np_snapshot, columns = table_header)
                st.table(df)

                table_header = [table_header]
                table_header.extend(snapshot)

                t = Texttable()
                t.add_rows(table_header)

                formatted_table = t.draw()

                text_contents = '''
Cache Hits: {cache_hit}\n
Cache Miss: {cache_miss}\n
Average Memory Access Time: {avg_access_time}ns\n
Total Memory Access Time: {total_access_time}ns\n
{snapshot}
                '''.format(cache_hit=hit, cache_miss=miss, penalty=miss_penalty, avg_access_time=avg_access_time, 
                        total_access_time=total_access_time, snapshot=formatted_table)

                st.download_button(
                    label="Download",
                    data=text_contents,
                    file_name='Group5_Simulation.txt',
                )   

if __name__ == "__main__":
    main()