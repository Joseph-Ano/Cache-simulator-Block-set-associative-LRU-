def main_algo(set_size: int, block_size: int, main_memory_size, cache_memory_size: str, program_flow: str):
    cache_size = cache_memory_size.strip().split(" ")

    if(cache_size[1] == "blocks"):
        num_sets = int(cache_size[0]) / set_size
    else:
        blocks_in_cache = int(cache_size[0]) / block_size
        num_sets = blocks_in_cache / set_size

    num_sets = int(num_sets)

    sequence = program_flow.strip().split(" ")
    sequence_length = len(sequence)
    
    cache = [[] for _ in range(num_sets)]
    hit = 0
    miss = 0
    
    for i in range(1, sequence_length, 1):
        curr_instruction = sequence[i]

        if(sequence[0] == "blocks"):
            dset = int(curr_instruction) % num_sets
        else:
            dset = int(curr_instruction)//block_size % num_sets

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
       
    return cache, hit, miss, num_sets

