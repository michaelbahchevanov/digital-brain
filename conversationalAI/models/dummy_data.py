import geocoder

class DummyData:
    # Variables
    products = []
    
    # Products data
    def getProducts(gender, skinType, hairType):

        menDrySkinProducts = [
            {'ProductID': 1, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA INTENSIVE 24H FACE CREAM", 'Skin Type': 'Dry',
             'Gender': 'Man', 'Size': '50ML', 'Price': 10.49},
            {'ProductID': 2, 'Name': 'NIVEA MEN SENSITIVE COOLING AFTERSHAVE BALSEM', 'Skin Type': 'Dry',
             'Gender': 'Man', 'Size': '100ML', 'Price': 9.99},
        ]

        menSensitiveSkinProducts = [
            {'ProductID': 3, 'Name': "NIVEA MEN SENSITIVE STUBBLE MOISTURISER CRÈME",
             'Skin Type': 'Sensitive', 'Gender': 'Man', 'Size': '50ML', 'Price': 13.49},
            {'ProductID': 4, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA SENSITIVE MOISTURIZING FACIAL CARE",
             'Skin Type': 'Sensitive', 'Gender': 'Man', 'Size': '50ML', 'Price': 15.15}
        ]

        womenDrySkinProducts = [
            {'ProductID': 1, 'Name': "DIADERMINE HYDRA NUTRITION DAY CREAM", 'Skin Type': 'Dry',
             'Gender': 'Woman', 'Size': '50ML', 'Price': 10.49},
            {'ProductID': 2, 'Name': 'OLAY WOMEN REGENERIST PERFUME-FREE NIGHT CREAM', 'Skin Type': 'Dry',
             'Gender': 'Woman', 'Size': '50ML', 'Price': 37.99},
        ]

        womenSensitiveSkinProducts = [
            {'ProductID': 3, 'Name': "NIVEA ESSENTIALS RESTORATIVE NIGHT CREAM",
             'Skin Type': 'Sensitive', 'Gender': 'Woman', 'Size': '50ML', 'Price': 13.49},
            {'ProductID': 4, 'Name': "GARNIER SKIN ACTIVE BOTANICAL DAY CREAM WITH ROSE WATER",
             'Skin Type': 'Sensitive', 'Gender': 'Woman', 'Size': '50ML', 'Price': 7.05}
        ]

        menDryHairProducts = [
            {'ProductID': 5, 'Name': "ALPECIN HYBRID CAFFEINE SHAMPOO", 'Hair Type': 'Dry', 'Gender': 'Man',
             'Size': '250ML', 'Price': 7.69},
            {'ProductID': 6, 'Name': "Schwarzkopf Repair & Care Shampoo", 'Hair Type': 'Dry', 'Gender': 'Both',
             'Size': '400ML', 'Price': 2.59}
        ]

        menNormalHairProducts = [
            {'ProductID': 7, 'Name': "NIVEA MEN STRONG POWER SHAMPOO", 'Hair Type': 'Normal', 'Gender': 'Man',
             'Size': '250ML', 'Price': 3.79},
            {'ProductID': 8, 'Name': "John Frieda Frizz Ease Dream Curls Shampoo", 'Hair Type': 'Normal',
             'Gender': 'Man', 'Size': '250ML', 'Price': 11.99}
        ]

        womenDryHairProducts = [
            {'ProductID': 5, 'Name': "GARNIER LOVING BLENDS ARGAN & CAMELLIA OIL SUBLIME MASK", 'Hair Type': 'Dry', 'Gender': 'Women',
             'Size': '300ML', 'Price': 6.79},
            {'ProductID': 6, 'Name': "KRUIDVAT ARGAN OIL & CARE HAIR OIL", 'Hair Type': 'Dry', 'Gender': 'Woman',
             'Size': '150ML', 'Price': 2.59}
        ]

        womenNormalHairProducts = [
            {'ProductID': 7, 'Name': "HAIRWONDER HAIR REPAIR CREAM", 'Hair Type': 'Normal', 'Gender': 'Woman',
             'Size': '150ML', 'Price': 9.09},
            {'ProductID': 8, 'Name': "ANDRÉLON INTENSE SUMMER BLONDE SHAMPOO", 'Hair Type': 'Normal',
             'Gender': 'Woman', 'Size': '300ML', 'Price': 4.49}
        ]

        if skinType == "dry" and gender == "man":
            DummyData.products.append(menDrySkinProducts)
        elif skinType == "sensitive" and gender == "man":
            DummyData.products.append(menSensitiveSkinProducts)
        elif skinType == "dry" and gender == "woman":
            DummyData.products.append(womenDrySkinProducts)
        elif skinType == "sensitive" and gender == "woman":
            DummyData.products.append(womenSensitiveSkinProducts)

        if hairType == "dry" and gender == "man":
            DummyData.products.append(menDryHairProducts)
        elif hairType == "normal" and gender == "man":
            DummyData.products.append(menNormalHairProducts)
        if hairType == "dry" and gender == "woman":
            DummyData.products.append(womenDryHairProducts)
        elif hairType == "normal" and gender == "woman":
            DummyData.products.append(womenNormalHairProducts)

        print(DummyData.products)
        return DummyData.products

    # Products on sale data
    def getSaleProducts(self):
        saleProducts = [
            {'Product name': DummyData.findProduct(1), 'Sale': '2nd half price'},
            {'Product name': DummyData.findProduct(3), 'Sale': '1 + 1 free'}
        ]

        return saleProducts

    # User profile data
    def buildUserProfile(gender, skin_type, hair_type):
        userProfile = [
            {'Gender': gender, 'Skin Type': skin_type, 'Hair Type': hair_type, 'Address': 'Antwerpenlaan 22, Eindhoven'}
        ]

        return userProfile

    # Return a product from product list based on ID
    @staticmethod
    def findProduct(id):
        for i in DummyData.products:
            for p in i:
                print()
                if p['ProductID'] == id:
                    return p['Name']

    # Shopping history data
    def getShoppingHistory(self):
        orders = [
            {'ProductID': DummyData.findProduct(5), 'Quantity': 4, 'Price': 30.76}
        ]

        return orders

    # Method to return user's ip location
    def getCity(self):
        g = geocoder.ip('me')
        print(g.city)
        Eindhoven = [
            "Winkelcentrum Woensel", "Strijpsestraat"
        ]

        Tilburg = [
            "Pieter Vredeplein", "Besterdring", "Heuvelstraat"
        ]

        if g.city in ["IJsselstein", "Breda"]:
            return Eindhoven
        elif g.city in "Tilburg":
            return Tilburg