import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    month_data = ["all", "january","february", "march", "april", "may", "june"]
    week_day =["all","monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    city=""
    month=""
    day=""
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Choose a city from Chicago, New York City or Washington: ").lower()
#    if city in list(city_data.keys()):
#        print('ff')
    
    # get user input for month (all, january, february, ... , june)
    month = input("Choose a month from january - june or all of the month from january - june: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Choose a day from 7 days of the week: ").lower()
    
    while (city in list(city_data)) and (month in month_data) and (day in week_day):
        print('-'*40)
        return city, month, day




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city_data[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["week_day"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour
    if month!= "all":
        months =  ["january","february", "march", "april", "may", "june"]
        month = months.index(month)+1
        df = df[df["month"]==month]
    if day!="all":
        df=df[df["week_day"]==day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df["month"].mode()[0]
    months_dict = {1: "january",2:"february",3:"march",4:"april",5:"may",6:"june"}
    for k,v in months_dict.items():
        if common_month==k:
            print("The most common month is: {}".format(v.title()))
    
    # display the most common day of week
    common_week_day = df["week_day"].mode()[0]
    print("The most common day of week is: {}".format(common_week_day))

    # display the most common start hour
    common_hour = df["hour"].mode()[0]
    print("The most common hour of the day is: {}.00".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df["Start Station"].value_counts()
    print("Most Commanly used start statrion is: \n{}".format(common_start_station))

    # display most commonly used end station
    common_end_station = df["End Station"].mode()
    print("Most Commonly used End Station is: \n{} ".format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_station = df.groupby(["Start Station","End Station"]).size()
    combine_station = common_station.to_frame(name = 'size').reset_index()
    print("Frequently used station combination is: {}".format(combine_station.max()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df["Trip Duration"].sum()
    total_time = total_time/(60*60)
    print("Total Travel Time is: {}".format(total_time))


    # display mean travel time
    avg_time = df["Trip Duration"].mean()
    print("Average Travel Time is: {}".format(avg_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df["User Type"].value_counts()
    print("Total of Different User Types: \n{}".format(user_type_count))

    # Display counts of gender
    if "Gender" in df.columns:
        df["Gender"].fillna("Male",inplace=True) #Replacing NAN with mode value Male.
        gender_count = df["Gender"].value_counts()
        print("Total Number of Male and Female: \n{}".format(gender_count))
    else:
        print("Gender Not Found in Washington City")


    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        avg_birth_year=int(df["Birth Year"].mean()) # Finding mean value of birth year column
        df["Birth Year"].fillna(avg_birth_year,inplace = True)  # Replacing avg birth year to NAN values
    
        earliest_birth_year = df["Birth Year"].min() # Calculating the earliest year of birth
        print("Earliest Birth Year is: {}".format(int(earliest_birth_year)))
    
        recent_birth_year = df["Birth Year"].max() # Calulating recent birth year
        print("Most recent Birth Year is: {}".format(int(recent_birth_year)))

        common_birth_year = df["Birth Year"].mode() # Calculating most common birth year
        print("Most Common Birth Year is: {}".format(int(common_birth_year)))
    else:
        print("Birth Year Not Found in Washington City")
        
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_req = input("\nWould you like to see the raw data of selected city?Enter yes or no.\n")
        print(raw_data_req)
        if raw_data_req == "yes":
            print(df.head(5))
            ans = input("\nWould you like to see 5 more rows of raw data?Enter yes or no.\n")
            start_index, end_index = 6,11
            df=df.reset_index()
            while ans == "yes":
                print(df.iloc[start_index:end_index])
                start_index+=5
                end_index+=5
                ans = input("\nWould you like to see 5 more rows of raw data?Enter yes or no.\n")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
