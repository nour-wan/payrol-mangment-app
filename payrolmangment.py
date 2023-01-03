from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import csv
import heapq


def app():
    put_html('<center><h1> Employee Payroll Management</h1></center>').style('font-style: italic; background-color:#8f6686;')
    put_html('<center><img src="https://media.istockphoto.com/id/1175195276/vector/payroll-concept-with-people-letters-and-icons-flat-vector-illustration-isolated-on-white.jpg?s=612x612&w=0&k=20&c=IfpAlFH2ZS2hYlRPQ171fhQLfDVFsQliJqFhKFMWB8U=" width="600px"></center>')
    put_html('<head><style> body {background-color:white;}</style></head>')
    

    list_of_types = [
        "Normal Employee",
        "Head of the Department",
        "General Director",
        "Guard",
        "Executiv Director"
        ]
    # General Functions
    def payInHour(salary, hour_in_company): 
        return (salary/hour_in_company)
    
    def payInDay(salary):
        return (salary/30)
    
    def incomeTax(salary, income_tax):
        return int((salary*income_tax)/100)
    
    def reward(salary, reward_value):
        return int((salary*reward_value)/100)
    
    def dayWithOutPay(salary, number_of_day):
        return int(number_of_day*payInDay(salary))
    
    #Note: Don't depend on outer variables in functions
    def additionalWorkHours(salary,number_of_overtime_hour,number_of_hour_in_company):
        return int(payInHour(salary,int(number_of_hour_in_company))*number_of_overtime_hour*2)
    
    #Note: Don't depend on outer variables in functions
    def finalSalary(salary, number_of_days, number_of_overtime_hour,reward_value,income_tax,number_of_hour_in_company):
        # Always try to write readable code
        rewarded_salary = salary + reward(salary, reward_value)
        additional_work_hours = additionalWorkHours(salary, number_of_overtime_hour,int(number_of_hour_in_company))
        income_tax_value  = incomeTax(salary, income_tax)
        day_without_pay_value = dayWithOutPay(salary, number_of_days)
        return int(rewarded_salary+additional_work_hours-income_tax_value-day_without_pay_value)
    
    def write_list_to_csv_file(file_name, my_list,open_mode, newline="\r\n"):
        if open_mode not in ['a', 'w','w+']:
            raise ValueError("Open mode in write_list_to_csv_file is not 'a' | 'w' | 'w+' ")
        with open(file_name, open_mode, newline=newline) as fs:
            writer2 =csv.writer(fs)
            writer2.writerow(my_list)
            fs.close()
    
    
    
    def input_list(item_name, csv_file_name):
        print("------------------------------")
        my_list=[]
        for employee_type in list_of_types:
            item = int(input(f"The {item_name} of {employee_type} please: "))
            my_list.append(item)
        write_list_to_csv_file(csv_file_name, my_list,open_mode='w',newline='')
        for index, item in enumerate(my_list):
            print(f"{list_of_types[index]} {item_name}: {item}")
        return my_list
    
    def input_number_of_hour_in_company():
        num_of_hours =int(input("Number of hour in company in month please: "))
        num=[num_of_hours]
        write_list_to_csv_file('number of hour in company.csv', num,open_mode='w',newline='')
        print(f"number_of_hour_in_company: {num_of_hours}")
        return int(num_of_hours)
    
    def read_list(file_name):
        my_list = []
        with open(file_name, 'r') as myfile:
            csv_content = list(csv.reader(myfile))
            for line in csv_content:
                my_list.append(line)
        my_list = list(filter(lambda x: x, my_list))
        return my_list
    
    def read_employee_data():
        table=[]
        with open('payrol.csv','r') as myFile:
                csv_content=csv.reader(myFile) 
                for line in csv_content:
                    # print(line)
                    table.append(line)
        put_table(table)
                

    def get_employee_info(salaries,rewards,income,number_of_hour_in_company,date):
        global number_of_days
        global number_of_overtime_hour
        name = input("Enter the employee's name: ")
        
    
        date_of_join_employee = input("Enter the emplyee's joining date: ")
        
        job=select("Enter the position of the employee:\n"
                        "1_Normal Employee,\n"
                        "2_Head of the Department,\n"
                        "3_General Director,\n"
                        "4_a Guard,\n"
                        "5_Executive Director \n",[1,2,3,4,5])

    
        #Note: Don't repeat your self
        salary = int(salaries[job-1]) # 0 = job-1
        income_tax = int(income[job-1])
        reward_value = int(rewards[job-1])
        
        print(f"Employee salary : {salary}")
        print(f"Employee income tax : {income_tax}")
        print(f"Employee reward value : {reward_value}")
    
        income_tax_employee = incomeTax(salary, income_tax)
    
        
        reward_employee = reward(salary, reward_value)
    
        pay=select("Do you want to pay reward for this employee yes\\no ?\n" ,['yes','no'] )
        if pay =='yes':
            pay = reward_employee
        elif pay=='no':
            pay = 0
 
    
        number_of_days = int(input("Enter number of vacation days without pay: "))
        day_WithOut_Pay_employee = dayWithOutPay(salary, number_of_days)
        number_of_overtime_hour = int(input("Enter number of additional Work Hours: "))
        additional_Work_Hours = additionalWorkHours(salary, number_of_overtime_hour,number_of_hour_in_company)
        final_salary_employee = finalSalary(salary, number_of_days, number_of_overtime_hour,reward_value,income_tax,number_of_hour_in_company)
        print("------------------------------")
    
        employee_info = []
        employee_info.append(name)
        employee_info.append(date_of_join_employee)
        employee_info.append(list_of_types[job-1])
        employee_info.append(salary)
        employee_info.append(income_tax_employee)
        employee_info.append(pay)
        employee_info.append(day_WithOut_Pay_employee)
        employee_info.append(additional_Work_Hours)
        employee_info.append(final_salary_employee)
        employee_info.append(date)
        return employee_info
    
    def update_data():
        number_of_hour_in_company = input_number_of_hour_in_company()
    
        salaries = input_list("salary","salary.csv")
        
        rewards = input_list("reward","reward.csv")
        
        income = input_list("income tax","income tax.csv")
    
        print("------------------------------")
    
        list_of_employees_info = [["name","date of join", "job", "salary", "income tax",
                                  "reward", "day without pay", "additional work hours", "final salary","the date"]]
        
        number_of_employee = int(input("Number of employees: "))
        
        date=input("Today date: ")
    
        for i in range(number_of_employee):
            list_of_employee = get_employee_info(salaries,rewards,income,number_of_hour_in_company,date)
            list_of_employees_info.append(list_of_employee)
    
        put_table(list_of_employees_info)
        print("------------------------------")
    
        with open("payrol.csv",'a',newline='') as fs:
            writer2 =csv.writer(fs)
            writer2.writerows(list_of_employees_info)
            fs.close()
    
    def add_new_employee(salaries,rewards,income,number_of_hour_in_company_int):
        new_employee_list=[]
        number_of_employee = int(input("Number of employees: "))
        date=input("Today date: ")
        for i in range(number_of_employee):
            list_of_employee = get_employee_info(salaries,rewards,income,number_of_hour_in_company_int,date)
            new_employee_list.append(list_of_employee)
    
        with open("payrol.csv",'a',newline='') as fs:
            writer2 =csv.writer(fs)
            writer2.writerows(new_employee_list)
            put_table(new_employee_list)
            fs.close()    
        popup("Added.")
    
    def update_data_of_employee(salaries,rewards,income,number_of_hour_in_company_int):
        file = open('payrol.csv', 'r')
        Reader = csv.reader(file)
        L = []
        update_name = input("Enter the employee's name to be updated data :\n ")
        Found = False
        for row in Reader:
            if row[0] == str(update_name):
                Found = True
                j = int(select('choices:\n1-update name\n2-update date of join\n3-update job\n4-update day without pay\n5-update additional work hours\n',[1,2,3,4,5]))
                number_of_days=int(row[6])//payInDay(int(row[3]))
                number_of_overtime_hour=int(row[7])//payInHour(int(row[3]),number_of_hour_in_company_int)
                reward_value=(int(row[5])*100)//(int(row[3]))
                income_tax=(int(row[4])*100)//(int(row[3]))
                if j==1:
                    new_name = input(f"True name of {update_name}:\n ")
                    row[0] = new_name
                elif j==2:
                    new_dateOfJoin = input(f"True date of joining for {update_name}:\n ")
                    row[1]=new_dateOfJoin
                elif j==3:                    
                    new_job = int(select("the true job is,choices:\n1-Normal Employee\n2-Head of the Department\n3-General Director\n4-a Guard\n5-Executiv Director\n",['1','2','3','4','5']))

                    salary = int(salaries[new_job-1])
                    income_tax = int(income[new_job-1])
                    reward_value = int(rewards[new_job-1]) 
                    row[2] =list_of_types[new_job-1] 
                    row[3] = int(salaries[new_job-1])
                    row[4] = incomeTax(salary, income_tax)
                    row[5] = reward(salary, reward_value)
                    row[6] =dayWithOutPay(salary,number_of_days)
                    row[7]=additionalWorkHours(salary,number_of_overtime_hour,number_of_hour_in_company_int)
                    row[8]=finalSalary(salary,number_of_days, number_of_overtime_hour,reward_value,income_tax,number_of_hour_in_company_int)
                elif j==4:
                    g=row[2]
                    index_g=list_of_types.index(g)                   
                    new_dayWithoutPay = int(input(f"True day without pay for {update_name}:\n"))                    
                    salary = int(salaries[index_g])
                    row[6] = dayWithOutPay(salary, new_dayWithoutPay)
                    row[8]=finalSalary(salary,number_of_days, number_of_overtime_hour,reward_value,income_tax,number_of_hour_in_company_int)
                elif j==5:
                    h=row[2]
                    index_h=list_of_types.index(h)
                    new_additionalWorkHours = int(input(f"True additional work hours for {update_name}:\n"))
                    salary = int(salaries[index_h])                    
                    row[7] = dayWithOutPay(salary, new_additionalWorkHours)
                    row[8]=finalSalary(salary,number_of_days, number_of_overtime_hour,reward_value,income_tax,number_of_hour_in_company_int)
            L.append(row)
        file.close()
        if Found == False:
            put_text("The employee Not found")
        else:
            file = open('payrol.csv', 'w+', newline='')
            Writer = csv.writer(file)
            Writer.writerows(L)
            put_table(L)
            file.seek(0)
            Reader = csv.reader(file)
            for row in Reader:
                print(row)
            file.close()
            popup("Updated")
    
    def delete_data_of_employee():
        file=open('payrol.csv','r')
        Reader=csv.reader(file)
        list_after_update=[]
        delete_name=input("Enter the employee's name to delete : ")
        Found=False
        for row in Reader:
            if row[0]==str(delete_name):
                Found=True
            else:
                list_after_update.append(row)
        file.close()
        if Found==False:
            put_text("The employee not found")
        else:
            file=open('payrol.csv','w+',newline='')
            Writer=csv.writer(file)
            Writer.writerows(list_after_update)
            put_table(list_after_update)
            file.seek(0)
            Reader=csv.reader(file)
            for row in Reader:
                print(row)
            popup("Deleted")
    
    def top5(final,namea):
            u=[]
            t=heapq.nlargest(1,final)
            index1=final.index(t[0])
            final.remove(t[0])
            u.append(namea[index1])
            namea.remove(namea[index1])
            # print(u,end=' ')
            put_text(u[0])
            # put_text(" ")
    def top_5_employee():
        put_html('<h3>Top 5 paid employees are:</h3>\n').style()
        with open('payrol.csv','r') as myfile8:
            csv_content8= csv.reader(myfile8,delimiter=',')
            z=[]
            e=[]
            for row in csv_content8:
                sal=row[8]
                fina=row[0]
                z.append(sal)
                e.append(fina)
            myfile8.close()
        z = list(filter(lambda x: x, z))
        e = list(filter(lambda x: x, e))
        final=z[1:]
        namea=e[1:]
        top5(final,namea),top5(final,namea),top5(final,namea),top5(final,namea),top5(final,namea)
        
    
    def less5(final,namea):
            u=[]          
            t=list(heapq.nsmallest(1,final))
            index1=final.index(t[0])
            final.remove(t[0])
            u.append(namea[index1])
            namea.remove(namea[index1])
            put_text(u[0])
    def less_5_employee():
        put_html('<h3>Less 5 paid employees are:</h3>\n')
        with open('payrol.csv','r') as myfile8:
            csv_content8= csv.reader(myfile8,delimiter=',')
            z=[]
            e=[]
            for row in csv_content8:
                sal=row[8]
                fina=row[0]
                z.append(sal)
                e.append(fina)
            myfile8.close()
        z = list(filter(lambda x: x, z))
        e = list(filter(lambda x: x, e))
        final=z[1:]
        namea=e[1:]
        less5(final,namea),less5(final,namea),less5(final,namea),less5(final,namea),less5(final,namea) 
        
        
    def total_salaries():
        with open('payrol.csv','r') as myfile8:
            csv_content8= csv.reader(myfile8,delimiter=',')
            final = []
            for row in csv_content8:
                sal=row[8]
                if sal=="final salary":
                    pass
                else:
                    final.append(int(sal))
            myfile8.close()
        final = list(filter(lambda x: x, final))
        final_salaries=(final[:])
        put_text(sum(final_salaries))
        
    def get_and_print_current_data():
        number_of_hour_in_company =read_list('number of hour in company.csv')
        number_of_hour_in_company_int=int(number_of_hour_in_company[0][0])
        print(f"number of hour in company: {number_of_hour_in_company_int}")
        
        categories=[str(x) for x in list_of_types]
        print('categories are : ',categories)

        salaries_str_element = read_list('salary.csv')
        salaries_int_element=salaries_str_element[0]
        salaries=[int(x) for x in salaries_int_element]      
        print(f"the salaries: {salaries}")
       
        rewards_str = read_list('reward.csv')
        rewards_int=rewards_str[0]
        rewards=[int(x) for x in rewards_int] 
        print(f"the rewards: {rewards}")
    
        income_str = read_list('income tax.csv')
        income_int=income_str[0]
        income=[int(x) for x in income_int] 
        print(f"the income tax: {income}")
    
        return salaries,rewards,income,number_of_hour_in_company_int
    
    def user_interaction():
        salaries,rewards,income,number_of_hour_in_company_int = get_and_print_current_data()
    
        user_choice=select('choices:',
                          options=["just read employee data",
                                    "add new employee",
                                    "update data of employee",
                                    "delete data of employee",
                                    "the top 5 employees payrol",
                                    "the less 5 employees payrol",
                                    "Total employee salaries"]
        )
        ###########read
        if user_choice=="just read employee data":
            read_employee_data()
        ################add            
        elif user_choice=="add new employee": 
            add_new_employee(salaries,rewards,income,number_of_hour_in_company_int)
        ################update        
        elif user_choice=="update data of employee":
            update_data_of_employee(salaries,rewards,income,number_of_hour_in_company_int)
        ####################delete        
        elif user_choice=="delete data of employee":
            delete_data_of_employee()
        #########top5                        
        elif user_choice=="the top 5 employees payrol":
            top_5_employee()
        #########less5
        elif user_choice=="the less 5 employees payrol":
            less_5_employee()
        ############total salaries
        elif user_choice=="Total employee salaries":
            total_salaries()
        #################    

    ################################################################
    if __name__ == "__main__":
        while True:
            user_choice = select("Do you want to update data? [yes/no]\n",['yes','no'])
            if user_choice == "yes":
                update_data()
            if user_choice=="no":
                user_interaction()
            restart=select("Do you want to start again yes\\no ?\n" ,['yes','no'])
            if restart=="no":
                exit()

start_server(app,port=1601,debug=True)
