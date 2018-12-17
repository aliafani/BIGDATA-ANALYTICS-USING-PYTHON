from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordTrigramCount(MRJob):
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                  reducer=self.reducer),
            MRStep(reducer=self.reducer_top10)
        ]

    def mapper(self, _, line):
        line = line.lower().split()
        for words in zip(line, line[1:], line[2:]):
            yield list((words[0], words[1], words[2])), 1
                                
    def reducer(self, trigram, counts):
        yield None, (trigram, sum(counts))
        
    def reducer_top10(self, _, trigram_count):
        for i in sorted(trigram_count, key=lambda x:x[1], reverse=True)[:10]:
                   yield i


if __name__ == '__main__':
    MRWordTrigramCount.run()