import csv
import pickle

from bs4 import BeautifulSoup

f = open('India_T20_matchcodes.pkl', 'rb')
matchCodes = pickle.load(f)
f.close()

print('opening/creating raw_data.csv file')
out = open('raw_data.csv', 'w')
output = csv.writer(out)

output.writerow(
    ["Opposition, Venue, DayMatch, 1st_Batting, India's_Score, Opp_Score, Wic_Taken, Wic_Given, Result"])

print('fetching data')


def get_page(url):
    try:
        import urllib
        return urllib.request.urlopen(url).read()
    except:
        return ""


for matchCode in matchCodes:
    websiteUrl = "http://www.howstat.com.au/cricket/Statistics/Matches/MatchScorecard_T20.asp?MatchCode=" + matchCode
    page = BeautifulSoup(get_page(websiteUrl), 'html.parser')
    result = page.findAll(attrs={'class': "TextBlack8", 'valign': "top"})

    # getting match date
    matchDate = result[0].contents[0].strip()
    # print(matchDate)

    # getting venue
    venue = result[1].contents[0].split()[-1]
    # print(venue)

    # getting day/night
    if len(result[2].contents[0].split()) == 6:
        day = '1'
    else:
        day = '0'

    # print(day)

    # getting toss result
    tossResult = result[3].contents[0].strip()
    # print(tossResult)

    # getting match result
    matchResult = result[4].contents[0].split()
    if matchResult[0] == 'No' or matchResult[0] == 'Match':
        continue

    if matchResult[0] == 'New' or matchResult[0] == 'South' or matchResult[0] == 'Sri' or matchResult[0] == 'West':
        matchResult = matchResult[0] + matchResult[1]

    elif matchResult[0] == 'United':
        matchResult = matchResult[0] + matchResult[1] + matchResult[2]

    else:
        matchResult = matchResult[0]

    # print(matchResult)

    # getting Man of the match
    manOfMatch = result[5].contents[0].strip()
    # print(manOfMatch)

    # opposition data
    matchTitle = page.findAll(attrs={'class': 'ScoreCardBanner3'})[0].contents[0].split('v')
    before_versus = matchTitle[0].split()
    after_versus = matchTitle[1].split()

    if 'India' not in before_versus:
        if before_versus[-2] == 'New' or before_versus[-2] == 'South' or before_versus[-2] == 'Sri' or before_versus[-2] == 'West':
            opposition = before_versus[-2] + before_versus[-1]
        elif before_versus[-2] == 'Arab':
            opposition = before_versus[-3] + before_versus[-2] + before_versus[-1]
        else:
            opposition = before_versus[-1]

    else:
        if after_versus[0] == 'New' or after_versus[0] == 'South' or after_versus[0] == 'Sri' or after_versus[0] == 'West':
            opposition = after_versus[0] + after_versus[1]
        elif after_versus[0] == 'United':
            opposition = after_versus[0] + after_versus[1] + after_versus[2]
        else:
            opposition = after_versus[0]

    # batting 1st or 2nd
    upperTeam = page.findAll(attrs={'class': "TextBlackBold8", 'valign': "top", 'colspan': "2"})[0].contents[0].split()
    if upperTeam[0] == 'India':
        bat1 = '1'
    else:
        bat1 = '0'

    # scores
    score = page.findAll(attrs={'class': "TextBlackBold8", 'align': "right", 'valign': "top"})
    if bat1 == 1:
        scoreIndia = score[5].contents[0].strip()
        scoreOpposition = score[17].contents[0].strip()
    else:
        scoreIndia = score[17].contents[0].strip()
        scoreOpposition = score[5].contents[0].strip()

    # wickets
    wicket = page.findAll(attrs={'class': "TextBlackBold8", 'valign': "top"})
    # print(wicket)
    w1 = wicket[13].contents[0].split()[0]
    w2 = wicket[30].contents[0].split()[0]
    if w1 == 'SR':  # this happens when we have note and video clips given in particular match
        w1 = wicket[15].contents[0].split()[0]
        w2 = wicket[32].contents[0].split()[0]
    elif w1 == 'Total':  # this happens when we have only one of note or video clips given in particular match
        w1 = wicket[14].contents[0].split()[0]
        w2 = wicket[31].contents[0].split()[0]

    if w1 == 'All':
        w1 = '10'

    if w2 == 'All':
        w2 = '10'

    if bat1 == '0':
        wickets_taken = w1
        wicket_given = w2
    else:
        wicket_given = w1
        wickets_taken = w2

    output.writerow([opposition, venue, day, bat1, scoreIndia, scoreOpposition, wickets_taken, wicket_given, matchResult])
