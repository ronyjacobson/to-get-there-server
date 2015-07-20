

if __name__ == '__main__':

    with open("street.csv", "r") as streets:
    	counter = 0
    	fileCounter = 0
    	output= open('streets0.csv', 'w')
    	for line in streets:
	    	if counter == 1500:
	    		counter = 0
	    		fileCounter = fileCounter + 1
	    		output.close()
	    		output= open('streets'+str(fileCounter)+'.csv', 'w')
        	output.write(line)
        	counter= counter +1
        streets.close()