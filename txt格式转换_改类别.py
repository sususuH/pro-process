import os

path = "/home/su/su/pysot-toolkit-master/LASOT/dimp50"
datanames = os.listdir(path)
for dir in datanames:
    path2 = path + '/' + dir
    path1 = "/home/su/su/pysot-toolkit-master/LASOT/M/" + dir
    with open(path1,'w',encoding ='utf - 8') as file:
        with open(path2,'r',encoding ='utf - 8') as infile:
            for line in infile:
                data_line =  line.strip("\n").split(',')
                # print(data_line)
                data = []
                # print(data_line,111)
                for num in range(len(data_line)):
                    data_line[num] =data_line[num]
                    # print(data_line[num])
                    data.append(data_line[num])
                # print(data[0])
                data = data[0].split('\t')
                if len(data) > 2:
                    data2 = str(data[0]) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]) + "\n"
                else:
                    data2 = str(data[0]) + "\n"
                file.write(data2)

            