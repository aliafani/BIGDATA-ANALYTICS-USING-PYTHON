from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordBigramCount2(MRJob):
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                  combiner = self.combiner,
                  reducer=self.reducer),
            MRStep(reducer=self.reducer_top10)
        ]

    def mapper(self, _, line):                  
        line = line.lower().split()                        
        for words in zip(line, line[1:]):        
            yield list((words[0], words[1])), 1   
            
    def combiner(self, bigram, counts):
        yield bigram, sum(counts)                
                               
    def reducer(self, bigram, counts):           
        yield None, (bigram, sum(counts))
                   
    def reducer_top10(self, _, bigram_count):
        for i in sorted(bigram_count, key=lambda x:x[1], reverse=True)[:10]:
                 yield i

            
if __name__ == '__main__':
    MRWordBigramCount2.run() 