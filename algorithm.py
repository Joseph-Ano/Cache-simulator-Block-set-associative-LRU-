def main_algo(set_size: int, block_size: int, main_memory_size, cache_memory_size: str, cache_memory_type: str, program_flow: str, program_flow_type: str):

    if(cache_memory_type == "blocks"):
        num_sets = int(cache_memory_size) / set_size
    else:
        blocks_in_cache = int(cache_memory_size) / block_size
        num_sets = blocks_in_cache / set_size

    num_sets = int(num_sets)

    sequence = program_flow.split(" ")
    sequence_length = len(sequence)
    
    cache = [[] for _ in range(num_sets)]
    hit = 0
    miss = 0
    
    for i in range(0, sequence_length, 1):
        curr_instruction = sequence[i]
        
        try:
            if(program_flow_type == "blocks"):
                dset = int(curr_instruction) % num_sets
            else:
                dset = int(curr_instruction)//block_size % num_sets
        except ZeroDivisionError:
            return -1, -1, -1
        except ValueError:
            return -2, -2, -2
        
        if(int(curr_instruction) < 0):
            return -3, -3, -3

        set_capacity = len(cache[dset])
        newest = -1
        oldest = float('inf')
        oldest_index = 0
        found = False

        for j in range(0, set_capacity, 1):
            newest = max(cache[dset][j][1], newest)
            if(cache[dset][j][1] < oldest):
                oldest = cache[dset][j][1]
                oldest_index = j

            if(cache[dset][j][0] == curr_instruction):
                age_index = j
                found = True

        if(found == True):
            hit+=1
            cache[dset][age_index][1] = newest + 1
            # print("hit: " + curr_instruction + " age: " + str(newest+1))
        elif(set_capacity < set_size):
            miss+=1
            cache[dset].append([curr_instruction, newest+1])
            # print("miss: " + curr_instruction + " age: " + str(newest+1))
        else:
            miss+=1
            cache[dset][oldest_index] = [curr_instruction, newest+1]
            # print("miss: " + curr_instruction + " age: " + str(newest+1))
       
    return cache, hit, miss

