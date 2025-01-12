import json 
# see how many categories and tags there are
#TODO:
#define tables and relationships 
#create .json files with appropiate data to fill on mysql
#create .json files in different repo 

#products.json
#product_category.json
#categories.json
#users.json
#review_user.json
#review.json
#reviewproduct.json
#images.json
#imageproduct.json

#join data with separate files compare to original data to check data integrity

with open("./data.json","rt") as f:
    content = json.loads(f.read())["products"]
    for k,v in content[0].items():
        print(k,v)
    products = []
    categories = []
    product_category = []
    images = []
    product_images = []
    tags= [] 
    product_tag=[]
    users = []
    reviews=[]
    user_review =[]
    product_review = []

    #TODO:
    
   
    

    for product in content:
        p = {"id":product['id'],
             'title':product['title'],
             'description':product['description'],
             "price":product['price'],
             "discountPercentage":product['discountPercentage'],
             "rating":product['rating'],
             "stock":product['stock'],
             "brand":product['brand'],
             "weight":product['weight'],
             "width":product['dimensions']['width'],
             "height":product['dimensions']['height'],
             "depth":product['dimensions']['depth'],
             "warrantyInformation":product["warrantyInformation"],
             "shippingInformation":product['shippingInformation'],
             "availabilityStatus":product['availabilityStatus'],
             "thumbnail":product["thumbnail"]}
        products.append(p)

        if len(categories) == 0:
            categories.append({"id":0,"name":product['category']})
        else:
            #check if already added
            category = [c for c in categories if c['name'] == product['category']]
            if len(category) == 0:
                categories.append({"id":categories[-1]['id']+1,"name":product['category']})

        
        
        category = [c for c in categories if c['name'] == product['category']]

        product_category_id = 0
        if len(product_category) != 0:
            product_category_id = product_category[-1]['id']+1
        product_category.append({"id":product_category_id,"id_product":product['id'],"id_category":category[0]['id']})

        for img in product["images"]:
            img_id = 0
            if len(images) != 0:
                img_id = images[-1]['id']+1   
            images.append({"id":img_id,"image":img})
            product_images_id = 0
            if len(product_images)!=0:
                product_images_id = product_images[-1]['id']+1
            product_images.append({"id":product_images_id,"id_image":img_id,"id_product":product['id']})

       
        for tag in product['tags']:
            tag_id = 0
            if len(tags) != 0:
                tag_id = images[-1]['id']+1
            tagFound = [t for t in tags if t['name'] == tag]
            if len(tagFound) == 0:
                tags.append({"id":tag_id,"name":tag})
            
            product_tag_id = 0
            if len(product_tag) != 0:
                product_tag_id = product_tag[-1]["id"]+1
            tagFound = [t for t in tag if t['name'] == tag] 
            product_tag.append({"id":product_tag_id,"id_product":product["id"],"id_tag":tagFound[0]['id']})

        for review in product["reviews"]:
            review_id = 0
            if len(reviews) != 0:
                review_id = reviews[-1]["id"]+1

            reviews.append({"id":review_id,
                            "rating":review["rating"],
                            "comment":review["comment"],
                            "date":review["date"]})
            
            username = review["reviewerName"].replace(" ","").lower()
            user = {"mail":review['reviewerEmail'],
                    "password":username+"123",
                    "username":username,
                    "name":review["reviewerName"]}
            user_id = 0
            if len(users) != 0:
                user_id = users[-1]["id"]+1
            user["id"] = user_id

            userFound = [u for u in users if u['mail'] == user['mail']]
            if len(userFound) == 0:
                users.append(user)

            userFound = [u for u in users if u['mail'] == user['mail']]
            user_review_id = 0
            if len(user_review) != 0:
                user_review_id = user_review_id[-1]['id'] +1
            user_review.append({"id":user_review_id,"id_user":userFound[0]['id'],"id_review":review_id})
        
            product_review_id = 0
            if len(product_review) != 0:
                product_review_id = product_review[-1]['id']+1
            product_review.append({"id":product_review_id,"id_review":review_id,"id_product":product["id"]})
#write to respective files and try comparisons


   
    