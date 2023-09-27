# Loan Calculator Usage

Run the python file using command-line by passing the following arguments:

-   `--type` indicates the type of payment: "annuity" or "diff" (differentiated). It's always required.
-   `--payment` is the monthly payment amount. For `--type=diff`, the payment is different each month, so we can't calculate months or principal, therefore a combination with `--payment` is invalid.
-   `--principal` is the initial amount borrowed.
-   `--periods` denotes the number of months needed to repay the loan.
-   `--interest` is the percentage of the principal that is added to the amount owed. Specify this without a percent sign.

**Note:** Only 4 of 5 arguments can be passed in a command out of which `--type` is always required.
<br />

**Examples:**

```
python3 loan-calculator.py --type=diff --principal=1000000 --periods=10 --interest=10
```

```
python3 loan-calculator.py --type=annuity --payment=8722 --periods=120 --interest=5.6
```
