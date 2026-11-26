import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--start", type=str)
parser.add_argument("--end", default="poop", type=str)
parser.add_argument("--dict", default="4_letter_words_graph", type=str)

args = parser.parse_args()

START = args.start
END = args.end
DICT = args.dict
BLOCKED = []

with open(DICT) as g:
    d = json.load(g)

graph = d["adjazenzmatrix"]
keys = d["words"]
#djistra table lines mit tracking zahl versehen

def compare_lines_and_increase(current_row, total_distances):
    #return refreshed total_distances 
    pass


def status(processed, stack):
    print(f"processed {len(processed)} words, {len(stack)} neighbors in the stack")

def path_find(itterations, processed):
    processed.sort()
    wordss = itterations["word"][::-1]
    inspecting={"w":"", "l":0}
    inspected=[]
    #print(wordss)
    for i, n in enumerate(itterations['rows'][::-1]):
        if inspecting['w'] == "":
            inspecting['w'] = wordss[i]
            inspecting['l'] = n[inspecting['w']]
            inspected.append(inspecting)
        else:
            if n[inspecting["w"]] == inspecting['l']:
                continue
            else:
                inspecting['w'] = wordss[i-1]
                print(keys[inspecting["w"]])
                inspecting['l'] = n[inspecting['w']]
                print(str(i) + str(inspecting))
                inspected.append(inspecting.copy())
                
    inspected[0]={'w':keys.index(END), "l":0}

    print(inspected)
    for i in inspected:
        print(keys[i['w']])



def djiskstra(start, end, processed, itterations, stack, found=False):
    si = keys.index(start)
    ei = keys.index(end)

    if len(itterations['rows']) == 0:
        current_row = graph[si]

        for i, n in enumerate(current_row):
             if n!=0 and i not in BLOCKED:
                  stack.append(i)
        
        processed.append(si)
        itterations["rows"].append(current_row)
        itterations["word"].append(si)

        #status(processed, stack)

        if ei in processed:
            print("end word found")
            found=True
        return keys[stack[0]], end, processed, itterations, stack, found
        #djiskstra(start=keys[stack[0]], end=end, processed=processed, itterations=itterations, stack=stack, found=found)

    else:
        if found:
            path_find(itterations, processed)


        if not found:

            last_row = itterations['rows'][-1]
            curr = last_row[si]
            current_row = graph[si]


            for i, n in enumerate(current_row):
                if n>0 and i not in processed and i not in stack and i not in BLOCKED:
                    current_row[i] = 1 + curr
                    stack.append(i)
                else:
                    current_row[i] = last_row[i]
            

            processed.append(si)
            itterations["rows"].append(current_row)
            itterations["word"].append(si)
            stack.pop(0)

            #status(processed, stack)
            if ei in processed:
                print("end word found")
                found=True

            return keys[stack[0]], end, processed, itterations, stack, found
            #djiskstra(start=keys[stack[0]], end=end, processed=processed, itterations=itterations, stack=stack, found=found)
    

    ###preparation
    # set distances from start_line to 1, 0 and infinite
    # have a current_itteration row that tracks the total distances from the start_line
    # have a dijkstra table list that contains all the steps from the current_itteration row
    # create a stack of the lines that have connections, sorted by the distances
    #### itterative part
    # skip the next step for all the already processed words
    # take first from stack and check if when you increase dist(start_line, stack_element) by one for the neighboring verticies it is lower than total distance of that verticy
    # refresh the total distances
    # refresh the stack
    # if end_word has a distance below infinite it is found and its distance cant further decrease beacause its only about connection and not about weights
    # add the proccesed word to the list of proccessed words
    # append current_itteration to dijkstra table
    ### post itteration
    # reverse djisktra table list
    # look at what word the distance changend from end_word
    # this should be done recursive because the end word is now the word at what the distance changed
    # this is done until you arrive at start word
    pass


if __name__ == "__main__":
    found = False
    start = START
    end = END
    processed=[]
    itterations={"word":[], "rows":[]}
    stack = []
    for i,b in enumerate(BLOCKED):
        BLOCKED[i] = keys.index(b)

    while not found:

        start, end, processed, itterations, stack, found = djiskstra(start=start, end=end, processed=processed, itterations=itterations, stack=stack, found=found)
    path_find(itterations, processed)