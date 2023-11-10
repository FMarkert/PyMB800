class Base_Question:
    def __init__(self,id,question_text,src,type,comment,casestudy):
        self.id = id 
        self.question_text = question_text
        self.src = src
        self.type = type
        self.comment = comment
        self.casestudy = casestudy
        print("Basisklasse erstellt")
    
    def display_question_text(self): #Methoden zum Anzeigen des Fragetextes, der Quelle, Kommentare und ggf. zugehöriger Casestudy
        pass
    
    def display_src(self): 
        pass

    def display_comment(self):
        pass 
    
    def display_casestudy(self):
        pass




class Drag_Drop_Order(Base_Question):
    def __init__(self,items,correct_answer):
        super().__init__()
        self.items = items
        self.correct_answer = correct_answer
        print("Drag_Drop_Order Frage erstellet") #Test
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer

    
class Drag_Drop_Pairs(Base_Question):
    def __init__(self,pairs):
        super().__init__()
        self.pairs = pairs 


class Dropdown(Base_Question):
    def __init__(self,items):
        super().__init__()
        self.items = items 


class Multiple_Choice(Base_Question):
    def __init__(self,items):
        super().__init__()
        self.items = items 
        print("MC Frage erstellt") #Test
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer



