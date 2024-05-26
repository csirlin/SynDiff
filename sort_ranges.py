# sort the ranges.txt by folder name into ranges.sorted.txt
file = open('ranges.txt', 'r')
ranges_str = file.read()
ranges_str_list = ranges_str.split('\n')
summary_str = ranges_str_list[-2]
print(len(ranges_str_list))
ranges_list = []
for line in ranges_str_list[:-2]:
    dash_index = line.find('-')
    colon_index = line.find(':')
    number = int(line[:dash_index-5])
    folder = line[dash_index+2:colon_index]
    rest = line[colon_index+2:]
    ranges_list.append((folder, rest))
    # print(line[:dash_index-5], "|", line[dash_index+2:colon_index], "|", line[colon_index+2:])

ranges_list.sort()
output = open('ranges_sorted.txt', 'w')
for i in range(len(ranges_list)):
    output.write(f"{i+1}/180 - {ranges_list[i][0]}: {ranges_list[i][1]}\n")
output.write(summary_str)