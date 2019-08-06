import re
def preprocess(input_file, output_file):
    tmpfile1 = output_file[0:len(output_file)-4] + '1' + '.csv'
    print(tmpfile1)
    preprocess1(input_file, tmpfile1)
    preprocess2(tmpfile1, output_file)

def preprocess1(input_file, output_file):
    fout = open(output_file, 'w', encoding='utf-8')
    i = 0
    with open(input_file, "r", encoding='utf-8') as f:
        for line in f:
            #line=re.sub('"','',line) 
            line=re.sub('\n','',line)
            
            #非中文输入法的字符删除掉
            line=re.sub('、','',line)  

            if not (line[1:7].isdigit() and (line[1]=='8' or line[1]=='9') and line[8]==','):
                fout.write(line)
            else:
                if i == 0:
                    fout.write(line)
                else:
                    fout.write('\n' + line)
            i = i + 1
    fout.close()
    
def preprocess2(input_file, output_file):
    fout = open(output_file, 'w', encoding='utf-8')
    with open(input_file, "r", encoding='utf-8') as f:
        for line in f:
            #print(line)
            result = re.search('"(.*)","(.*)","(.*)","(.*)"', line)
            line = '%s|%s|%s|%s' %(result.group(1),result.group(2), result.group(3), result.group(4))
            fout.write(line)
            fout.write('\n')

    fout.close()  