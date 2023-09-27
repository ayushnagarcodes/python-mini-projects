import argparse
import math
parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=float)
parser.add_argument("--interest", type=float)
args = parser.parse_args()
#  An error message when fewer than four parameters are provided.
args_list = [args.type, args.payment, args.principal, args.periods, args.interest]
if args_list.count(None) != 1:
    print('Incorrect parameters.')
    exit()
# Main Calculator
if args.type == 'annuity':
    if args.periods == None:
        # An error message when values are negative.
        if args.payment < 0 or args.principal < 0 or args.interest < 0:
            print('Incorrect parameters.')
            exit()
        loan_principal = float(args.principal)
        annuity_monthly_payment = float(args.payment)
        loan_interest = float(args.interest)
        i = loan_interest / (12 * 100)
        n_monthly_payments = math.log(annuity_monthly_payment / (annuity_monthly_payment - i * loan_principal), 1 + i)
        years = (math.ceil(n_monthly_payments)) // 12
        months = (math.ceil(n_monthly_payments)) % 12
        total_months = years * 12 + months
        output = f'It will take {years} years and {months} months to repay this loan!'
        if years == 1:
            print(output.replace('years', 'year'))
        elif years == 0:
            print(output.replace(f' {years} years and', ''))
        if months == 1:
            print(output.replace('months', 'month'))
        elif months == 0:
            print(output.replace(f' and {months} months', ''))
        else:
            print(output)
        print(f'Overpayment = {round(annuity_monthly_payment * total_months - loan_principal)}')
    elif args.payment == None:
        # An error message when values are negative.
        if args.principal < 0 or args.periods < 0 or args.interest < 0:
            print('Incorrect parameters.')
            exit()
        loan_principal = float(args.principal)
        n_monthly_payments = int(args.periods)
        loan_interest = float(args.interest)
        i = loan_interest / (12 * 100)
        annuity_monthly_payment = loan_principal * ((i * (1 + i) ** n_monthly_payments) / ((1 + i) ** n_monthly_payments - 1))
        print(f'Your monthly payment = {math.ceil(annuity_monthly_payment)}!')
        print(f'Overpayment = {round(math.ceil(annuity_monthly_payment) * n_monthly_payments - loan_principal)}')
    elif args.principal == None:
        # An error message when values are negative.
        if args.payment < 0 or args.periods < 0 or args.interest < 0:
            print('Incorrect parameters.')
            exit()
        annuity_monthly_payment = float(args.payment)
        n_monthly_payments = int(args.periods)
        loan_interest = float(args.interest)
        i = loan_interest / (12 * 100)
        loan_principal = annuity_monthly_payment / ((i * (1 + i) ** n_monthly_payments) / ((1 + i) ** n_monthly_payments - 1))
        print(f'Your loan principal = {math.floor(loan_principal)}!')
        print(f'Overpayment = {math.ceil(annuity_monthly_payment * n_monthly_payments - loan_principal)}')
elif args.type == 'diff':
    if args.payment == None:
        # An error message when values are negative.
        if args.principal < 0 or args.periods < 0 or args.interest < 0:
            print('Incorrect parameters.')
            exit()
        loan_principal = float(args.principal)
        loan_interest = float(args.interest)
        n_monthly_payments = int(args.periods)
        i = loan_interest / (12 * 100)
        payment_list = []
        for m in range(1, n_monthly_payments + 1):
            differentiated_payments = (loan_principal / n_monthly_payments) + i * (loan_principal - ((loan_principal * (m - 1)) / n_monthly_payments))
            print(f'Month {m}: payment is {math.ceil(differentiated_payments)}')
            payment_list.append(math.ceil(differentiated_payments))
        print(f'Overpayment = {round(sum(payment_list) - loan_principal)}')
    # An error message because in --type=diff, the payment is different each month, so we can't calculate months or
    # principal, therefore a combination with --payment is invalid.
    else:
        print('Incorrect parameters.')
        exit()
