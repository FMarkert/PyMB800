import random

#Daten für PDF


# Alles soll ohne eckige Klammern, ohne geschweifte Klammern und ohne Anführungszeichen angezeigt werden
# Die Fragen sollen nummeriert werden 
# Über jeder Frage soll auch die id gezeigt werden
# Richtig beantwortete Fragen sollen grün hervorgehoben werden, falsch beantwortete Fragen rot

#Beispiele, wie user_answer_list und questions aufgebaut sind

user_answers_list = [{'6': ['View the Location Code for available inventory', 'Choose Make Invoice']}, {'26': {'Customer Posting Group': 'Specific posting group', 'Gen. Business Posting Group': 'General posting group', 'Gen. Product Posting Group': 'General posting group', 'Inventory Posting Group': 'Specific posting group', 'VAT Business Posting Group': 'Tax posting groups', 'VAT Product Poting Group': 'Tax posting groups', 'Vendor Posting Group': 'Specific posting group'}}, {'30': ['B']}, {'1': {'1': 'Create a No. Series.', '2': 'Create the Data template.', '3': 'Define the No. Series on the configuration template.'}}, {'2': ['A', 'C']}]


questions_origin = [{'casestudy': '', 'comment': '', 'correct_answer': ['View the Item Availability by Periods', 'Choose Make Order'], 'id': 6, 'items': {'1': {'options': ['View the Location Code for available inventory', 'View the Item Availability by Periods', 'Check the Catalog on the Sales Line Details'], 'text': 'Deliver on a specific customer date '}, '2': {'options': ['Choose Make Invoice', 'Choose Copy Document', 'Choose Make Order'], 'text': 'Deliver on a specific customer date '}}, 'question_text': 'You need to create the process for salespeople. \nWhat should you do? To answer, select the appropriate options in the answer area. \nNOTE: Each correct selection is worth one point.', 'src': 'l4d', 'type': 'dropdown'}, {'casestudy': '', 'comment': '', 'id': 26, 'items': {'Customer Posting Group': 'Specific posting group', 'Gen. Business Posting Group': 'General posting group', 'Gen. Product Posting Group': 'General posting group', 'Inventory Posting Group': 'Specific posting group', 'VAT Business Posting Group': 'Tax posting groups', 'VAT Product Poting Group': 'Tax posting groups', 'Vendor Posting Group': 'Specific posting group'}, 'question_text': 'You set up a new company for a customer. \nThe customer provides you with the chart of accounts and the preferred grouping of items, vendors, and customers. \nYou must ensure that item posting corresponds with the grouping preferences and chart of accounts for the customer. \nYou need to create the posting groups and setup. \nWhich type of posting groups should you create? \nTo answer, drag the appropriate posting group types to the correct entities. \nEach posting group type may be used once, more than once, or not at all.', 'src': 'l4d', 'type': 'drag_drop_pairs'}, {'casestudy': '', 'comment': '', 'correct_answer': ['B'], 'id': 30, 'items': {'A': 'Yes', 'B': 'No'}, 'question_text': 'You are implementing Dynamics 365 Business Central for a company. \nThe company provides subscription services to their customers. \nThe subscription invoices are almost identical each month. \nThe company wants to set up recurring sales lines for subscription invoices. \nYou need to create systems for creating subscription invoices. \nSolution: Create a new recurring sales line code. \nThen, run the Create Recurring Invoices batch to create the invoice. \nDoes the solution meet the goal?', 'src': 'l4d', 'type': 'multiple_choice'}, {'casestudy': '', 'comment': '', 'id': 1, 'items': {'1': 'Create a No. Series.', '2': 'Create the Data template.', '3': 'Define the No. Series on the configuration template.'}, 'question_text': 'You need to design a process to resolve the broker issues for Accounts. \nWhich three actions should perform in sequence? \nTo answer, move the appropriate actions from the list of actions to the answer area and arrange them in the correct order. \nNOTE: More than one order of answer choices is correct. \nYou will receive credit for any of the correct orders you select.', 'src': 'l4d', 'type': 'drag_drop_order'}, {'casestudy': '', 'comment': '', 'correct_answer': ['A', 'C'], 'id': 2, 'items': {'A': 'Set up payment terms with a value of CM+20D for the due date calculation.', 'B': 'Assign the payment terms to the customer price group.', 'C': 'Assign the payment terms to the customer.', 'D': 'Assign the payment terms to the customer posting group.', 'E': 'Set up payment terms with a value of D20 for the due date calculation.'}, 'question_text': 'You need to set up payment terms for buying groups. \nWhich two actions should you perform? \nEach correct answer presents part of the solution. \nNOTE: Each correct selection is worth one point.', 'src': 'l4d', 'type': 'multiple_choice'}]

questions = questions_origin


print_list = []

    
for question in questions:
        if question.get('type  ') == 'dropdown':  # Relevante Daten für Fragetyp Dropdown
            id = question.get('id')
            question_type = question.get('type')
            question_text = question.get('question_text')
            items_raw = question.get('items') # Dictionary - Schlüssel sind Nummerierung und Werte sind Dictionary mit Textteil der Antwort und den optionen
            correct_answer = question.get('correct_answer')
            user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
            print_unit = [question_type, id, question_text, items_raw, correct_answer, user_answer]
            print(print_unit)
            print_list.append(print_unit)            

            #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
            # Item i, options, correct_answer i, user_answer i

        elif question.get('type') == 'multiple_choice':
            id = question.get('id')
            question_type = question.get('type')

            question_text = question.get('question_text')
            items_raw = question.get('items') # Dictionary mit Aufzählung (A-Z) als Schlüssel und den Antwortmöglichkeiten als Werten
            correct_answer = question.get('correct_answer') # Liste mit den Schlüsseln der korrekten Antworten
            user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
            print_unit = [question_type, id, question_text, items_raw, correct_answer, user_answer]
            print_list.append(print_unit)
            #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
            # Werte aus items_raw aufgelistet untereinander mit den Schlüsseln als Aufzählungszeichen, dann correct_answer, dann user_answer
        
        elif question.get('type') == 'drag_drop_order':
            id = question.get('id')
            question_type = question.get('type')
            question_text = question.get('question_text')
            items_raw = question.get('items') # Dictionary mit Zahlen als String, die die Reihenfolge darstellen sollen als Schlüssel und der jeweiligen Antwort als Schlüssel
            user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
            print_unit = [question_type, id, question_text, items_raw, user_answer]
            print_list.append(print_unit)
        
            
            #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
            # Werte aus items_raw aufgelistet untereinander mit den Schlüsseln als Aufzählungszeichen stellt die richtige Antwort da, danach user_answer in gleicher Form darstellen
        
        elif question.get('type') == 'drag_drop_pairs':
            id = question.get('id')
            question_type = question.get('type')
            question_text = question.get('question_text')
            items_raw = question.get('items') # Dictionary: Schlüssel und Wert geben immer ein Paar
            user_answer = [answer[str(id)] for answer in user_answers_list if str(id) in answer][0]
            print_unit = [question_type, id, question_text, items_raw, user_answer]
            print_list.append(print_unit)

            #Anzeige in pdf: Nach der id soll der question_text angezeigt werden, danach der Block mit den Antworten, der für jede Frage so aussehen soll:
            #Schlüssel und Werte aus items_raw sollen jeweils in einer eingenen Zeile aufgelistet untereinenderstehen, danach soll user_answer im gleichen Stil angezeigt werden

def shuffle_questionpool(questions): # Die Liste mit Fragen wird durchgemischt 
    random.shuffle(questions)
    for question in questions:
        items = question["items"]
        print(items)
        pool = []
        pool.append(items)
    return pool

shuffle_questionpool(questions)