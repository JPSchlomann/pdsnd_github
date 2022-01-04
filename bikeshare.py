import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_correct_input(user_input, expected_inputs):
    """ handling of unexpected or wrong user inputs """
    user_input = user_input.lower().strip()
    while True:
        if user_input in expected_inputs:
            correct_input = user_input
            break
        else:
            print("\nSorry, we can't handle your input! \nPlease choose only between {}".format(expected_inputs))
            user_input = input("Please repeat your input here: ").lower().strip()
    return correct_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City, or Washington? ")
    city = get_correct_input(city,['chicago','new york city','washington'])

    # ask for filters
    filter_input = input("\nWould you like to filter the data by month, day, or not at all? ")
    filter_input = get_correct_input(filter_input,['month','day','not'])

    # additional information for filtering
    if filter_input == 'month':
        # get user input for month (all, january, february, ... , june)
        month = input("\nWhich month - January, February, March, April, May, or June? ")
        month = get_correct_input(month, ['january', 'february', 'march', 'april', 'may', 'june'])
        day = 'all'
    elif filter_input == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ")
        day = get_correct_input(day, ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
        month = 'all'
    else:
        month = 'all'
        day = 'all'

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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday + 1
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # get the corresponding int
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day  = days.index(day) + 1
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode(dropna=True)[0]
    print('Most common month: '+ str(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode(dropna=True)[0]
    print('Most common day: '+ str(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode(dropna=True)[0]
    print('Most common hour: '+ str(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode(dropna=True)[0]
    print('Most common start station: ' + popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode(dropna=True)[0]
    print('Most common end station: ' + popular_end)

    # display most frequent combination of start station and end station trip
    #please see readme for source of this part:
    popular_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start and end station: \n{}'.format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ' + str(travel_time) + ' sec.')

    # display mean travel time
    travel_meantime = df['Trip Duration'].mean()
    print('Mean Travel Time: ' + str(travel_meantime) + ' sec.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_types = df['User Type'].nunique(dropna=True)
    print('Number of user types: ' + str(count_types))

    # Display counts of gender
    if 'Gender' in df:
        count_gender = df['Gender'].nunique(dropna=True)
        print('Number of gender types: ' + str(count_gender))
    else:
        print('Number of gender types: Only for the cities of Chicago and New York available')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest Year of Birth: '+ str(df['Birth Year'].min()))
        print('Most recent Year of Birth: '+ str(df['Birth Year'].max()))
        print('Most common Year of Birth: '+ str(df['Birth Year'].mode(dropna=True)[0]))
    else:
        print('Earliest Year of Birth: Only for the cities of Chicago and New York available')
        print('Most recent Year of Birth: Only for the cities of Chicago and New York available')
        print('Most common Year of Birth: Only for the cities of Chicago and New York available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #stats can only be calculated if there is data available for the customer based filter settings
        if df.empty != True:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            see_raw_data = input('Would you like to see some raw data? Enter yes or no: ')
            see_raw_data = get_correct_input(see_raw_data, ['yes','no'])

            idx = 0
            while see_raw_data == 'yes':
                print(df.iloc[idx:idx+5,:])
                see_raw_data = input('Would you like to see more? Enter yes or no: ')
                see_raw_data = get_correct_input(see_raw_data, ['yes','no'])
                idx += 5
            else:
                restart = input('\nWould you like to restart? Enter yes or no: ')
                restart = get_correct_input(restart, ['yes','no'])
                if restart == 'yes':
                    break
        else:
            print('\nSorry, we don\'t have data for your filter settings. \nPlease try again')


if __name__ == "__main__":
	main()
