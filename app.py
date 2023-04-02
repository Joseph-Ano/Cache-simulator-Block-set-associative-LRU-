from texttable import Texttable
import numpy as np
import pandas as pd
import streamlit as st
from algorithm import *

def main():
    st.title("Group 5 CSARCH2 Final Project")
    st.text("Cache simulator (Block-set-associative / LRU)")

    set_size = st.sidebar.text_input("Set Size", key="set_size")
    block_size = st.sidebar.text_input("Block Size", key="block_size")
    mm = st.sidebar.text_input("Main memory size", key="mm")
    cache_memory_size = st.sidebar.text_input("Cache memory size", key="cache_size")
    program_flow = st.sidebar.text_input("Program flow", key="program_flow")

    try:
        set_size = int(set_size)
        block_size = int(block_size)
    except:
        pass
    
    # set_size = 2 #blocks
    # block_size = 2 #words
    # mm = None
    # cache_memory_size = "4 blocks"
    # program_flow = "blocks 1 7 5 0 2 1 5 6 5 2 2 0"

    cache_check = 1
    cache_access_time = 1
    memory_access_time = 10

    if(st.button("Simulate", key="simulate")):
        snapshot, hit, miss, num_sets = main_algo(set_size, block_size, mm, cache_memory_size, program_flow)

        if(snapshot == -5):
            st.warning("Cache memory size is not a valid input given the Set Size and/or Block size")
            
        else:
            miss_penalty = cache_check + (block_size*memory_access_time) + cache_access_time

            hit_rate = hit/(hit+miss)
            miss_rate = miss/(hit+miss)
            avg_access_time = hit_rate*cache_access_time + miss_penalty*miss_rate
            total_access_time = (hit*block_size*cache_access_time) + (miss*block_size*(cache_access_time+memory_access_time)) + cache_check*miss


            st.write("Cache hits: {cache_hit}".format(cache_hit=hit))
            st.write("Cache miss: {cache_miss}".format(cache_miss=miss))
            st.write("Miss penalty: {penalty}".format(penalty=miss_penalty))
            st.write("Average memory access time: {access_time}".format(access_time=avg_access_time))
            st.write("Total memory access time: {access_time}".format(access_time=total_access_time))

            table_header = ["Sets"]

            for row in range(0, len(snapshot), 1):
                blocks_in_set = len(snapshot[row])

                while(blocks_in_set < set_size):
                    snapshot[row].append([])
                    blocks_in_set+=1

                for col in range(0, set_size, 1):
                    if not snapshot[row][col]:
                        snapshot[row][col] = "empty"
                    else:
                        snapshot[row][col] = snapshot[row][col][0]

            for i in range(0, set_size, 1):
                table_header.append("Block {i}".format(i=i))

            for i in range(0, len(snapshot),1):
                snapshot[i].insert(0, "Set {i}".format(i=i))

            np_snapshot = np.array(snapshot)

            print(snapshot)

            df = pd.DataFrame(np_snapshot, columns = table_header)
            st.table(df)


            table_header = [table_header]
            table_header.extend(snapshot)

            t = Texttable()
            t.add_rows(table_header)

            formatted_table = t.draw()

            text_contents = '''
    Cache hits: {cache_hit}\n
    Cache miss: {cache_miss}\n
    Average memory access time: {avg_access_time}\n
    Total memory access time: {total_access_time}\n
    {snapshot}
            '''.format(cache_hit=hit, cache_miss=miss, penalty=miss_penalty, avg_access_time=avg_access_time, 
                    total_access_time=total_access_time, snapshot=formatted_table)

            st.download_button(
                label="Download",
                data=text_contents,
                file_name='Group5.txt',
            )   

if __name__ == "__main__":
    main()