import sys,pickle,pathlib,os,time

class BankSystem:
    accname = ''
    accno = ''
    isactive = False
    status = ''
    balance = 25.0
    min_balance = 100

    def createAccount(self):
        print(end='Enter holder name: ')
        self.accname = str(input())
        print(end='Enter account number: ')
        self.accno = str(input())
        print(end='Deposit: ')
        self.balance += float(input())
        return True


def makeAccount():
    account = BankSystem()
    account.createAccount()
    if account.balance < account.min_balance:
        print('No sufficient funds in your account, so account is inactive')
    writeAccountsFile(account)


def writeAccountsFile(account):
    file = pathlib.Path('accounts.acct')
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            acctlist.append(account)
    else:
        acctlist = [account]
    with open(file,'wb') as newfile:
        pickle.dump(acctlist,newfile)   


def view_my_record(number):
    file = pathlib.Path('accounts.acct')
    found = False
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            for record in acctlist:
                if record.accno == number:
                    print('Account Balance: %s\tStatus: %s' % (record.balance,record.status))
                    found = True
    else:
        print('No record to search through')
    if not found:
       print('Couldn\'t find record with this account number')


def editAccount(number):
    file = pathlib.Path('accounts.acct')
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            for record in acctlist:
                if record.accno == number:
                    print('Account name: %s Account number: %s' % (record.accname.capitalize(),record.accno))
                    record.accname = str(input('Edit holder name: '))
                    record.accno = str(input('Edit account number: '))
                    option = str(input('Would you like to update your balance too? y/n: '))
                    if option.startswith('y') or option.startswith('Y'):
                        record.balance += float(input('Enter amount to deposit: '))
            with open(file,'wb') as file:
                pickle.dump(acctlist,file)
    return True


def depositAndWithdraw(accno,option):
    successful = False
    file = pathlib.Path('accounts.acct')
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            for record in acctlist:
                if record.accno == accno:
                    if option == 1:
                        if not record.isactive:
                            amount = float(input('Enter amount to deposit: '))
                            record.balance += amount
                            if record.balance >= record.min_balance:
                                print('Account updated Account is now active Balance:%s',record.balance)
                                successful = True
                            else:
                                print('Account updated! Balance:%s',record.balance)
                                successful = True
                                
                        else:
                            amount = float(input('Enter amount to deposit: '))
                            record.balance += amount
                            print('Account updated Balance:%s',record.balance)
                            successful = True
                            
                    elif option == 2:
                        if not record.isactive:
                            print('Your account is inactive. Cannot withdraw!')
                            successful = False
                        else:
                            amount = float(input('Enter amount to withdraw: '))
                            if amount > record.balance:
                                print('You cannot withdraw more than balance in you account')
                            elif record.balance - amount < record.min_balance:
                                print('You cannot leave less than $100 in your account.')
                                successful = False
                            else:
                                record.balance -= amount
                                print('Account updated! Balance:',record.balance)
                                successful = True
    else:
        print('No records to search through')
    with open(file,'wb') as file:
        pickle.dump(acctlist,file)
    return successful


def displayAll():
    file = pathlib.Path('accounts.acct')
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            print('Account Name\t\tAccount Balance\t\tAccount No\t\tStatus')
            for record in acctlist:
                print('%s\t\t\t$%s\t\t\t%s\t\t%s' % (record.accname.capitalize(),record.balance,record.accno,record.status))
                print()
    else:
        print('No records to display')


def set():
    file = pathlib.Path('accounts.acct')
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            for record in acctlist:
                record.isactive = True if record.balance >= 100 else False
                record.status = 'active' if record.isactive == True else 'inactive'
    else:
        pass
    with open(file,'wb') as file:
        pickle.dump(acctlist,file)


def deleteAccount(number):
    file = pathlib.Path('accounts.acct')
    if file.exists():
        with open(file,'rb') as acctfile:
            acctlist = pickle.load(acctfile)
            newlist = []
            for record in acctlist:
                if record.accno != number:
                    newlist.append(record)
        with open(file,'wb') as file:
            pickle.dump(newlist,file)
    else:
        print('No records to search through')
        return False
    return True

        
def Menu():
    print('\t\t\t************************************\n\t\t\t********** BANKING SYSTEM **********')
    print('\t\t\t************************************\n\t\t\t**** DEVELOPED BY DERRON DERICK ****')
    print('\t\t\t************************************\n\t\t\t************************************')
    pause = input()        

Menu()
print()
usr_input = ''
while usr_input != 8:
    print('1. CREATE AN ACCOUNT\n2. BALANCE ENQUIRY\n3. EDIT ACCOUNT\n4. DEPOSIT\n5. WITHDRAW\n6. DELETE MY ACCOUNT\n7. VIEW ACCOUNT RECORDS\n8. QUIT\nSelect your option: \n')
    usr_input = input('>>> ')
    
    if usr_input == '1':
        makeAccount()
        print('Account Created!')
        set()
            
    elif usr_input == '2':
        number = str(input('Enter Account Number: '))
        view_my_record(number)

    elif usr_input == '3':
        number = str(input('Enter Account Number: '))
        editAccount(number)
        set()

    elif usr_input == '4':
        number = str(input('Enter Account Number: '))
        if depositAndWithdraw(number,1):
            print('Deposit successful!')
            set()

    elif usr_input == '5':
        number = str(input('Enter Account Number: '))
        if depositAndWithdraw(number,2):
            print('Withdrawal successful!')
            set()
        else:
            print('Withdrawal unsuccessful!')
            set()

    elif usr_input == '6':
        number = str(input('Enter Account Number: '))
        if deleteAccount(number):
            print('Account has been closed successfully!')

    elif usr_input == '7':
        displayAll()

    elif usr_input == '8':
        for i in 'Thanks for banking with us. GoodBye...':
            print(i,end='')
            if i == '.':
                time.sleep(0.30)
            time.sleep(0.25)
        sys.exit()

    else:
        print("Invalid choice!")
        


pause = input()

                
