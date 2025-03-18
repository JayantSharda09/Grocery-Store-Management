import mysql.connector
con = mysql.connector.connect(user='root', password='ajjianvi1', host='localhost', database='project')
cursor = con.cursor()

def Update_stock():
    cursor.execute("select * from items_bought")
    y=cursor.fetchall()
    items_bought={}
    for i in y:
        for j in i:
            b=[i[1], i[2]]
            items_bought[i[0]]=b
    n=int(input("enter total items: "))
    for i in range(n):
        g=input("enter item: ")
        if g in items_bought:
            print("This item already exists listed at", items_bought[g][1], "per piece")
            j=int(input('enter price: '))
            if j==items_bought[g][1]:
                h=int(input("enter quantity: "))
                x="update items_bought set quantity = quantity + %s where name = %s"
                cursor.execute(x,(h,g))
                print("")
            else:
                g=input("enter another name for this item: ")
                h=int(input("enter quantity: "))
                x="insert into items_bought values(%s, %s, %s)"
                cursor.execute(x,(g,h,j))
                print("")
        else:
            h=int(input('enter quantity: '))
            j=int(input('enter prices: '))
            x="insert into items_bought values(%s, %s, %s)"
            cursor.execute(x,(g,h,j))
            print("")
    con.commit()
    cursor.execute("select * from items_bought")
    y=cursor.fetchall()
    print("items bought")
    print("items : quantity : price")
    for i in y:
        print(i[0], ":", i[1], ":", i[2])
#Update_stock()

def Update_items_display(): 
    cursor.execute("select * from items_bought")
    y=cursor.fetchall()
    items_bought={}
    for i in y:
        for j in i:
            b=[i[1], i[2]]
            items_bought[i[0]]=b
    while True:
        n=int(input("enter total items to be sold: "))
        if n<=len(items_bought):
            for i in range(n):
                while True:
                    c=input('enter item: ')
                    if c in items_bought:
                        while True:
                            d=int(input('enter quantity: '))
                            if d<=items_bought[c][0]:
                                e=int(input('enter prices: '))
                                l=[c,d,e]
                                print("")
                                x="insert into items_display values(%s, %s, %s)"
                                cursor.execute(x,l)
                                break
                            else:
                                print('you only have', items_bought[c][0], c)
                        break
                    else:
                        print('item not in stock')
            break
        else:
            print('you only have', len(items_bought), 'items')
    con.commit()
    cursor.execute("select * from items_display")
    y=cursor.fetchall()
    print("items on display")
    print("items : quantity : price")
    for i in y:
        print(i[0], ":", i[1], ":", i[2])
#Update_items_display()

def order():
    global items_sold
    cursor.execute("select * from items_bought")
    items_bought=cursor.fetchall()
    cursor.execute("select * from items_display")
    y=cursor.fetchall()
    items_display={}
    for i in y:
        for j in i:
            b=[i[1], i[2]]
            items_display[i[0]]=b
    print(items_display)
    while True:
        n=int(input("enter the no of items: "))
        if n<=len(items_display):
            for i in range(n):
                while True:
                    a=input('enter item: ')
                    if a in items_display:
                        while True:
                            qty=int(input('enter quantity: '))
                            if qty<=items_display[a][0]:
                                p=items_display[a][1]
                                items_sold=[a,qty,p]
                                print("")
                                x="insert into items_sold values(%s, %s, %s)"
                                cursor.execute(x,items_sold)
                                x="update items_bought set quantity = quantity - %s where name = %s"
                                cursor.execute(x,(qty,a))
                                x="update items_display set quantity = quantity - %s where name = %s"
                                cursor.execute(x,(qty,a))
                                break
                            else:
                                print('we only have ', items_display[a][0], a)
                        break
                    else:
                        print('enter name correctly: ')
            break
        else:
            print("You only have ",len(items_display), 'items')
    con.commit()
    cursor.execute("select * from items_sold")
    y=cursor.fetchall()
    print("items sold")
    print("items : quantity : price")
    for i in y:
        print(i[0], ":", i[1], ":", i[2])
#order()

def Return():
    l=[]
    cursor.execute("select * from items_bought")
    items_bought=cursor.fetchall()
    cursor.execute("select * from items_display")
    items_display=cursor.fetchall()
    cursor.execute("select * from items_sold")
    y=cursor.fetchall()
    items_sold={}
    for i in y:
        for j in i:
            b=[i[1], i[2]]
            items_sold[i[0]]=b
    while True:
        n=int(input("enter the no of items: "))
        if n<=len(items_sold):
            for i in range(n):
                while True:
                    a=input('enter item: ')
                    if a in items_sold:
                        while True:
                            qty=int(input('enter quantity: '))
                            if qty<=items_sold[a][0]:
                                l.append([a,qty,items_sold[a][1]])
                                print("")
                                x="update items_bought set quantity = quantity + %s where name = %s"
                                cursor.execute(x,(qty,a))
                                x="update items_display set quantity = quantity + %s where name = %s"
                                cursor.execute(x,(qty,a))
                                x="update items_sold set quantity = quantity - %s where name = %s"
                                cursor.execute(x,(qty,a))
                                break
                            else:
                                print('you can only return', items_sold[a][0], a)
                        break
                    else:
                        print('enter name correctly')
            break
        else:
            print("You can only return",len(items_sold), 'items')
    print("items returned")
    print("items : quantity : price")
    for i in l:
        print(i[0], ":", i[1], ":", i[2])
    con.commit()
#Return()

def report():
    cursor.execute("select * from items_bought")
    items_bought=cursor.fetchall()
    cursor.execute("select * from items_display")
    items_display=cursor.fetchall()
    cursor.execute("select * from items_sold")
    items_sold=cursor.fetchall()
    c1=0
    c2=0
    for i in range(len(items_sold)):
        x=(items_sold[i][1]*items_sold[i][2]) 
        y=(items_bought[i][1]*items_bought[i][2])
        c1=c1+x
        c2=c2+y
    if c2-c1>=0:
        print("total loss: ", abs(c2-c1))
    elif c2-c1<0:
        print("total profit: ", abs(c2-c1))
    con.commit()
#report()    

def stock():
    cursor.execute("select * from items_bought")
    items_bought=cursor.fetchall()
    cursor.execute("select * from items_display")
    items_display=cursor.fetchall()
    cursor.execute("select * from items_sold")
    items_sold=cursor.fetchall()
    print("items bought")
    print("items : quantity : price")
    for i in items_bought:
        print(i[0], ":", i[1], ":", i[2])
    print("items on display")
    print("items : quantity : price")
    for i in items_bought:
        print(i[0], ":", i[1], ":", i[2])
    print("items sold")
    print("items : quantity : price")
    for i in items_bought:
        print(i[0], ":", i[1], ":", i[2])
    con.commit()
#stock()

def clear():
    print("1 for items bought")
    print("2 for items on display")
    print("3 for items sold")
    print("4 for all tables")
    n=int(input("enter table to be cleared: "))
    if n==1:
        cursor.execute("delete from items_bought")
        print("items bought cleared")
    elif n==2:
        cursor.execute("delete from items_display")
        print("items display cleared")
    elif n==3:
        cursor.execute("delete from items_sold")
        print("items sold cleared")
    elif n==4:
        cursor.execute("delete from items_bought")
        cursor.execute("delete from items_display")
        cursor.execute("delete from items_sold")
        print("all tables cleared")
    con.commit()
#clear()

#password
cursor.execute("select * from info")
x=cursor.fetchall()
y={}
for i in x:
    for j in i:
        b=[i[1], i[2]]
        y[i[0]]=b
def idcreate():
    ID=input("enter user id: ")
    if ID in y:
        print("this id already exists")
        while True:
            password=input("enter password: ")
            if y[ID][0]==password:
                print("WELCOME", y[ID][1])
                while True:                            
                    print("Select function you want to use")
                    print("1.Update Stock")
                    print("2.Update items on display")
                    print("3.Order")
                    print("4.Return")
                    print("5.Report")
                    print("6.Stock")
                    print("7.Clear Database")
                    m=int(input("Enter your choice:"))
                    if m==1:
                        Update_stock()
                    elif m==2:
                        Update_items_display()
                    elif m==3:
                        order()
                    elif m==4:
                        Return()
                    elif m==5:
                        report()
                    elif m==6:
                        stock()
                    elif m==7:
                        clear()
                    else:
                        print("Enter appropriate option!")
                        continue
                    j=input("Do you want to continue?y/n:")
                    if j!="y":
                        break
                break           
            else:
                print("incorrect password")
    else:
        name=input("enter user name: ")
        if b=="y":
            print("you password must have at least")
            print("6 characters")
            print("1 uppercase characters")
            print("1 number")
            while True:
                password=input("enter password: ")
                l="false"
                u="false"
                n="false"
                if len(password)>=6:
                    l="true"
                for i in password:
                    if i.isdigit():
                        n="true"
                                            
                    if i.isupper():
                        u="true"
                if l=="true" and u=="true" and n=="true":
                    password1=input("please re enter your password")
                    if password1==password:
                        print("password set")
                        cursor.execute("insert into info values(%s, %s, %s)",(ID,password,name))
                        con.commit()
                        break
                else:
                    if l=="false" and u=="true" and n=="true":
                        print("your password is not 6 characters long")
                    elif l=="true" and u=="false" and n=="true":
                        print("your password does not contain an uppercase alphabet")
                    elif l=="true" and u=="true" and n=="false":
                        print("your password does not contain any numbers")
                    elif l=="false" and u=="false" and n=="true":
                        print("your password is not 6 characters long and does not contain an uppercase alphabet")
                    elif l=="false" and u=="true" and n=="false":
                        print("your password is not 6 characters long and does not contain any numbers")
                    elif l=="true" and u=="false" and n=="false":
                        print("your password neither contains an uppercase alphabet nor any numbers ")
                    elif l=="false" and u=="false" and n=="false":
                        print("your password does not follow any of the given criteria")
while True:
    a=input("Do you already have an account? y/n: ")
    if a=="y":
        while True:
            ID=input("enter user ID: ")
            if ID in y:
                while True:
                    password=input("enter password: ")
                    if y[ID][0]==password:
                        print("WELCOME", y[ID][1])
                        while True:                            
                            print("Select function you want to use")
                            print("1.Update Stock")
                            print("2.Update items on display")
                            print("3.Order")
                            print("4.Return")
                            print("5.Report")
                            print("6.Stock")
                            print("7.Clear Database")
                            m=int(input("Enter your choice:"))
                            if m==1:
                                Update_stock()
                            elif m==2:
                                Update_items_display()
                            elif m==3:
                                order()
                            elif m==4:
                                Return()
                            elif m==5:
                                report()
                            elif m==6:
                                stock()
                            elif m==7:
                                clear()
                            else:
                                print("Enter appropriate option!")
                                continue
                            j=input("Do you want to continue?y/n:")
                            if j!="y":
                                break
                        break                      
                    else:
                        print("incorrect password")
                break           
            else:
                print("user id not found")
                b=input("would you like to make an account? y/n")
                if b=="y":
                    idcreate()
                elif b=="n":
                    print("enter correct user id")
        break
    elif a=="n":
        b=input("would you like to create an account? y/n: ")
        if b=="y":
            idcreate()
        elif b=="n":
            print("Thank You! :)")
            break
        break
    else:
        print("please enter y or n")
                                
cursor.close()
con.close()
