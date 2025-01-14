import json 
import mysql.connector
import re

#Fill with your own data
cnx = mysql.connector.connect(user="root",password="root",host='127.0.0.1',database="products")

cursor = cnx.cursor()

def create_table():

    products_table = """CREATE TABLE products(ID INTEGER PRIMARY KEY,
    title VARCHAR(120),
    description VARCHAR(300),
    price FLOAT,
    discountPercentage FLOAT,
    rating FLOAT, 
    stock INTEGER,
    brand VARCHAR(60),
    weight INT,
    width FLOAT, 
    height FLOAT,
    depth FLOAT,
    warrantyInformation VARCHAR(120),
    shippingInformation VARCHAR(90),
    availabilityStatus VARCHAR(90),
    thumbnail VARCHAR(200),
    idcategory INTEGER)
    """

    category_table = "CREATE TABLE categories(ID INTEGER PRIMARY KEY AUTO_INCREMENT,name VARCHAR(80))"

    review_table = """CREATE TABLE reviews(ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    comment VARCHAR(120),
    date DATETIME,
    rating INTEGER,idproduct INTEGER,iduser INTEGER)
    """

    image_table = "CREATE TABLE images(ID INTEGER PRIMARY KEY AUTO_INCREMENT, image VARCHAR(120),idproduct INTEGER)"

    tag_table = "CREATE TABLE tags(ID INTEGER PRIMARY KEY AUTO_INCREMENT,name VARCHAR(40))"

    user_table = "CREATE TABLE users(ID INTEGER PRIMARY KEY AUTO_INCREMENT,mail VARCHAR(100),name VARCHAR(100),username VARCHAR(80),password VARCHAR(100))"

    tag_product_table = "CREATE TABLE tagproduct(ID INTEGER PRIMARY KEY AUTO_INCREMENT,idtag INTEGER,idproduct INTEGER)"

    tables = [products_table,
            category_table,
            review_table,
            image_table,
            tag_table,
            user_table,
            tag_product_table,]

    for table in tables:
        cursor.execute(table)


#Call this method the first time you execute the program to create the tables of the database
create_table()

with open("./data.json","rt") as f:
    content = json.loads(f.read())["products"]
    for k,v in content[0].items():
        print(k,v)

    for product in content:
        print(product)
        p = {"id":product['id'],
             'title':product['title'],
             'description':product['description'],
             "price":product['price'],
             "discountPercentage":product['discountPercentage'],
             "rating":product['rating'],
             "stock":product['stock'],
             "brand":product['brand'] if "brand" in product.keys() else None,
             "weight":product['weight'],
             "width":product['dimensions']['width'],
             "height":product['dimensions']['height'],
             "depth":product['dimensions']['depth'],
             "warrantyInformation":product["warrantyInformation"],
             "shippingInformation":product['shippingInformation'],
             "availabilityStatus":product['availabilityStatus'],
             "thumbnail":product["thumbnail"]}
        
        categoryFound = cursor.execute("SELECT * FROM categories WHERE name=%s",(product['category'],))
        cursor.fetchall()
        if not categoryFound:
            cursor.execute("INSERT INTO categories(name) VALUES(%s)",(product['category'],))
            print(cursor.fetchone())
            
        category_id = cursor.lastrowid

        p['idcategory'] = category_id
        cursor.execute("INSERT INTO products VALUES({})".format(",".join(["%s" for i in p.keys()])),list(p.values()))

        for img in product["images"]:
            cursor.execute("INSERT INTO images(image,idproduct) VALUES(%s,%s)",(img,product['id']))
            img_id= cursor.lastrowid
        for tag in product['tags']:
            foundTag = cursor.execute("SELECT * FROM tags WHERE name=%s",(tag,))
            cursor.fetchall()
            if not foundTag:
                cursor.execute("INSERT INTO tags(name) VALUES(%s)",(tag,))
            tag_id = cursor.lastrowid
            cursor.execute("INSERT INTO tagproduct(idtag,idproduct) VALUES(%s,%s)",(tag_id,product['id']))

        for review in product["reviews"]:
            
          
            username = review["reviewerName"].replace(" ","").lower()
            userFound = cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
            cursor.fetchall()
            if not userFound:
                cursor.execute("INSERT INTO users(mail,password,username,name) VALUES(%s,%s,%s,%s)",(review['reviewerEmail'],username+"123",username,review["reviewerName"]))
            
            cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
            
            user_id = cursor.fetchall()[0][0]

            cursor.execute("INSERT INTO reviews(rating,comment,date,idproduct,iduser) VALUES(%s,%s,%s,%s,%s)",(review["rating"],
                            review["comment"],
                            re.sub(r'[.][0-9]*Z',""," ".join(review["date"].split("T"))),product['id'],user_id))

            cnx.commit()



   
    