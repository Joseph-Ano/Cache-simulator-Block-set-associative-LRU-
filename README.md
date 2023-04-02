# csarch2-final-proj
Cache simulator (Block-set-associative / LRU)
Created By Group 5: Ano, Ejercito, Limjoco
--- 

# Assumptions
1. Read policy: **Non-Load-through**
2. Cache check time: **1ns**
3. Cache access time: **1ns**
4. Memory access time: **10ns**

--- 

# User manual 
How to run the app:
1. All input fields must be filled out.

2. For Main memory size and Cache memory size, place either `blocks` or `words` after the value.
>*Example:* **4 blocks** or **4 words**

3. For program flow, place either `blocks` or `words` before the sequece of instructions. Separate each value with a space.  
>*Example*: **blocks 1 7 5 0 2 1 5 6 5 2 2 0**

4. Click the `Simulate` button once all fields are filled out. The results will be displayed on the screen.

5. To download the results as a txt file, click the `Download` button below the results. Clicking the button will reload the web app and the results on the screen will disappear. The text will have a file name called `Group5_Simulation.txt'`.

**Sample Input**
set_size = 2 #blocks
block_size = 2 #words
mm = None
cache_memory_size = "4 blocks"
program_flow = "blocks 1 7 5 0 2 1 5 6 5 2 2 0"

# Disclaimer
*After rigorous testing, the group discovered that the `texttables` library has a limit on printing a number of tables. If the tables are printing beyond a "Set Size" of greater than or equal to 19, the application will throw an error. The application will still continue working and throwing errors until a valid input has been simulated. User will be unable to download the text file, but the table will still be displayed on the web application.