import sys
import re

def main():
  with open(sys.argv[1], 'r') as file:
    lines = file.read().splitlines()

  p1Wins=0
  p2Wins=0
  f = open(sys.argv[2], "a")

  for j in range(0, len(lines)):
    allmoves = lines[j].split(' ')
    player1moves = allmoves[:5]
    player2moves = allmoves[5:]

    p1_firsts = []
    p2_firsts = []
    p1_seconds = []
    p2_seconds = []

    p1Moves = []
    p2Moves = []
    p1Suits = []
    p2Suits = []

    for i in range(0, len(player1moves)):
      p1_firsts.append(player1moves[i][0])
      p1_seconds.append(player1moves[i][1])
    p1_firsts.sort(key=alphaNumOrder)
    p1_seconds.sort(key=alphaNumOrder)
    p1Moves.append(p1_firsts)
    p1Suits.append(p1_seconds)

    for i in range(0, len(player2moves)):
      p2_firsts.append(player2moves[i][0])
      p2_seconds.append(player2moves[i][1])
    p2_firsts.sort(key=alphaNumOrder)
    p2_seconds.sort(key=alphaNumOrder)
    p2Moves.append(p2_firsts)
    p2Suits.append(p2_seconds)

    #MORE TO BE DONE
    res = finalRank(p1_firsts, p1_seconds,p2_firsts, p2_seconds)
    if res[0]:
      p1Wins +=1
    elif res[1]:
      p2Wins +=1
    elif not res[0] and not res[1]:
      print("some edge case is missing")
    # print("PLAYER1-", p1Wins, "   PLAYER2-", p2Wins)    
  f.write('PLAYER 1: ' + '%d' % p1Wins)
  f.write('\nPLAYER 2: ' + '%d' % p2Wins)
  f.close()
  print("FINAL PLAYER1-", p1Wins, "   FINAL PLAYER2-", p2Wins)

def alphaNumOrder(string):
   return ''.join([format(int(x), '05d') if x.isdigit() else x for x in re.split(r'(\d+)', string)])

def toReplace(cards):
  newCards = list(map(lambda x:14 if x=="A" else x,cards))
  newCards = list(map(lambda x:10 if x=="T" else x,newCards))
  newCards = list(map(lambda x:11 if x=="J" else x,newCards))
  newCards = list(map(lambda x:12 if x=="Q" else x,newCards))
  newCards = list(map(lambda x:13 if x=="K" else x,newCards))
  newCards = [ int(x) for x in newCards ]
  return newCards

def isAce(cards):
  isAce= False
  for i in range(len(cards)):
    if cards[i]==14:
      isAce= True
      return isAce
  return isAce

# Arithmatic Progression formula
def isConsecutive(cards):
  if sorted(cards) == list(range(min(cards), max(cards)+1)):
    return True
  return False

# return rank, bool, highest card
def isHighCard(cards):
  return 1, True, max(cards)

# checks for pair, 2pair, 3pair, 4Pair
def allPair(cards):
  freqs = {}
  no_of_pairs=0
  no_threeKind = 0
  no_fourKind = 0
  max_four=0
  max_three=0
  max_two=[]

  maxValCard = max(cards)
  for i in cards:
      freqs[i] = freqs.get(i, 0) + 1
  if len(freqs) <= 4:
    for i in freqs:
      if freqs[i] == 2:
        no_of_pairs += 1
        max_two.append(i)
      if freqs[i] == 3:
        no_threeKind =1
        max_three = i
      if freqs[i] == 4:
        no_fourKind =1
        max_four = i
    return [True if no_of_pairs > 0 else False, max_two], 2, [True if no_of_pairs == 2 else False, max_two], [True if no_threeKind ==1 else False, max_three],[True if no_fourKind ==1 else False, max_four], no_of_pairs, maxValCard
  return [False, 2]

def isStraight(cards):
  maxValCard = max(cards)
  if isConsecutive(cards):
    return 5, True, maxValCard
  else:
    return 5, False

# rank 6
def isFlush(card_nos, suites):
  freqs = {}
  no_of_pairs=0
  maxValCard = max(card_nos)
  for i in suites:
      freqs[i] = freqs.get(i, 0) + 1
  if len(freqs) ==1:
    return 6, True, maxValCard
  return 6, False

# rank 7
def isFullHouse(cards):
  pair_result = allPair(cards)
  if pair_result[0] and pair_result[0][0] and pair_result[3] and pair_result[3][0]:
    return 7, True, pair_result[0][1][0], pair_result[3][1] 
  return 7, False

# rank 9
def isStraightFlush(card_nos, suites):
  if_flush = isFlush(card_nos, suites)
  if if_flush[1]:
    if_cons = isStraight(card_nos)
    if if_cons[1]:
      return 9, True
    return 9, False
  return 9, False

# rank 10
def isRoyalFlush(card_nos, suites):
  isTen = 0
  isJack=0
  isQueen=0
  isKing=0

  if_flush = isFlush(card_nos, suites)
  if if_flush[1]:
    if isAce(card_nos):
      for i in card_nos:
        if (i == 10):
          isTen +=1
        if (i == 11):
          isJack +=1
        if (i == 12):
          isQueen +=1
        if (i == 13):
          isKing +=1
      return 10, True if isTen ==1 and isJack ==1 and isQueen ==1 and isKing==1 else False
    return 10, False
  return 10, False

def returnMaxHigh(cards1, cards2):
  if max(cards1)==max(cards2):
    cards1.remove(max(cards1))
    cards2.remove(max(cards2))
    return returnMaxHigh(cards1, cards2)
  elif max(cards1) > max(cards2):
    return 1
  elif max(cards1) < max(cards2):
    return 2

def finalRank(p1_firsts, p1_seconds,p2_firsts, p2_seconds):
  p1cards = toReplace(p1_firsts)
  p2cards = toReplace(p2_firsts)
  p1cards.sort()
  p2cards.sort()

  p1hasWon = False
  p2hasWon = False

  p1_res3 = isHighCard(p1cards)
  p1_res4 = allPair(p1cards)
  p1_res5 = isStraight(p1cards)
  p1_res6 = isFlush(p1cards, p1_seconds)
  p1_res7 = isFullHouse(p1cards)
  p1_res8 = isStraightFlush(p1cards, p1_seconds)
  p1_res9 = isRoyalFlush(p1cards, p1_seconds)

  p2_res3 = isHighCard(p2cards)
  p2_res4 = allPair(p2cards)
  p2_res5 = isStraight(p2cards)
  p2_res6 = isFlush(p2cards, p2_seconds)
  p2_res7 = isFullHouse(p2cards)
  p2_res8 = isStraightFlush(p2cards,p2_seconds)
  p2_res9 = isRoyalFlush(p2cards, p2_seconds)

  # royal Flush
  if p1_res9[1]:
    # print("001:")
    p1hasWon = True
    return [p1hasWon, p2hasWon]    
  elif p2_res9[1]:
    # print("1:")
    p2hasWon = True
    return [p1hasWon, p2hasWon]

  # straightflush
  if p1_res8[1] and not p1hasWon and not p2hasWon:
    # print("12:")
    p1hasWon = True
    return [p1hasWon, p2hasWon]
  elif p2_res8[1] and not p1hasWon and not p2hasWon:
    # print("123:")
    p2hasWon = True
    return [p1hasWon, p2hasWon]

  # FOUR KIND
  if len(p1_res4)>=5 and len(p2_res4)>=5 and p1_res4[4][0] and p2_res4[4][0] and not p1hasWon and not p2hasWon:
    # print("4k222")
    if p1_res4[4][1]> p2_res4[4][1]:
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    elif p1_res4[4][1]< p2_res4[4][1]:
      p2hasWon = True
      return [p1hasWon, p2hasWon]   
  if len(p1_res4)>=5 and p1_res4[4][0] and not p1hasWon and not p2hasWon:
    # print("4k1")
    p1hasWon = True 
    return [p1hasWon, p2hasWon]
  if len(p2_res4)>=5 and p2_res4[4][0] and not p1hasWon and not p2hasWon:
    # print("4k1")
    p1hasWon = True 
    return [p1hasWon, p2hasWon]

  # FullHouse
  if p1_res7[1] and p2_res7[1] and not p1hasWon and not p2hasWon:
    # chck highest 3p and 2P
    # print("777:")
    if p1_res7[3] > p2_res7[3]:
      # print("7676:")
      p1hasWon = True
      return [p1hasWon, p2hasWon]
    if p1_res7[3] < p2_res7[3]:
      # print("725:")
      p2hasWon = True
      return [p1hasWon, p2hasWon]
    if p1_res7[3] == p2_res7[3]:
      if p1_res7[2] > p2_res7[2]:
        # print("7232:")
        p1hasWon = True
        return [p1hasWon, p2hasWon]
      if p1_res7[2] < p2_res7[2]:
        # print("715:")
        p2hasWon = True
        return [p1hasWon, p2hasWon]
  if p1_res7[1] and not p1hasWon and not p2hasWon:
    # print("7:")
    p1hasWon = True
    return [p1hasWon, p2hasWon]
  elif p2_res7[1] and not p1hasWon and not p2hasWon:
    # print("700:")
    p2hasWon = True
    return [p1hasWon, p2hasWon]

  #FLUSH
  if p1_res6[1] and p2_res6[1] and not p1hasWon and not p2hasWon:
    # print("666:")
    if p1_res6[2]>  p2_res6[2]:
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    elif p2_res6[2]> p1_res6[2]:
      p2hasWon = True
      return [p1hasWon, p2hasWon]
  if p1_res6[1] and not p1hasWon and not p2hasWon:
    # print("6:")
    p1hasWon = True
    return [p1hasWon, p2hasWon]
  elif p2_res6[1] and not p1hasWon and not p2hasWon:
    # print("600:")
    p2hasWon = True
    return [p1hasWon, p2hasWon]

  # Straight
  if p1_res5[1] and p2_res5[1] and not p1hasWon and not p2hasWon:
    # print("555:")
    if p1_res5[2]>  p2_res5[2]:
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    elif p2_res5[2]> p1_res5[2]:
      p2hasWon = True
      return [p1hasWon, p2hasWon]
  if p1_res5[1] and not p1hasWon and not p2hasWon:
    # print("5:")
    p1hasWon = True
    return [p1hasWon, p2hasWon]
  elif p2_res5[1] and not p1hasWon and not p2hasWon:
    # print("500:")
    p2hasWon = True
    return [p1hasWon, p2hasWon]

  # THREE KIND
  if len(p1_res4)>=4 and  len(p2_res4)>=4 and p1_res4[3][0] and p2_res4[3][0] and not p1hasWon and not p2hasWon:
    # print("3k222")
    if p1_res4[3][1]> p2_res4[3][1]:
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    elif p1_res4[3][1]< p2_res4[3][1]:
      p2hasWon = True
      return [p1hasWon, p2hasWon]
  if len(p1_res4)>=4  and p1_res4[3][0] and not p1hasWon and not p2hasWon:
    # print("3k1")
    p1hasWon = True 
    return [p1hasWon, p2hasWon]
  if len(p2_res4)>=4  and p2_res4[3][0] and not p1hasWon and not p2hasWon:
    # print("3k2")
    p2hasWon = True 
    return [p1hasWon, p2hasWon]

  # TWO PAIRS
  if len(p1_res4)>=3 and len(p2_res4)>=3 and p1_res4[2][0] and p2_res4[2][0] and not p1hasWon and not p2hasWon:
    # print("22k222")
    if max(p1_res4[2][1])> max(p2_res4[2][1]):
      # print("trueTWOpair")
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    elif max(p1_res4[2][1])< max(p2_res4[2][1]):
      p2hasWon = True
      return [p1hasWon, p2hasWon]
    elif p1_res4[2][1]== p2_res4[2][1]:
      if p1_res4[6]>p2_res4[6]:
        p1hasWon = True 
        return [p1hasWon, p2hasWon]
      else:
        p2hasWon = True 
        return [p1hasWon, p2hasWon]
  if len(p1_res4)>=3 and p1_res4[2][0] and not p1hasWon and not p2hasWon:
    # print("2lfk1")
    p1hasWon = True 
    return [p1hasWon, p2hasWon]
  if len(p2_res4)>=3 and p2_res4[2][0] and not p1hasWon and not p2hasWon:
    # print("2lfk2")
    p2hasWon = True 
    return [p1hasWon, p2hasWon]

  # ONE PAIR - 
  if p1_res4[0] and p2_res4[0] and p1_res4[0][0] and p2_res4[0][0] and not p1hasWon and not p2hasWon:
    # print("1k222", p1_res4[0] , p2_res4[0])
    if max(p1_res4[0][1])> max(p2_res4[0][1]):
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    elif max(p1_res4[0][1])< max(p2_res4[0][1]):
      p2hasWon = True
      return [p1hasWon, p2hasWon]
    elif p1_res4[0][1]== p2_res4[0][1]:
      if p1_res4[6]>p2_res4[6]:
        p1hasWon = True 
        return [p1hasWon, p2hasWon]
      else:
        p2hasWon = True 
        return [p1hasWon, p2hasWon]
  if p1_res4[0] and p1_res4[0][0] and not p1hasWon and not p2hasWon:
    # print("1kd1")
    p1hasWon = True 
    return [p1hasWon, p2hasWon]
  if p2_res4[0] and p2_res4[0][0] and not p1hasWon and not p2hasWon:
    # print("1kd2")
    p2hasWon = True 
    return [p1hasWon, p2hasWon]


  # HIGHEST CARD DECK
  if p1_res3[1] and p2_res3[1] and p1_res3[2] == p2_res3[2] and not p1hasWon and not p2hasWon:
    re = returnMaxHigh(p1cards, p2cards)
    if re ==1:
      p1hasWon = True 
      return [p1hasWon, p2hasWon]
    if re ==2:
      p2hasWon = True 
      return [p1hasWon, p2hasWon]
  if p1_res3[1] and p1_res3[2] > p2_res3[2] and not p1hasWon and not p2hasWon:
    # print("lastt")
    p1hasWon = True 
    return [p1hasWon, p2hasWon]
  if p2_res3[1] and p1_res3[2] < p2_res3[2] and not p1hasWon and not p2hasWon:
    # print("lastt22")
    p2hasWon = True 
    return [p1hasWon, p2hasWon]

  # return [p1hasWon, p2hasWon]

if __name__== "__main__":
    print('starting the POKER game!')
    main()
    print('Congrats Winners!')