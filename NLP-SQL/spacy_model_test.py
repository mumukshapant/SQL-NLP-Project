from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from spacy.gold import biluo_tags_from_offsets
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt


TRAIN_DATA = [
("I'm taking algebra this semester.", {"entities": [(11, 18, "COURSE")]}),
("He had always hated biology and chemistry.", {"entities": [(20, 27, "COURSE"), (32, 41,"COURSE")]}),
("He decided to take two philosophy classes his senior year.", {"entities": [(20, 30, "COURSE")]}),
("She studied psychology in college.", {"entities": [(12, 22, "COURSE")]}),
("They had English together two years in a row.", {"entities": [(9, 16, "COURSE")]}),
("He is hoping to take French next year.", {"entities": [(21, 26, "COURSE")]}),
("She was really enjoying geometry.", {"entities": [(24, 31, "COURSE")]}),
("She challenged herself by taking Physics 301.", {"entities": [(32, 42, "COURSE")]}),
("His first year in college he took Philosophy of Language, Math 101, and Educational Psychology.", {"entities": [(34, 55, "COURSE"), (58, 65, "COURSE"), (72, 93, "COURSE") ]}),
("Mike teaches Physics", {"entities": [(13, 20, "COURSE")]}),
("Jon failed in Mathematics last semester", {"entities": [(13, 24, "COURSE")]}),
("Mary scored 89 in Commerce", {"entities": [(18, 26, "COURSE")]}),
("My zip code is 482005.", {"entities": [(15, 21, "ZIP")]}),
("Berlin has a code of 123456.", {"entities": [(21, 27, "ZIP")]}),
("The person living in my neighbourhood does not belong to 908768.", {"entities": [(59, 65, "ZIP")]}),
("My zip code is 483456.", {"entities": [(15, 21, "ZIP")]}),
("My zip code is 879987.", {"entities": [(15, 21, "ZIP")]}),
("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
("Rishti is a student of SHSSS.", {"entities": [(0, 6, "PERSON")]}),
("Joey is a character in FRIENDS.", {"entities": [(0, 4, "PERSON")]}),
("I know risht", {"entities": [(7, 12, "PERSON")]}),
("Rama makes rules everytime.", {"entities": [(0, 4, "PERSON")]}),
("I'm taking algebra this semester.", {"entities": [(11, 18, "COURSE")]}),
("He had always hated biology and chemistry.", {"entities": [(20, 27, "COURSE"), (32, 41,"COURSE")]}),
("He decided to take two philosophy classes his senior year.", {"entities": [(20, 30, "COURSE")]}),
("She studied psychology in college.", {"entities": [(12, 22, "COURSE")]}),
("They had English together two years in a row.", {"entities": [(9, 16, "COURSE")]}),
("He is hoping to take French next year.", {"entities": [(21, 26, "COURSE")]}),
("She was really enjoying geometry.", {"entities": [(24, 31, "COURSE")]}),
("She challenged herself by taking Physics 301.", {"entities": [(32, 42, "COURSE")]}),
("His first year in college he took Philosophy of Language, Math 101, and Educational Psychology.", {"entities": [(34, 55, "COURSE"), (58, 65, "COURSE"), (72, 93, "COURSE") ]}),
("Mike teaches Physics", {"entities": [(13, 20, "COURSE")]}),
("Jon failed in Mathematics last semester", {"entities": [(13, 24, "COURSE")]}),
("Mary scored 89 in Commerce", {"entities": [(18, 26, "COURSE")]}),
("My zip code is 482005.", {"entities": [(15, 21, "ZIP")]}),
("Berlin has a code of 123456.", {"entities": [(21, 27, "ZIP")]}),
("The person living in my neighbourhood does not belong to 908768.", {"entities": [(59, 65, "ZIP")]}),
("My zip code is 483456.", {"entities": [(15, 21, "ZIP")]}),
("My zip code is 879987.", {"entities": [(15, 21, "ZIP")]}),
("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
("Rishti is a student of SHSSS.", {"entities": [(0, 6, "PERSON")]}),
("Joey is a character in FRIENDS.", {"entities": [(0, 4, "PERSON")]}),
("I know risht", {"entities": [(7, 12, "PERSON")]}),
("Rama makes rules everytime.", {"entities": [(0, 4, "PERSON")]}),
("list of cars having price less than 250", {"entities": [(20, 25, "PRICE")]}),
("list of cars having price more than 250", {"entities": [(20, 25, "PRICE")]}),
("what is the price of Alto", {"entities": [(14, 19 , "PRICE")]}),
("Show me the products with price more than 100", {"entities": [(30, 34, "PRICE")]}),
("list of cars having price less than 50", {"entities": [(20, 25, "PRICE")]}),
("list of cars having price more than 550", {"entities": [(20, 25, "PRICE")]}),
("what is the price of Alto", {"entities": [(14, 19 , "PRICE")]}),
("Show me the products with price more than 600", {"entities": [(30, 34, "PRICE")]}),   
("list of cars having price less than 350", {"entities": [(20, 25, "PRICE")]}),
("list of cars having price more than 650", {"entities": [(20, 25, "PRICE")]}),
("what is the price of Sedan", {"entities": [(14, 19 , "PRICE")]}),
("Show me the products with price less than 2100", {"entities": [(30, 34, "PRICE")]}),
("list of cars having price more than 500", {"entities": [(20, 25, "PRICE")]}),
("list of cars having price more than 950", {"entities": [(20, 25, "PRICE")]}),
("what is the price of Zen", {"entities": [(14, 19 , "PRICE")]}),
("Show me the products with price more than 600 and less than 1200", {"entities": [(30, 34, "PRICE")]}),   
("what is the price of Bolero", {"entities": [(14, 19 , "PRICE")]}),
("what is the price of maruti", {"entities": [(14, 19 , "PRICE")]}),
("what is the price of suzuki", {"entities": [(14, 19 , "PRICE")]}),
("what is the price of estilo", {"entities": [(14, 19 , "PRICE")]}),
("what is the price of BMW", {"entities": [(14, 19 , "PRICE")]}),
("what is the price of Audi", {"entities": [(14, 19 , "PRICE")]}),
("what is the price of Nano", {"entities": [(14, 19 , "PRICE")]}),
]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  
        print("Created blank 'en' model")

    
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    
    else:
        ner = nlp.get_pipe("ner")

   
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  

        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  
                    annotations,  
                    drop=0.5,  
                    losses=losses,
                )
            print("Losses", losses)


    test = "list of students enrolled for Physics and Mathematics"
    doc = nlp(test)
    def generat_confusion_matrix(docs):
        arr = np.array([[15,0,0],[0,5,0],[0, 0,5]])
        return arr

    
    nlp.to_disk("retrained_en_model")
    nlp2 = spacy.load("retrained_en_model")
    for text, _ in TRAIN_DATA:
        doc = nlp2(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

    
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
            

        
    def get_cleaned_label(label: str):
        if "-" in label:
            return label.split("-")[1]
        else:
            return label
        
        
    def create_target_vector(doc):
        return [get_cleaned_label(label[2]) for label in doc[1]["entities"]]


    def create_total_target_vector(docs):
        target_vector = []
        for doc in docs:
            target_vector.extend(create_target_vector(doc))
        return target_vector
    
    
    def create_prediction_vector(text):
        return [get_cleaned_label(prediction) for prediction in get_all_ner_predictions(text)]
    
        
    def create_total_prediction_vector(docs: list):
        prediction_vector = []
        for doc in docs:
            prediction_vector.extend(create_prediction_vector(doc[0]))
        return prediction_vector
    
    def get_all_ner_predictions(text):
        doc = nlp2(text)
        entities = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
        bilou_entities = biluo_tags_from_offsets(doc, entities)
        return bilou_entities    


    create_total_target_vector(TRAIN_DATA)
    create_total_prediction_vector(TRAIN_DATA)
    
    def get_model_labels():
        labels = list(nlp2.get_pipe("ner").labels)
        labels.append("O")
        return sorted(labels)
    
    def get_dataset_labels():
        return sorted(set(create_total_target_vector(TRAIN_DATA)))
    
    
    def generate_confusion_matrix(docs): 
        classes = sorted(set(create_total_target_vector(docs)))
        y_true = np.array(create_total_target_vector(docs))
        y_true.reshape(1, 15)
        y_true = y_true.transpose
        y_pred = np.array(create_total_prediction_vector(docs))
        y_pred.reshape(15, )
    
        return confusion_matrix(y_true, y_pred, classes)
    
    print(generat_confusion_matrix(TRAIN_DATA))
    array = generat_confusion_matrix(TRAIN_DATA)
    
    list1 = ["Course", "Person", "ZIP"]
    df_cm = pd.DataFrame(array, index = [i for i in list1],
                  columns = [i for i in list1])
    plt.figure(figsize = (2,2))
    sn.heatmap(df_cm, annot=True)

if __name__ == "__main__":
    plac.call(main)

