class StringCompareUtil():
    def compareAlphaWords(self, word1, word2):
        charMatchCount=0
        charNonMatchCount=0
        deltaSize = len(word2)-len(word1)
        idxW1=0
        idxW2=0
        while idxW1 < len(word1) and idxW2 < len(word2):
            if word1[idxW1] == word2[idxW2]:
                charMatchCount+=1
                idxW1+=1
                idxW2+=1
            elif word1[idxW1]<word2[idxW2]:
                charNonMatchCount+=1
                idxW1+=1
            else:
                idxW2+=1
        return [charMatchCount, charNonMatchCount, deltaSize]

    def rankAlphaWordComparison(self, metadata):
        matchCount=metadata[0]
        nonMatchCount=metadata[1]
        deltaSize=metadata[2]

        matchScore = matchCount-(nonMatchCount*nonMatchCount)
        sizeModifier = pow(.999,deltaSize) if deltaSize>=0 else pow(.9, -deltaSize)
        return matchScore*sizeModifier


