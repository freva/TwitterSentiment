from TwitterSearch import searchTweetsWithLocation

endid = ""
for i in xrange(10):
    results = searchTweetsWithLocation("#sb49", end_id=endid)
    endid = results["low"]
    print results

