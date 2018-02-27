import sys
import operator
import pdb

class Freq:
    def __init__(self):
        pass

    def loadfiles(self, childesFile):
        childesLines = open(childesFile, 'r').readlines()
        freqs = self.getFreqs(childesLines)
        return freqs

    def getFreqs(self, lines):
        freqs = {}
        for l in lines:
            if l[0] not in ['@']:
                if not l.startswith('*CHI'):
                    l = l.split('\t')
                    for word in l[1].strip().split():
                        if word not in freqs:
                            freqs[word] = 0
                        freqs[word] += 1
        return freqs

class Balance:
    def __init__(self):
        pass

    def catInput(self, dataDict, _file):
        array = open(_file, 'r').readlines()
        for line in array:
            line = line.strip()
            key = line.split('\t')[2]
            if key not in dataDict:
                dataDict[key] = []
            dataDict[key].append(line)
        return dataDict

    def loadfiles(self, train, dev, test):
        # edit, make this a dict
        data = {}
        data = self.catInput({}, train)
        data = self.catInput(data, dev)
        data = self.catInput(data, test)
        # data = [x.strip() for x in data]
        return data

    def balance(self, cdi, data):
        sortedOutput = []
        sortedCdi = sorted(cdi.items(), key=operator.itemgetter(1))
        sortedCdi.reverse()
        for sc in sortedCdi:
            if sc[0] in data:
                # pdb.set_trace()
                for line in data[sc[0]]:
                    sortedOutput.append(line)
        devtest = []
        for word in data:
            if word not in sortedCdi:
                for line in data[word]:
                    devtest.append(line)
        print(len(sortedOutput), "found in Childes")
        print(len(devtest), "left for dev and test")
        return sortedOutput, devtest

    def writeout(self, found, devtest):
        outfile = open('german-task1-train.balanced', 'w')
        outfile_dev_test = open('german-task1-dev.balanced', 'w')
        for line in found:
            line += '\n'
            outfile.write(line)
        for line in devtest:
            line += '\n'
            outfile_dev_test.write(line)
        outfile.flush()
        outfile_dev_test.flush()
        outfile.close()
        outfile_dev_test.close()

f = Freq()
b = Balance()
# child directed input
cdi = f.loadfiles(sys.argv[1])
data = b.loadfiles(sys.argv[2], sys.argv[3], sys.argv[4])
found, devtest = b.balance(cdi, data)
b.writeout(found, devtest)