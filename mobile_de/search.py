
import threading

from mobile_de.scraper import *

def search(search_params):

    current_url, pagesnr = search_url(search_params)
    # create file name
    carMake = search_params[0]
    if carMake.lower() == 'any':
        carMake = ''
    carModel = search_params[1]
    carMake = carMake.replace(" ", "-")
    carModel = carModel.replace(" ", "-")
    if carModel == "":
        linksFileName = carMake + ".csv"
    else:
        linksFileName = carMake + "_" + carModel + ".csv"

    # get links
    with open(linksFileName, mode="w") as linksFile:
        threads = []
        for i in range(20):
            threadNumber = "Thread " + str(i)
            thread = threading.Thread(target = getCarLinksTemp, args = (threadNumber, current_url, linksFile))
            threads.append(thread)
            thread.start()

            # limit parallel threads number
            if len(threads) == 4:
                for thread in threads:
                    thread.join()
                threads = []
            
            current_url = next_page(current_url, i)

        # wait for all threads to finish execution
        for thread in threads:
            thread.join()
        print("All threads are finished")
        linksFile.close()

    # get links to variable
    car_links = []
    with open(linksFileName, mode="r") as linksFile:
        #for line in linksFile:
        #    carLink.append(line)
        car_links = linksFile.readlines()
        linksFile.close()

    if len(car_links) == 0:
        print("No ads to process")
        print("\====================================/\n\n")
        return
    elif len(car_links) == 1:
        print(len(car_links), "ad to process\n--------------------")
    else:
        print(len(car_links), "ads to process\n--------------------")

    # output file name
    fileName = carMake + "_" + carModel + "_" + search_input[2] + "-" + search_input[3] + "_" + search_input[4] + "-" + search_input[5] + "_" + search_input[6] + "-" + search_input[7] + "_" + search_input[8] + "-" + search_input[9] + ".csv"

    with open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score"])
        # start threading for getting data
        threads = []
        for link in car_links:
            threadNumber = "Thread " + str(car_links.index(link))
            thread = threading.Thread(target = getData, args = (threadNumber, link, csvWriter))
            threads.append(thread)
            thread.start()

            # limit parallel threads number
            if len(threads) == 24:
                for thread in threads:
                    thread.join()
                threads = []

        # wait for all threads to finish execution
        for thread in threads:
            thread.join()
        print("All threads are finished")
        csvFile.close()

    os.chdir(maindir)
    os.chdir('./csv files')
    print("Giving scores to vehicles")
    score(fileName)
    #except:
    #   print("Can not calculate score, possible error")
    os.chdir(maindir)
    print("Search executed successfully")
    print("\====================================/\n\n")
    return fileName

# get temporary car links
def getCarLinksTemp(thread_number, current_url, links_file):
    time_started = time.time()
    print(thread_number, "started at", time_started)
    carLinks = get_car_links(current_url)
    for item in carLinks:
        links_file.write("%s\n" % item)
    print(thread_number, "executed in", time.time() - time_started)


# get data from links
def getData(thread_number, car_link, csv_writer):
    time_started = time.time()
    print(thread_number, "started at", time_started)
    data = get_car_data(car_link)
    csv_writer.writerow([car_link , data[0], data[1], data[2], data[3], data[4]])
    print(thread_number, "executed in", time.time() - time_started)
