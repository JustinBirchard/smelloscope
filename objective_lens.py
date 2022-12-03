# objective_lens
#* Smelloscope Version 1.3
#* file last updated 12/2/22

import config

def group_selection():
    """Interface to allow user to choose group of stocks.

    Returns:
        list: a cleaned list of tickers
    """
    choice = ''
    while choice not in ['y', 'n']:
        choice = input('Would you like to use a preset group of stocks?(y/n): ' )

    if choice == 'y':
        next_choice = ''
        while next_choice not in config.smello['presets'].keys():
            print('')

            for preset in config.smello['presets'].keys():
                print(preset)
            print('')

            next_choice = input('Enter a preset from the choices above: ' )

        stocks = config.smello['presets'][next_choice]

    elif choice == 'n':
        custom_choice = ''
        while custom_choice not in ['y', 'n']:
            custom_choice = input('\nUse a custom group from config file?(y/n): ')

        if custom_choice == 'y':
            print('')
            next_custom_choice = ''
            for custom_group in config.smello['custom'].keys():
                print(custom_group)
            print('')

            while next_custom_choice not in config.smello['custom'].keys():
                next_custom_choice = input('Enter a group from the choices above: ' )

            stocks = config.smello['custom'][next_custom_choice]

        elif custom_choice == 'n':
            print('\nEnter a group of tickers seperated by commas.')
            print('Example: MSFT, AAPL, ADBE\n')
            stocks_str = input(' :')
            stocks = [stock for stock in stocks_str.split(', ')]     

        print('')   

    young_stocks = config.smello['problem_stocks']['young_stocks']
    financial_stocks = config.smello['problem_stocks']['financial_stocks']
    problem_stocks = young_stocks + financial_stocks

    clean_stocks = []
    for stock in stocks:

        if stock not in problem_stocks:
            clean_stocks.append(stock)

        elif stock in problem_stocks and stock == stocks[0]:
            error_msg1 = f"Bummer! The Scope isn't equipped to sniff {stock}. " 
            error_msg2 = 'Please remove it from your group and try again.'
            raise ValueError(error_msg1 + error_msg2)

        elif stock in problem_stocks:
            print(f"\nPoop!\nThe Scope is not equipped for sniffing {stock}")
            print("We'll keep smelling the rest of the stocks in your group.\n")

    return clean_stocks