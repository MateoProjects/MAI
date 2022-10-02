
from os import listdir
from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

class Dataset:
    ##  Parse all XML files in given dir, and load a list of sentences.
    ##  Each sentence is a list of tuples (word, start, end, tag)
    def __init__(self, datadir) :
        self.data = {}
        # process each file in directory
        for f in listdir(datadir) :
   
            # parse XML file, obtaining a DOM tree
            tree = parse(datadir+"/"+f)
   
            # process each sentence in the file
            sentences = tree.getElementsByTagName("sentence")
            for s in sentences :
                sid = s.attributes["id"].value   # get sentence id
                stext = s.attributes["text"].value   # get sentence text
                entities = s.getElementsByTagName("entity")

                spans = []
                for e in entities :
                    # for discontinuous entities, we only get the first span
                    # (will not work, but there are few of them)
                    (start,end) = e.attributes["charOffset"].value.split(";")[0].split("-")
                    typ =  e.attributes["type"].value
                    spans.append((int(start),int(end),typ))
         
                # convert the sentence to a list of tokens
                tokens = self.__tokenize(stext)

                # add gold label to each token, and store it in self.data
                self.data[sid] = []
                for i in range (0,len(tokens)) :
                    # see if the token is part of an entity
                    tokens[i]['tag'] = self.__get_tag(tokens[i], spans)
                    self.data[sid].append(tokens[i])

        
    ## --------- tokenize sentence ----------- 
    ## -- Tokenize sentence, returning tokens and span offsets
    def __tokenize(self, txt):
        offset = 0
        tks = []
        ## word_tokenize splits words, taking into account punctuations, numbers, etc.
        for t in word_tokenize(txt):
            ## keep track of the position where each token should appear, and
            ## store that information with the token
            offset = txt.find(t, offset)
            tks.append({'lc_form':t.lower(), 'form':t, 'start':offset, 'end':offset+len(t)-1} )
            offset += len(t)

        ## tks is a list of quadruples (lc_form,form,start,end)
        return tks


    ## --------- get tag ----------- 
    ##  Find out whether given token is marked as part of an entity in the XML
    def __get_tag(self, token, spans) :
        for (spanS,spanE,spanT) in spans :
            if token['start']==spanS and token['end']<=spanE : return "B-"+spanT
            elif token['start']>=spanS and token['end']<=spanE : return "I-"+spanT
        return "O"
 
    ## ---- iterator to get sentences in the data set
    def sentences(self) :
        for sid in self.data :
            yield self.data[sid]

    ## ---- iterator to get ids for sentence in the data set
    def sentence_ids(self) :
        for sid in self.data :
            yield sid

    ## ---- get one sentence by id
    def get_sentence(self, sid) :
        return self.data[sid]

    ## get sentences as token lists
    def tokens(self) :
        for sid in self.data:
            s = []
            for w in self.data[sid] :
                s.append((sid, w['form'], w['start'], w['end']))
            yield s
