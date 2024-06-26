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
        return self.question_text
    
    def display_src(self): 
        return self.src

    def display_comment(self):
        return self.comment 
    
    def display_casestudy(self):
        return self.casestudy


class Drag_Drop_Order(Base_Question):
    def __init__(self,id,question_text,src,type,comment,casestudy,items):
        super().__init__(id,question_text,src,type,comment,casestudy)
        self.items = items
        print("Drag_Drop_Order Frage erstellt") #Test
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer

    
class Drag_Drop_Pairs(Base_Question):
    def __init__(self,id,question_text,src,type,comment,casestudy,items):
        super().__init__(id,question_text,src,type,comment,casestudy)
        self.items = items 
    def display_pairs(self):
        return self.items 
    def check_answer(self, user_answer):
        return user_answer == self.items

class Dropdown(Base_Question):
    def __init__(self,id,question_text,src,type,comment,casestudy,items,correct_answer):
        super().__init__(id,question_text,src,type,comment,casestudy)
        self.items = items 
        self.correct_answer = correct_answer
    def display_items(self):
        return self.items
    def display_c_answers(self):
        return self.correct_answer
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer
        


class Multiple_Choice(Base_Question):
    def __init__(self,id,question_text,src,type,comment,casestudy,items,correct_answer):
        super().__init__(id,question_text,src,type,comment,casestudy)
        self.items = items 
        self.correct_answer = correct_answer
        print("MC Frage erstellt") #Test
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer